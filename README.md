# Pano Viewer

A lightweight 360° panorama viewer for Mac and Windows. Open an image and look around: drag to pan, scroll or pinch to zoom, and after 3 seconds without input it starts rotating on its own. No account, no internet connection, about 10 MB installed.

*Leggi in italiano: [README.it.md](README.it.md)*

## Download

Get the latest installers from the [Releases page](../../releases/latest):

- **Mac** (Apple Silicon and Intel): `.dmg`
- **Windows**: `-setup.exe` (recommended) or `.msi`

## Supported formats

The format is detected automatically from the image proportions.

| Proportions | Format |
|---|---|
| 2:1 | Equirectangular, mono |
| 1:1 | Equirectangular stereo, top/bottom (top = left eye) |
| 4:1 | Equirectangular stereo, side by side (left half = left eye) |
| 6:1 | Cubemap, horizontal strip |
| 1:6 | Cubemap, vertical strip |
| 3:2 | Cubemap, 3×2 grid |
| 4:3 | Cubemap, cross |
| 12:1 | Stereo cubemap (6 faces left eye + 6 faces right eye) |
| 2:1 with two circles | Dual fisheye (Samsung Gear 360, early Insta360 and similar cameras) |

For stereo images, the **Eye L / Eye R** button switches between the two views.

For strip and 3×2 cubemaps the default face order is Right, Left, Up, Down, Front, Back. If a renderer uses a different order, change it from the **Faces** menu; the **↻ Sky** and **↻ Floor** buttons rotate the top and bottom faces.

Dual fisheye images have the same proportions as an equirectangular, so the viewer recognizes them by their black corners and two circles. The **Lens** slider sets the lens field of view (usually 195°) to hide the seam; **Swap** exchanges front and back lenses.

If the automatic choice is wrong, pick the format from the **Format** menu.

**Limits:** equirectangulars up to 12K per eye (12288 px wide), cubemap faces up to 4096 px. Larger images are downscaled for display only. JPG, PNG and WebP.

## Controls

| Action | How |
|---|---|
| Look around | Drag with mouse or finger |
| Zoom | Scroll wheel, pinch, `+` / `−`, or double-click |
| Next / previous image | `→` / `←`, Page Down / Page Up, or the side buttons |
| First / last image | Home / End |
| Rotate view with the keyboard | `Shift` + arrow keys |
| Fullscreen | `F` or the Fullscreen button |
| Autorotate on/off | Autorotate button |

## Browsing a folder

When you open an image, the app also loads every other image in the same folder, sorted by name (img2 comes before img10). Use `←` `→` to step through them; the counter at the top shows where you are, for example "3 / 12". If you open several files at once, you browse only those. With a single image, the arrow keys rotate the view.

## Opening files from your computer

- **Mac:** right-click the image → Open With → Pano Viewer. You can also drop files on the Dock icon or into the window.
- **Windows:** right-click → Open with → Pano Viewer (the first time, choose "Choose another app").

The app registers as a viewer for JPG, PNG and WebP without becoming the default app for all your photos.

## First launch (unsigned app)

The app is not signed with a paid developer certificate, so the system shows a warning the first time. This is expected.

- **Mac:** open the `.dmg` and drag Pano Viewer into Applications. On first launch, right-click the app → Open → Open. If macOS says the app "is damaged", open Terminal and run:
  ```
  xattr -cr "/Applications/Pano Viewer.app"
  ```
- **Windows:** if you see "Windows protected your PC", click **More info → Run anyway**.

## Building

Builds run for free on GitHub Actions:

- Every push to `main` builds the Mac and Windows installers; download them from **Actions → Build app → Artifacts**.
- Publishing a release builds the installers and attaches them to that release automatically.

To build locally you need Node 18+ and Rust (`rustup`):

```
npm install
npm run dev      # run the app in development mode
npm run build    # build the installer for your current system
```

The viewer lives in `web/viewer.html`; `scripts/build-frontend.mjs` prepares it for the app (three.js is bundled, so it works offline). `test/` contains a generator of sample images for every format and a check that each format renders the same view as the reference equirectangular.

Built with [Tauri](https://tauri.app) and [three.js](https://threejs.org).
