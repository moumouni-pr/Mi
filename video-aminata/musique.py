import numpy as np, soundfile as sf, sys
SR=44100; DUR=190.0; BPM=92; beat=60/BPM; bar=4*beat
N=int(SR*DUR); L=np.zeros(N); R=np.zeros(N)
def f(m): return 440*2**((m-69)/12)
def lp(x,a):  # one-pole lowpass
    y=np.empty_like(x); s=0.0
    for i in range(len(x)): s+=a*(x[i]-s); y[i]=s
    return y
def add(sig,t0,pan=0.0,g=1.0):
    i=int(t0*SR); j=min(N,i+len(sig))
    if i>=N: return
    L[i:j]+=sig[:j-i]*g*(1-pan)/1.0; R[i:j]+=sig[:j-i]*g*(1+pan)/1.0
def epiano(m,dur,vel=1.0):
    t=np.arange(int(dur*SR))/SR; fr=f(m)
    s=np.sin(2*np.pi*fr*t)+.35*np.sin(2*np.pi*2*fr*t)*np.exp(-t*3)+.12*np.sin(2*np.pi*3*fr*t)*np.exp(-t*5)
    env=np.exp(-t*2.2)*np.minimum(1,t/0.005); env[-200:]*=np.linspace(1,0,200)
    return s*env*vel
def pad(ms,dur):
    t=np.arange(int(dur*SR))/SR; s=np.zeros_like(t)
    for m in ms:
        for d in (-0.08,0.08):
            ph=(f(m)*(1+d/100)*t)%1; s+=(2*ph-1)
    s=lp(s/len(ms),0.035)
    env=np.minimum(1,t/0.6)*np.minimum(1,(dur-t)/0.6); return s*env
def bass(m,dur):
    t=np.arange(int(dur*SR))/SR; s=np.sin(2*np.pi*f(m)*t)+.2*np.sin(2*np.pi*2*f(m)*t)
    env=np.minimum(1,t/0.01)*np.exp(-t*1.2); env[-300:]*=np.linspace(1,0,300); return s*env
def kick():
    t=np.arange(int(.3*SR))/SR; fr=50+90*np.exp(-t*30); return np.sin(2*np.pi*np.cumsum(fr)/SR)*np.exp(-t*12)
rng=np.random.default_rng(1)
def shaker():
    t=np.arange(int(.08*SR))/SR; n=rng.standard_normal(len(t)); n=n-lp(n,0.3); return n*np.exp(-t*60)
# chords (root midi, triad notes)
C=(48,[60,64,67]); G=(43,[59,62,67]); Am=(45,[60,64,69]); F=(41,[60,65,69]); Em=(40,[59,64,67]); Dm=(38,[57,62,65])
happy=[C,G,Am,F]; sad=[Am,F,Dm,Em]; hope=[F,G,C,Am]
t=0.0; b=0
while t<DUR:
    if t<43: prog,mode=hope,"full"
    elif t<104.5: prog,mode=sad,"soft"
    elif t<150: prog,mode=hope,"full"
    else: prog,mode=happy,'full'
    root,tri=prog[b%4]
    add(pad([n-12 for n in tri]+[tri[0]],bar+0.6),t,0,0.10 if mode=='full' else 0.13)
    add(bass(root,bar*0.95),t,0,0.20 if mode=='full' else 0.12)
    arp=[tri[0],tri[1],tri[2],tri[1]+12,tri[2],tri[1],tri[0]+12,tri[2]]
    for k in range(8):
        if mode=='soft' and k%2: continue
        add(epiano(arp[k],beat*1.6,0.8 if k%4==0 else 0.55),t+k*beat/2,(-0.3 if k%2 else 0.3),0.11)
    if mode=='full':
        for k in range(4): add(kick(),t+k*beat,0,0.22 if k%2==0 else 0.10)
        for k in range(8): add(shaker(),t+k*beat/2+beat/4,0.2,0.05)
    t+=bar; b+=1
mix=np.stack([L,R],1)
fade=np.ones(N); fi=int(1.5*SR); fo=int(4*SR); fade[:fi]=np.linspace(0,1,fi); fade[-fo:]=np.linspace(1,0,fo)
mix*=fade[:,None]; mix/=np.abs(mix).max()*1.12
sf.write(sys.argv[1],mix.astype(np.float32),SR)
