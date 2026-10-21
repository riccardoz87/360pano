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

/// Tutte le immagini nella stessa cartella del file, in ordine di nome (img2 prima di img10).
#[tauri::command]
fn list_siblings(path: String) -> Result<Vec<String>, String> {
    let p = std::path::Path::new(&path);
    let dir = p.parent().ok_or("cartella non trovata")?;
    let mut files: Vec<std::path::PathBuf> = std::fs::read_dir(dir)
        .map_err(|e| e.to_string())?
        .filter_map(|e| e.ok().map(|e| e.path()))
        .filter(|f| f.is_file() && is_image(f))
        .filter(|f| !f.file_name().map_or(false, |n| n.to_string_lossy().starts_with("._")))
        .collect();
    files.sort_by(|a, b| natural_cmp(&name_of(a), &name_of(b)));
    Ok(files.into_iter().map(|f| f.to_string_lossy().into_owned()).collect())
}

fn is_image(f: &std::path::Path) -> bool {
    matches!(
        f.extension().map(|e| e.to_string_lossy().to_lowercase()).as_deref(),
        Some("jpg" | "jpeg" | "png" | "webp")
    )
}

fn name_of(f: &std::path::Path) -> String {
    f.file_name().map(|n| n.to_string_lossy().to_lowercase()).unwrap_or_default()
}

/// Confronto "naturale": i numeri dentro i nomi si confrontano come numeri.
fn natural_cmp(a: &str, b: &str) -> std::cmp::Ordering {
    let (mut a, mut b) = (a.chars().peekable(), b.chars().peekable());
    loop {
        match (a.peek(), b.peek()) {
            (None, None) => return std::cmp::Ordering::Equal,
            (None, _) => return std::cmp::Ordering::Less,
            (_, None) => return std::cmp::Ordering::Greater,
            (Some(x), Some(y)) if x.is_ascii_digit() && y.is_ascii_digit() => {
                let mut na = String::new();
                while let Some(c) = a.peek().filter(|c| c.is_ascii_digit()) { na.push(*c); a.next(); }
                let mut nb = String::new();
                while let Some(c) = b.peek().filter(|c| c.is_ascii_digit()) { nb.push(*c); b.next(); }
                let (ta, tb) = (na.trim_start_matches('0'), nb.trim_start_matches('0'));
                let o = ta.len().cmp(&tb.len()).then_with(|| ta.cmp(tb));
                if o != std::cmp::Ordering::Equal { return o; }
            }
            (Some(x), Some(y)) => {
                let o = x.cmp(y);
                if o != std::cmp::Ordering::Equal { return o; }
                a.next(); b.next();
            }
        }
    }
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    // Windows / Linux: il file arriva come argomento ("Apri con…" o doppio clic).
    let args: Vec<String> = std::env::args()
        .skip(1)
        .filter(|a| !a.starts_with('-'))
        .collect();

    tauri::Builder::default()
        .plugin(tauri_plugin_dialog::init())
        .manage(Pending(Mutex::new(args)))
        .invoke_handler(tauri::generate_handler![take_pending, read_image, list_siblings])
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
