# Pano Viewer

App leggera per Mac e Windows che apre panoramiche 360° e le rende navigabili: trascini per guardarti intorno, zoom con rotella o pinch, e dopo 3 secondi di inattività parte l'autorotate.

## Formati riconosciuti in automatico

| Proporzioni | Formato |
|---|---|
| 2:1 | Equirettangolare mono |
| 1:1 | Equirettangolare stereo sopra/sotto (sopra = occhio sinistro) |
| 4:1 | Equirettangolare stereo affiancato (sinistra = occhio sinistro) |
| 6:1 | Cubica in striscia orizzontale |
| 1:6 | Cubica in striscia verticale |
| 3:2 | Cubica 3×2 |
| 4:3 | Cubica a croce |
| 12:1 | Cubica stereo (6 facce occhio sinistro + 6 occhio destro) |
| 2:1 con due cerchi | Doppio fisheye (Samsung Gear 360, prime Insta360 e simili) |

Per le cubiche in striscia e 3×2 l'ordine predefinito delle facce è Destra, Sinistra, Sopra, Sotto, Fronte, Retro. Se un render usa un altro ordine, si cambia dal menu "Facce"; i pulsanti "↻ Cielo" e "↻ Pavimento" ruotano le facce superiore e inferiore.

Il doppio fisheye ha le stesse proporzioni di una equirettangolare: il viewer lo riconosce dagli angoli neri e dai due cerchi. Lo slider "Lente" regola l'angolo di campo (di solito 195°) per far sparire la cucitura; "Inverti" scambia lente anteriore e posteriore.

Limiti: equirettangolari fino a 12K per occhio (12288 px di larghezza), facce cubiche fino a 4096 px. Oltre, l'immagine viene ridotta solo per la visualizzazione. JPG, PNG e WebP.

Comandi: trascina per ruotare, rotella o pinch per lo zoom, doppio clic per avvicinare, +/− da tastiera, F per lo schermo intero.

## Scorrere le immagini di una cartella

Quando apri un'immagine, l'app carica anche tutte le altre della stessa cartella, in ordine di nome. Con **← →** (o i pulsanti ai lati, oppure Pagina su/giù) passi alla precedente o alla successiva; **Home** e **Fine** vanno alla prima e all'ultima. In alto vedi la posizione, per esempio "3 / 12". Se apri più file insieme, scorri solo quelli. Con una sola immagine, o tenendo premuto **Shift**, le frecce ruotano la vista.

## Aprire i file dal sistema

- **Mac:** tasto destro sull'immagine → Apri con → Pano Viewer. Funziona anche trascinando il file sull'icona nel Dock o dentro la finestra.
- **Windows:** tasto destro → Apri con → Pano Viewer (la prima volta: "Scegli un'altra app").

L'app si registra per JPG, PNG e WebP come visualizzatore, senza diventare il programma predefinito per tutte le foto.

## Compilare (gratis, su GitHub)

1. Crea un repository su GitHub e carica questa cartella.
2. Ogni push su `main` avvia la compilazione; si può avviare anche a mano da **Actions → Build app → Run workflow**.
3. Dopo circa 10–15 minuti, nella pagina del workflow, sotto **Artifacts** trovi:
   - `PanoViewer-mac` con il `.dmg` (Intel e Apple Silicon insieme)
   - `PanoViewer-windows` con l'installer `.exe` e il `.msi`

## Primo avvio senza certificati

L'app non è firmata, quindi il sistema avvisa al primo avvio. È normale.

- **Mac:** apri il `.dmg`, trascina l'app in Applicazioni. Al primo avvio: tasto destro sull'app → Apri → Apri. Se dice che l'app "è danneggiata", apri il Terminale e scrivi:
  `xattr -cr "/Applications/Pano Viewer.app"`
- **Windows:** se compare "Windows ha protetto il PC", clicca **Ulteriori informazioni → Esegui comunque**.

## Sviluppo in locale

Servono Node 18+ e Rust (`rustup`). Poi:

```
npm install
npm run dev      # apre l'app in modalità sviluppo
npm run build    # crea l'installer per il sistema in uso
```

Il visualizzatore vive in `web/viewer.html`; `scripts/build-frontend.mjs` lo prepara per l'app (three.js incluso, funziona offline).

`test/` contiene un generatore di immagini di prova per tutti i formati e un test che verifica che ogni formato mostri la stessa vista della equirettangolare di riferimento.
