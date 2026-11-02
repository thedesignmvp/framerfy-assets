# Draw lime highlight boxes (CSS px of the 1470-wide window) on 2x window captures.
import sys, json
from PIL import Image, ImageDraw, ImageFont
F = "/tmp/hyper/fontdl/inter/extras/ttf/Inter-SemiBold.ttf"
LIME=(228,242,75); INK=(22,23,15)
spec = json.load(open(sys.argv[1]))
for name, cfg in spec.items():
    boxes = cfg['boxes'] if isinstance(cfg, dict) else cfg
    crop = cfg.get('crop') if isinstance(cfg, dict) else None
    src = Image.open(f"/tmp/hyper/g/{name}.png").convert("RGBA")
    bg = Image.new("RGBA", src.size, (17,17,17,255)); bg.alpha_composite(src); im = bg.convert("RGB")
    ox=oy=0
    if crop:
        im = im.crop(tuple(v*2 for v in crop)); ox, oy = crop[0], crop[1]
    from PIL import ImageFilter
    for bb in (cfg.get('blur',[]) if isinstance(cfg, dict) else []):
        r=tuple((v-o)*2 for v,o in zip(bb,(ox,oy,ox,oy))); im.paste(im.crop(r).filter(ImageFilter.GaussianBlur(14)), r[:2])
    d = ImageDraw.Draw(im)
    font = ImageFont.truetype(F, 30)
    for i, b in enumerate(boxes, 1):
        x0,y0,x1,y1 = [(v-o)*2 for v,o in zip(b[:4],(ox,oy,ox,oy))]
        for w in range(6):
            d.rounded_rectangle([x0-6-w, y0-6-w, x1+6+w, y1+6+w], radius=14+w, outline=LIME)
        if len(boxes) > 1:
            cx, cy = x0-6, y0-6
            d.ellipse([cx-24, cy-24, cx+24, cy+24], fill=LIME, outline=INK, width=3)
            t=str(i); tw=d.textlength(t,font=font); d.text((cx-tw/2, cy-19), t, fill=INK, font=font)
    im = im.resize((1520, round(im.height*1520/im.width)), Image.LANCZOS)
    im.save(f"/tmp/hyper/g/out/{name}.jpg", quality=88)
    print(name, im.size)
