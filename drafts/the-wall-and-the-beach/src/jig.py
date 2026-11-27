# A jigsaw cut from the owner's photograph: 6 by 4 pieces with real tabs and blanks, each kept as its own image with a soft bevel.
import numpy as np, json, os
from PIL import Image, ImageDraw, ImageFilter
S=os.path.dirname(os.path.abspath(__file__)); NX,NY=6,4; PW=PH=200; MAR=60
def build():
    src=Image.open(S+'/wall-soft.jpg').convert('RGB').crop((118,180,1318,980)).resize((NX*PW,NY*PH),Image.LANCZOS); rng=np.random.default_rng(5)
    hs=rng.choice([-1,1],(NY,NX-1)); vs=rng.choice([-1,1],(NY-1,NX)); out=[]
    for j in range(NY):
        for i in range(NX):
            m=Image.new('L',(PW+2*MAR,PH+2*MAR),0); d=ImageDraw.Draw(m); d.rectangle([MAR,MAR,MAR+PW,MAR+PH],fill=255); r=PW*.115
            def knob(cx,cy,sign,horizontal):
                # a tab pokes out (sign +1) or a blank is cut in (sign -1); neck then head
                dx,dy=(sign,0) if horizontal else (0,sign); nx_,ny_=cx+dx*r*.55,cy+dy*r*.55; hx,hy=cx+dx*r*1.55,cy+dy*r*1.55; f=255
                d.ellipse([hx-r,hy-r,hx+r,hy+r],fill=f); (d.rectangle([min(cx,nx_+dx*r)-0, cy-r*.55, max(cx,nx_+dx*r)+0, cy+r*.55],fill=f) if horizontal else d.rectangle([cx-r*.55,min(cy,ny_+dy*r),cx+r*.55,max(cy,ny_+dy*r)],fill=f))
            cut=Image.new('L',m.size,0); dc=ImageDraw.Draw(cut)
            def blank(cx,cy,sign,horizontal):
                dx,dy=(sign,0) if horizontal else (0,sign); hx,hy=cx+dx*r*1.55,cy+dy*r*1.55; nx_,ny_=cx+dx*r*.55,cy+dy*r*.55
                dc.ellipse([hx-r,hy-r,hx+r,hy+r],fill=255); (dc.rectangle([min(cx,nx_+dx*r),cy-r*.55,max(cx,nx_+dx*r),cy+r*.55],fill=255) if horizontal else dc.rectangle([cx-r*.55,min(cy,ny_+dy*r),cx+r*.55,max(cy,ny_+dy*r)],fill=255))
            midy=MAR+PH/2; midx=MAR+PW/2
            if i<NX-1: (knob(MAR+PW,midy,1,True) if hs[j,i]>0 else blank(MAR+PW,midy,-1,True))
            if i>0:    (knob(MAR,midy,-1,True) if hs[j,i-1]<0 else blank(MAR,midy,1,True))
            if j<NY-1: (knob(midx,MAR+PH,1,False) if vs[j,i]>0 else blank(midx,MAR+PH,-1,False))
            if j>0:    (knob(midx,MAR,-1,False) if vs[j-1,i]<0 else blank(midx,MAR,1,False))
            m=Image.fromarray(np.where(np.asarray(cut)>0,0,np.asarray(m)).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2)).point(lambda v: 255 if v>120 else 0).filter(ImageFilter.GaussianBlur(.8))
            tile=Image.new('RGB',m.size,(0,0,0)); x0=i*PW-MAR; y0=j*PH-MAR; big=Image.new('RGB',(NX*PW+2*MAR,NY*PH+2*MAR),(200,190,170)); big.paste(src,(MAR,MAR)); tile=big.crop((x0+MAR,y0+MAR,x0+MAR+m.size[0],y0+MAR+m.size[1]))
            # bevel: light from the upper left, shade to the lower right, from the mask's own edge
            a=np.asarray(m,np.float32)/255; bl=np.asarray(m.filter(ImageFilter.GaussianBlur(5)),np.float32)/255; gy,gx=np.gradient(bl); light=np.clip((-gx-gy)*9,-1,1)*a
            t=np.asarray(tile,np.float32); t=np.clip(t*(1+.28*light[:,:,None])+26*np.maximum(light,0)[:,:,None],0,255)
            p=Image.fromarray(t.astype(np.uint8)).convert('RGBA'); p.putalpha(m); out.append(p)
    return out
if __name__=='__main__':
    P=build(); os.makedirs(S+'/jig',exist_ok=True)
    for k,p in enumerate(P): p.save(f'{S}/jig/{k:02d}.png')
    sheet=Image.new('RGB',(NX*PW+200,NY*PH+200),(120,90,60)); [sheet.alpha_composite(p,(0,0)) if False else sheet.paste(p,(40+(k%NX)*(PW+22),40+(k//NX)*(PH+22)),p) for k,p in enumerate(P)]; sheet.resize((960,int(960*sheet.size[1]/sheet.size[0]))).save(S+'/jig_sheet.jpg',quality=85); print(len(P))
