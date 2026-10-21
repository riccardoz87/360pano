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

Per le cubiche in striscia e 3×2 l'ordine predefinito delle facce è Destra, Sinistra, Sopra, Sotto, Fronte, Retro. Se un render usa un altro ordine, si cambia dal menu "Facce"; i pulsanti "↻ Cielo" e "↻ Pavimento" ruotano le facce superiore e inferiore.

Limiti: equirettangolari fino a 12K per occhio (12288 px di larghezza), facce cubiche fino a 4096 px. Oltre, l'immagine viene ridotta solo per la visualizzazione. JPG, PNG e WebP.

Comandi: trascina per ruotare, rotella o pinch per lo zoom, doppio clic per avvicinare, frecce e +/− da tastiera, F per lo schermo intero.

## Aprire i file dal sistema

- **Mac:** tasto destro sull'immagine → Apri con → Pano Viewer. Funziona anche trascinando il file sull'icona nel Dock o dentro la finestra.
- **Windows:** tasto destro → Apri con → Pano Viewer (la prima volta: "Scegli un'altra app").

L'app si registra per JPG, PNG e WebP come visualizzatore, senza diventare il programma predefinito per tutte le foto.

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
