use std::sync::Mutex;
#[cfg(any(target_os = "macos", target_os = "ios"))]
use tauri::{Emitter, Manager};

/// File ricevuti dal sistema (Finder / Esplora risorse) non ancora letti dalla finestra.
struct Pending(Mutex<Vec<String>>);

/// La finestra chiede i file in attesa (all'avvio e a ogni evento "files-opened").
#[tauri::command]
fn take_pending(state: tauri::State<Pending>) -> Vec<String> {
    std::mem::take(&mut *state.0.lock().unwrap())
}

/// Legge l'immagine dal disco e la passa alla finestra come dati binari.
#[tauri::command]
fn read_image(path: String) -> Result<tauri::ipc::Response, String> {
    std::fs::read(&path)
        .map(tauri::ipc::Response::new)
        .map_err(|e| e.to_string())
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    // Windows / Linux: il file arriva come argomento ("Apri con…" o doppio clic).
    let args: Vec<String> = std::env::args()
        .skip(1)
        .filter(|a| !a.starts_with('-'))
        .collect();

    tauri::Builder::default()
        .manage(Pending(Mutex::new(args)))
        .invoke_handler(tauri::generate_handler![take_pending, read_image])
        .build(tauri::generate_context!())
        .expect("impossibile avviare Pano Viewer")
        .run(|app, event| {
            // macOS: il Finder consegna i file con un evento, anche ad app già aperta.
            #[cfg(any(target_os = "macos", target_os = "ios"))]
            if let tauri::RunEvent::Opened { urls } = &event {
                let paths: Vec<String> = urls
                    .iter()
                    .filter_map(|u| u.to_file_path().ok())
                    .map(|p| p.to_string_lossy().into_owned())
                    .collect();
                if let Some(state) = app.try_state::<Pending>() {
                    state.0.lock().unwrap().extend(paths);
                }
                let _ = app.emit("files-opened", ());
            }
            let _ = (app, event);
        });
}
