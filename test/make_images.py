"""Genera immagini di test per tutti i formati, a partire da una equirettangolare di riferimento.
Convenzione direzioni (uguale al viewer): u -> lon = 2*pi*u, direzione (cos lon, y, sin lon); fronte = -x (centro immagine)."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os, sys

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
W, H = 2048, 1024

# riferimento asimmetrico: fasce colorate in longitudine, gradiente in latitudine, scritte
ref = Image.new("RGB", (W, H))
d = ImageDraw.Draw(ref)
cols = [(220,60,60),(240,160,40),(230,220,60),(80,200,90),(60,180,220),(70,90,220),(160,80,210),(220,90,170)]
for i, c in enumerate(cols):
    d.rectangle([i*W//8, 0, (i+1)*W//8, H], fill=c)
arr = np.asarray(ref).astype(np.float32)
lat = np.linspace(1, 0.25, H)[:, None, None]
arr = arr * lat
ref = Image.fromarray(arr.clip(0,255).astype(np.uint8))
d = ImageDraw.Draw(ref)
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
except Exception:
    font = ImageFont.load_default()
for i in range(16):
    d.text((i*W/16+20, H/2-30), "ABCDEFGHIJKLMNOP"[i], fill=(255,255,255), font=font)
for x in range(0, W, 64):
    d.line([(x,0),(x,H)], fill=(0,0,0), width=2)
for y in range(0, H, 64):
    d.line([(0,y),(W,y)], fill=(0,0,0), width=2)
d.ellipse([W*0.3, 60, W*0.36, 160], fill=(255,255,255))    # cielo
d.rectangle([W*0.62, H-170, W*0.7, H-80], fill=(0,0,0))     # pavimento
ref.save(f"{out}/eq.png")
R = np.asarray(ref).astype(np.float32)

def sample_eq(dirs):
    x, y, z = dirs[...,0], dirs[...,1], dirs[...,2]
    n = np.sqrt(x*x+y*y+z*z)
    u = (np.arctan2(z, x) / (2*np.pi)) % 1.0
    v = np.arccos(np.clip(y/n, -1, 1)) / np.pi
    px = np.clip((u*W).astype(int), 0, W-1)
    py = np.clip((v*H).astype(int), 0, H-1)
    return R[py, px]

FR = {  # faccia: (forward, right, up)
    'F': ((-1,0,0),(0,0,-1),(0,1,0)),
    'R': ((0,0,-1),(1,0,0),(0,1,0)),
    'B': ((1,0,0),(0,0,1),(0,1,0)),
    'L': ((0,0,1),(-1,0,0),(0,1,0)),
    'U': ((0,1,0),(0,0,-1),(1,0,0)),
    'D': ((0,-1,0),(0,0,-1),(-1,0,0)),
}
S = 512
def face(k):
    f, r, up = [np.array(v, np.float32) for v in FR[k]]
    s = (np.arange(S)+0.5)/S
    ss, tt = np.meshgrid(s, s)
    dirs = f + (2*ss-1)[...,None]*r + (1-2*tt)[...,None]*up
    return sample_eq(dirs).clip(0,255).astype(np.uint8)
faces = {k: face(k) for k in FR}

def strip(order, vertical=False):
    return np.concatenate([faces[k] for k in order], axis=0 if vertical else 1)
Image.fromarray(strip("RLUDFB")).save(f"{out}/cube-h.png")
Image.fromarray(strip("RLUDFB", True)).save(f"{out}/cube-v.png")
Image.fromarray(np.concatenate([strip("RLU"), strip("DFB")], axis=0)).save(f"{out}/cube-32.png")
cross = np.zeros((3*S, 4*S, 3), np.uint8)
for k, (cx, cy) in {'U':(1,0),'L':(0,1),'F':(1,1),'R':(2,1),'B':(3,1),'D':(1,2)}.items():
    cross[cy*S:(cy+1)*S, cx*S:(cx+1)*S] = faces[k]
Image.fromarray(cross).save(f"{out}/cube-x.png")
inv = {k: 255-v for k, v in faces.items()}
Image.fromarray(np.concatenate([strip("RLUDFB"), np.concatenate([inv[k] for k in "RLUDFB"], 1)], 1)).save(f"{out}/cube-st.png")
E = np.asarray(ref)
Image.fromarray(np.concatenate([E, 255-E], 0)).save(f"{out}/eq-tb.png")
Image.fromarray(np.concatenate([E, 255-E], 1)).save(f"{out}/eq-sbs.png")
print("ok")
