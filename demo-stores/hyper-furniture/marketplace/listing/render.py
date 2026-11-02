from PIL import Image, ImageDraw, ImageFont, ImageFilter
M='/tmp/hyper/media/'; F='/tmp/hyper/fontdl/inter/extras/ttf/'
W,H=3200,2400
INK=(22,23,15); LIME=(228,242,75); GREY=(243,243,238); LINE=(230,230,224); MUTED=(107,108,99)
def font(w,s): return ImageFont.truetype(F+f'Inter-{w}.ttf', s)
def wrap(d,text,f,maxw):
    words=text.split(); lines=[]; cur=''
    for w in words:
        t=(cur+' '+w).strip()
        if d.textlength(t,font=f)<=maxw: cur=t
        else: lines.append(cur); cur=w
    lines.append(cur); return lines
def text_block(d,xy,text,f,fill,maxw,lh,track=0):
    x,y=xy
    for ln in wrap(d,text,f,maxw):
        d.text((x,y),ln,font=f,fill=fill); y+=lh
    return y
def shadow(base,box,radius,blur=90,alpha=60,offset=60):
    sh=Image.new('RGBA',base.size,(0,0,0,0)); sd=ImageDraw.Draw(sh)
    x0,y0,x1,y1=box; sd.rounded_rectangle((x0+20,y0+offset,x1-20,y1+offset),radius=radius,fill=(22,23,15,alpha))
    sh=sh.filter(ImageFilter.GaussianBlur(blur)); base.alpha_composite(sh)
def browser(base,img,x,top,w=2720):
    shot=Image.open(M+img).convert('RGB'); h=int(w*shot.height/shot.width); bar=92
    box=(x,top,x+w,top+bar+h); shadow(base,box,44)
    layer=Image.new('RGBA',base.size,(0,0,0,0)); ld=ImageDraw.Draw(layer)
    ld.rounded_rectangle(box,radius=44,fill=(255,255,255,255))
    layer.paste(shot.resize((w,h),Image.LANCZOS),(x,top+bar))
    ld.rectangle((x,top,x+w,top+bar),fill=(251,251,248,255)); ld.line((x,top+bar,x+w,top+bar),fill=LINE,width=2)
    for i in range(3): ld.ellipse((x+40+i*44,top+33,x+66+i*44,top+59),fill=(218,218,211,255))
    mask=Image.new('L',base.size,0); ImageDraw.Draw(mask).rounded_rectangle(box,radius=44,fill=255)
    base.paste(layer,(0,0),mask)
    ImageDraw.Draw(base).rounded_rectangle(box,radius=44,outline=LINE,width=2)
def pill(d,x,y,text,f,bg,fg,border=None,padx=40,h=88):
    tw=d.textlength(text,font=f); d.rounded_rectangle((x,y,x+tw+2*padx,y+h),radius=h//2,fill=bg,outline=border,width=2 if border else 0)
    bb=f.getbbox(text); d.text((x+padx,y+(h-(bb[3]+bb[1]))/2),text,font=f,fill=fg); return x+tw+2*padx
def feature(name,eyebrow,title,sub,img,fw=2720):
    base=Image.new('RGBA',(W,H),GREY+(255,)); d=ImageDraw.Draw(base)
    fe=font('SemiBold',40); pill(d,240,192,eyebrow.upper(),fe,LIME,INK,padx=36,h=80)
    y=text_block(d,(236,330),title,font('SemiBold',128),INK,2720,138)
    y=text_block(d,(240,y+44),sub,font('Regular',52),MUTED,2300,76)
    top=max(860,y+80)
    if img=='PHONES':
        ph=Image.open('/tmp/hyper/c2-phones.png').convert('RGB')
        # crop the three phones from the 2x capture (backdrop is the same grey)
        crop=ph.crop((520,140,3320,2080)); cw=2600; ch=int(cw*crop.height/crop.width)
        base.paste(crop.resize((cw,ch),Image.LANCZOS),((W-cw)//2,top-40))
    else:
        browser(base,img,(W-fw)//2,top,fw)
    out=base.convert('RGB'); out.save(M+f'out/{name}@2x.jpg',quality=92); out.resize((1600,1200),Image.LANCZOS).save(M+f'out/{name}.png',optimize=True)
def cover():
    base=Image.new('RGBA',(W,H),INK+(255,)); d=ImageDraw.Draw(base)
    x=240; y=220
    for logo in ['framer.svg.png','shopify.svg.png']:
        d.rounded_rectangle((x,y,x+112,y+112),radius=32,fill=(255,255,255))
        lg=Image.open(M+logo).convert('RGBA').resize((64,64),Image.LANCZOS); base.alpha_composite(lg,(x+24,y+24)); x+=136
    fl=font('Medium',44); d.text((x+12,y+30),'Framer template  ·  Shopify store',font=fl,fill=(201,202,191))
    d.text((228,370),'WoodFurn',font=font('SemiBold',300),fill=(255,255,255))
    yy=text_block(d,(240,730),'A furniture store for Framer, connected to Shopify through the free Framerfy plugin.',font('Regular',64),(185,186,176),1900,92)
    fp=font('SemiBold',42); px=240; py=yy+50
    px=pill(d,px,py,'Free template',fp,LIME,INK)+24
    for t in ['Live cart','Test-mode checkout','Phone-ready']: px=pill(d,px,py,t,fp,INK,(255,255,255),border=(80,81,72))+24
    browser(base,'home.jpg',240,py+170)
    out=base.convert('RGB'); out.save(M+'out/01-cover@2x.jpg',quality=92); out.resize((1600,1200),Image.LANCZOS).save(M+'out/01-cover.png',optimize=True)
cover()
feature('02-products','Synced from Shopify','Products, variants and prices from your catalog','Size and assembly options change the price. Titles, images and descriptions come from Shopify, so the store follows your admin.','product.jpg')
feature('03-cart','Cart drawer','A cart drawer that works the day you publish','Quantities, subtotal, Checkout and Clear cart come wired up. Add to cart opens it from any product page.','drawer.jpg',fw=2000)
feature('04-checkout','Checkout','Try the checkout, then switch it to Shopify','Demo mode takes Stripe test cards, including a 3-D Secure step. One setting on the Checkout button sends shoppers to Shopify’s checkout.','checkout.jpg')
feature('05-collections','Collections','A shop page and six collections','Sofas, chairs, stools, tables, new and sale. Each page filters the synced catalog, and badges come from your Shopify tags.','shop.jpg')
feature('06-responsive','Responsive','Made for every screen','Every page has desktop, tablet and phone layouts, with a slide-in menu and a full-width cart on phones.','PHONES')
feature('07-orders','Orders','Order confirmation and order history','Each demo order shows the card used, the delivery address and the total. Shoppers find past orders under My orders.','confirmed.jpg')
feature('08-hero','Hero','A slideshow hero with three scenes','Autoplay, swipe and arrows. Swap in your own photos and headlines on the canvas.','slide3.jpg')
print('done')
