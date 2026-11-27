import json, wave, subprocess, numpy as np
from piper import PiperVoice, SynthesisConfig
P='/tmp/claude-0/x/piper/'; v=PiperVoice.load(P+'en_GB-vctk-medium.onnx',P+'en_GB-vctk-medium.onnx.json'); SID=json.load(open(P+'en_GB-vctk-medium.onnx.json'))['speaker_id_map']['p288']; SR=22050
BPM=72; BT=60/BPM; BAR=4*BT
REP=[('’',"'"),('Urizen','Yoo-rizen'),('Golgonooza','Golgo-nooza'),('autopoiesis','auto-poy-eesis'),('autopoietic','auto-poy-ettic'),('Sympoiesis','Sim-poy-eesis'),('sympoiesis','sim-poy-eesis'),('Maturana','Matoo-rahna'),('Varela','Varella'),('Winnicott','Winnicot'),('Los ','Loss '),('I. J. Good','I. J. Good'),('1965','nineteen sixty five'),('1998','nineteen ninety eight'),('builded','bilded'),('chartered','charterd'),('Visscher','Fisher'),('Kierkegaard','Keerkegard'),('Goodhart','Good-heart'),('Le Guin','Luh Gwin'),('re-member','ree-member'),('Murdock','Murdock'),('Nietzsche','Neecha'),('1874','eighteen seventy-four'),('Chesterton','Chesterton'),('Schön','Shern'),('Ram Dass','Rahm Dahss'),('reflection-in-action','reflection in action'),('reflection-on-action','reflection on action')]
def say(t):
    for a,b in REP: t=t.replace(a,b)
    a=np.concatenate([c.audio_int16_array for c in v.synthesize(t,syn_config=SynthesisConfig(speaker_id=SID,length_scale=1.16))]).astype(np.float32)/32768
    nz=np.nonzero(np.abs(a)>.004)[0]; return a[max(0,nz[0]-400):nz[-1]+1200]
up=lambda t,g: np.ceil(t/g-1e-6)*g
N=json.load(open('script.json')); clips=[]; cues=[]; secs=[]; t=0.
for pi,ch in enumerate(N):
    for i,s in enumerate(ch['text']):
        a=say(s); d=len(a)/SR; nw=len(s.split())
        if pi==0 and i==0: st=up(1.2*BAR,BAR)
        elif i==0: st=up(t+1.9,BAR)
        else: st=up(t+pause,2*BT)
        if i==0: p0=st
        clips.append((st,a)); cues.append([round(float(st),2),round(float(st+d),2),s]); t=st+d; pause=min(1.7,.45+.05*nw)
    secs.append([ch['id'],round(float(p0),2),round(float(t),2)])
total=float(up(t+7.5,BAR)); wav=np.zeros(int(total*SR),np.float32)
for st,a in clips: i=int(st*SR); wav[i:i+len(a)]+=a
w=wave.open('voice.wav','wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(wav,-1,1)*32767).astype(np.int16).tobytes()); w.close()
subprocess.run(['ffmpeg','-y','-loglevel','error','-i','voice.wav','-af','asetrate=22050*0.945,aresample=44100,atempo=1/0.945,bass=g=2.5:f=180,equalizer=f=3000:t=q:w=1.2:g=2.5,treble=g=-1:f=7000,acompressor=threshold=-22dB:ratio=3:attack=6:release=120:makeup=3,aecho=0.85:0.5:24|41:0.07|0.04,loudnorm=I=-16:TP=-1.5','-ar','44100','-ac','1','voice_m.wav'],check=True)
json.dump({'total':round(total,2),'cues':cues,'secs':secs,'strikes':[],'bpm':BPM},open('timing.json','w'),ensure_ascii=False); print(round(total,1)); print(secs)
