import sys, io, numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright

viewer, imgdir, three = sys.argv[1], sys.argv[2], sys.argv[3]
VIEWS = [(0,0,90),(90,10,90),(-150,-5,90),(40,70,90),(-60,-75,90),(180,0,60)]

def shoot(page):
    page.wait_for_timeout(250)
    return np.asarray(Image.open(io.BytesIO(page.locator("canvas").screenshot())).convert("RGB")).astype(np.float32)

def load(page, name):
    page.set_input_files("#file", f"{imgdir}/{name}.png")
    page.wait_for_function("document.getElementById('meta').textContent.includes('" + {"eq":"Equi 2:1"}.get(name, "") + "') && document.getElementById('busy').hidden")
    page.wait_for_timeout(300)

with sync_playwright() as p:
    b = p.chromium.launch(args=["--use-gl=angle","--use-angle=swiftshader","--enable-unsafe-swiftshader","--ignore-gpu-blocklist"])
    page = b.new_page(viewport={"width":800,"height":500})
    page.route("**/cdnjs.cloudflare.com/**", lambda r: r.fulfill(path=three, content_type="application/javascript"))
    page.route("**/fonts.googleapis.com/**", lambda r: r.abort())
    errs = []
    page.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    page.goto("file://" + viewer)
    page.wait_for_timeout(800)
    load(page, "eq")
    print("eq meta:", page.inner_text("#meta"))
    refs = []
    for v in VIEWS:
        page.evaluate(f"window.__pano.setView({v[0]},{v[1]},{v[2]})")
        refs.append(shoot(page))
    Image.fromarray(refs[0].astype(np.uint8)).save(f"{imgdir}/shot_eq.png")
    for name in ["eq-tb","eq-sbs","cube-h","cube-v","cube-32","cube-x","cube-st"]:
        page.set_input_files("#file", f"{imgdir}/{name}.png")
        page.wait_for_timeout(1200)
        page.wait_for_function("document.getElementById('busy').hidden")
        meta = page.inner_text("#meta")
        diffs = []
        for v, r in zip(VIEWS, refs):
            page.evaluate(f"window.__pano.setView({v[0]},{v[1]},{v[2]})")
            diffs.append(np.abs(shoot(page) - r).mean())
        line = f"{name:8s} [{meta}] diff occhio S: " + " ".join(f"{d:5.1f}" for d in diffs)
        if not page.locator("#eyeBtn").is_hidden():
            page.click("#eyeBtn"); page.wait_for_timeout(600)
            page.evaluate(f"window.__pano.setView({VIEWS[0][0]},{VIEWS[0][1]},{VIEWS[0][2]})")
            line += f" | occhio D vs S: {np.abs(shoot(page)-refs[0]).mean():5.1f}"
        print(line)
        if name == "cube-x":
            page.evaluate("window.__pano.setView(40,70,90)")
            Image.fromarray(shoot(page).astype(np.uint8)).save(f"{imgdir}/shot_cubex_up.png")
    print("errori console:", errs)
    b.close()
