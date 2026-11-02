from PIL import Image, ImageDraw
LIME=(228,242,75); INK=(22,23,15)
W,H=1520,954
WIN=[116,116,1620,962]
spec = {
 "v03-headless-install": ("t25", WIN, [[315,516,571,550]]),
 "v04-create-storefront": ("t31", None, [[772,527,965,566]]),
 "v05-storefront-api": ("t34", WIN, [[722,409,1186,448]]),
 "v06-store-domain": ("t86.5", WIN, [[132,396,288,420],[600,592,790,622]]),
 "v07-connect-new-store": ("t58", None, [[493,620,1009,709]]),
 "v08-create-store": ("t94", None, [[587,229,1293,605],[587,693,1293,761]]),
 "v09-select-store": ("t100", None, [[600,511,1108,639],[600,832,1108,876]]),
 "v10-import-fields": ("t120.5", WIN, [[352,164,378,190],[128,360,310,382],[738,330,998,616],[738,756,998,790]]),
}
from PIL import ImageFont
font = ImageFont.truetype("/tmp/hyper/fontdl/inter/extras/ttf/Inter-SemiBold.ttf", 26)
for name,(f,crop,boxes) in spec.items():
    im = Image.open(f"hi/{f}.png").convert("RGB")
    ox=oy=0
    if crop: im = im.crop(crop); ox,oy = crop[0],crop[1]
    d = ImageDraw.Draw(im)
    for i,b in enumerate(boxes,1):
        x0,y0,x1,y1 = b[0]-ox,b[1]-oy,b[2]-ox,b[3]-oy
        for w in range(4): d.rounded_rectangle([x0-5-w,y0-5-w,x1+5+w,y1+5+w], radius=10+w, outline=LIME)
        if len(boxes)>1:
            cx,cy=max(x0-5,24),max(y0-5,24); d.ellipse([cx-20,cy-20,cx+20,cy+20], fill=LIME, outline=INK, width=3)
            t=str(i); tw=d.textlength(t,font=font); d.text((cx-tw/2,cy-16),t,fill=INK,font=font)
    s = min(W/im.width, H/im.height); im2 = im.resize((round(im.width*s), round(im.height*s)), Image.LANCZOS)
    out = Image.new("RGB",(W,H),INK); out.paste(im2,((W-im2.width)//2,(H-im2.height)//2))
    out.save(f"/tmp/hyper/g/out/{name}.jpg", quality=88); print(name, im.size)
