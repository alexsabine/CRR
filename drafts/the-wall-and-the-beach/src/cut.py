import json, os, subprocess, sys, textwrap
from PIL import Image, ImageDraw, ImageFont
S=os.path.dirname(os.path.abspath(__file__)); IT='/tmp/claude-0/-home-user/1edd5cc0-6987-5771-b57b-68d2ef3dbc39/scratchpad/clips/package/files/im-fell-english-latin-400-italic.woff'; FPS=24
TM=json.load(open(S+'/timing.json')); TOTAL=TM['total']; cues=TM['cues']; os.makedirs(S+'/subs',exist_ok=True)
def run(c):
    r=subprocess.run(c,capture_output=True)
    if r.returncode: print(' '.join(map(str,c))[:400]); print(r.stderr.decode()[-900:]); sys.exit(1)
def sub(text,out):
    im=Image.new('RGBA',(1280,720),(0,0,0,0)); d=ImageDraw.Draw(im)
    if text:
        f=ImageFont.truetype(IT,32); lines=textwrap.wrap(text,68); bh=34+38*len(lines); y0=720-bh
        d.rectangle([0,y0,1280,720],fill=(255,253,248,236)); d.line([0,y0,1280,y0],fill=(217,207,174,255),width=2)
        for q,l in enumerate(lines): w=d.textlength(l,font=f); d.text(((1280-w)/2,y0+14+38*q),l,font=f,fill=(20,32,42,255))
    im.save(out)
sub('',S+'/subs/blank.png'); L=[]; t=0
for q,(c0,c1,tx) in enumerate(cues):
    c0=round(c0*FPS)/FPS; c1=round((c1+.5)*FPS)/FPS
    if q+1<len(cues): c1=min(c1,round(cues[q+1][0]*FPS)/FPS)
    if c0>t: L.append((S+'/subs/blank.png',c0-t))
    sub(tx,f'{S}/subs/{q:02d}.png'); L.append((f'{S}/subs/{q:02d}.png',c1-c0)); t=c1
L.append((S+'/subs/blank.png',TOTAL-t+1)); open(S+'/subs.txt','w').write(''.join(f"file '{p}'\nduration {d:.4f}\n" for p,d in L)+f"file '{S}/subs/blank.png'\n")
af="[3:a]aformat=channel_layouts=stereo,asplit=2[v1][v2];[2:a]volume=0.46,equalizer=f=2600:t=q:w=0.9:g=-4[m];[m][v1]sidechaincompress=threshold=0.02:ratio=9:attack=25:release=900:makeup=1[duck];[duck][v2]amix=inputs=2:normalize=0:weights='1 1.9',loudnorm=I=-16:TP=-1.5[a]"
run(['ffmpeg','-v','error','-y','-framerate',str(FPS),'-i',S+'/frames/%05d.jpg','-f','concat','-safe','0','-i',S+'/subs.txt','-i',S+'/song.wav','-i',S+'/voice_m.wav','-filter_complex',f"[1:v]fps={FPS},format=rgba[s];[0:v][s]overlay=0:0:shortest=1,fade=in:st=0:d=1.5:color=0xfffdf8,fade=out:st={TOTAL-1.7:.2f}:d=1.6:color=0xfffdf8,format=yuv420p[o];"+af,'-map','[o]','-map','[a]','-c:v','libx264','-crf','20','-preset','slow','-c:a','aac','-b:a','160k','-ar','48000','-profile:v','high','-level','3.1','-movflags','+faststart','-t',str(TOTAL),S+'/the-wall-and-the-beach.mp4'])
run(['ffmpeg','-v','error','-y','-i',S+'/the-wall-and-the-beach.mp4','-vf','fps=1/14.2,scale=400:-1,tile=8x6','-frames:v','1',S+'/sheet.jpg'])
print('done',os.path.getsize(S+'/the-wall-and-the-beach.mp4'))
