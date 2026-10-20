// Prepara la cartella dist/ per l'app desktop partendo da web/viewer.html:
// three.js locale (niente internet), nessun font remoto, documento HTML completo.
import { readFileSync, writeFileSync, mkdirSync, copyFileSync } from "node:fs";

let html = readFileSync("web/viewer.html", "utf8");
html = html
  .replace(/<script src="https:\/\/cdnjs[^"]+three\.min\.js"><\/script>/, '<script src="vendor/three.min.js"></script>')
  .replace(/<link[^>]+fonts\.googleapis[^>]+>\n?/g, "")
  .replace(/<meta name="claude:[^>]+>\n?/g, "");

if (!html.includes('src="vendor/three.min.js"')) throw new Error("tag di three.js non trovato in viewer.html");

const doc = `<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
</head>
<body>
${html}
</body>
</html>
`;
mkdirSync("dist/vendor", { recursive: true });
writeFileSync("dist/index.html", doc);
copyFileSync("web/vendor/three.min.js", "dist/vendor/three.min.js");
console.log("dist/ pronta");
