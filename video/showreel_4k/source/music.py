"""Bande-son du showreel : synthèse 100 % numpy (120 BPM, 30 s, stéréo 48 kHz).
Usage : python3 music.py sortie.wav"""
import sys, wave
import numpy as np

SR = 48000; DUR = 30.0; N = int(SR * DUR); BEAT = 0.5
rs = np.random.RandomState(4)
L = np.zeros(N); R = np.zeros(N)          # bus sec
WL = np.zeros(N); WR = np.zeros(N)        # bus réverbération


def filt(x, lo=None, hi=None):
    """Filtre passe-bande par FFT, bords adoucis."""
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); g = np.ones_like(f)
    if lo: g *= 1 / (1 + (lo / np.maximum(f, 1e-6)) ** 6)
    if hi: g *= 1 / (1 + (f / hi) ** 6)
    return np.fft.irfft(X * g, len(x))


def add(sig, t0, gain=1.0, pan=0.0, wet=0.0):
    i = int(round(t0 * SR))
    if i >= N: return
    s = sig[:N - i] * gain
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    L[i:i + len(s)] += s * l; R[i:i + len(s)] += s * r
    if wet: WL[i:i + len(s)] += s * l * wet; WR[i:i + len(s)] += s * r * wet


def tt(d): return np.arange(int(d * SR)) / SR
def saw(f, t, det=0.0): return 2 * (((f * (1 + det)) * t) % 1.0) - 1


def kick():
    t = tt(.45); ph = 2 * np.pi * np.cumsum(44 + 120 * np.exp(-t / .028)) / SR
    return np.sin(ph) * np.exp(-t / .16) + .5 * rs.randn(len(t)) * np.exp(-t / .003)

def clap():
    t = tt(.3); n = filt(rs.randn(len(t)), 900, 7000)
    e = sum(np.exp(-np.maximum(t - d, 0) / .012) * (t >= d) for d in (0, .011, .023)) * .5 + np.exp(-t / .07) * (t >= .03)
    return n * e

def hat(dec=.03):
    t = tt(dec * 6); return filt(rs.randn(len(t)), 7500) * np.exp(-t / dec)

def bass(f, d):
    t = tt(d); s = filt(saw(f, t) + .6 * np.sin(2 * np.pi * f * t), None, 420)
    return s * np.minimum(t / .005, 1) * np.exp(-t / (d * .9))

def pluck(f, d=.35):
    t = tt(d); s = saw(f, t) * .6 + np.sign(np.sin(2 * np.pi * f * t)) * .25 + np.sin(4 * np.pi * f * t) * .3
    return filt(s, 150, 5200) * np.exp(-t / .09) * np.minimum(t / .002, 1)

def pad(fs, d):
    t = tt(d); s = np.zeros((2, len(t)))
    for f in fs:
        for k, det in enumerate((-.006, -.002, .003, .007)):
            s[k % 2] += saw(f, t + rs.rand(), det)
    e = np.minimum(t / .5, 1) * np.minimum((d - t) / .35, 1)
    return filt(s[0], 120, 1700) * e, filt(s[1], 120, 1700) * e

def riser(d, hp=1500):
    t = tt(d); u = t / d
    n = filt(rs.randn(len(t)), hp) * u ** 2.2
    sw = np.sin(2 * np.pi * np.cumsum(180 * 2 ** (u * 3.4)) / SR) * u ** 2 * .35
    return (n * .7 + sw) * np.minimum((d - t) / .01, 1)

def impact():
    t = tt(2.6); ph = 2 * np.pi * np.cumsum(34 + 60 * np.exp(-t / .09)) / SR
    return np.sin(ph) * np.exp(-t / .55) * 1.3 + filt(rs.randn(len(t)), 200, 9000) * np.exp(-t / .5) * .45

def whoosh(d=.7):
    t = tt(d); return filt(rs.randn(len(t)), 500, 6000) * np.exp(-((t - d / 2) ** 2) / (2 * (d / 6) ** 2))


A1, F1, C2, G1 = 55.0, 43.654, 65.406, 48.999
CH = {  # fondamentale de basse, accord (pad), notes d'arpège
    'Am': (A1, [220.0, 261.63, 329.63], [440.0, 523.25, 659.25, 880.0]),
    'F': (F1, [174.61, 220.0, 261.63], [349.23, 440.0, 523.25, 698.46]),
    'C': (C2, [196.0, 261.63, 329.63], [392.0, 523.25, 659.25, 783.99]),
    'G': (G1, [196.0, 246.94, 293.66], [392.0, 493.88, 587.33, 783.99]),
}
PROG = ['Am', 'F', 'C', 'G']
K, CL = kick(), clap()
duck = np.ones(N)                           # compression « sidechain » sur le kick

def do_kick(t, g=1.0):
    add(K, t, .95 * g)
    i = int(t * SR); n = int(.28 * SR); e = 1 - .7 * np.exp(-np.arange(n) / (.09 * SR))
    duck[i:i + n] = np.minimum(duck[i:i + n], e[:max(0, min(n, N - i))])

# ---- ouverture 0–4 s : nappe grave, deux montées, deux impacts
t = tt(4.2); add(np.sin(2 * np.pi * 55 * t) * np.minimum(t / 1.5, 1) * np.minimum((4.2 - t) / .2, 1), 0, .28)
pl, pr_ = pad(CH['Am'][1], 4.0)
PADL = np.zeros(N); PADR = np.zeros(N); fi = np.minimum(tt(4.0) / 2.5, 1) ** 2; PADL[:len(pl)] += pl * fi * .3; PADR[:len(pr_)] += pr_ * fi * .3
add(riser(1.5), .5, .16, wet=.3); add(impact(), 2.0, .9, wet=.5)
add(riser(1.6, 2500), 2.4, .2, wet=.3); add(impact(), 4.0, .8, wet=.4)
for k in range(8): add(pluck(880 * (1.5 if k % 2 else 1), .5), 2.0 + k * .25, .1, pan=(-1) ** k * .6, wet=.8)

# ---- corps 4–28 s
ARPL = np.zeros(N); ARPR = np.zeros(N)
for bar in range(12):
    t0 = 4 + bar * 2.0; root, chord, arp = CH[PROG[bar % 4]]
    sec = 'A' if t0 < 10 else 'B' if t0 < 16 else 'DROP' if t0 < 20 else 'BREAK' if t0 < 24 else 'END'
    pl, pr_ = pad(chord, 2.05); i = int(t0 * SR); g = .3 if sec == 'BREAK' else .42
    PADL[i:i + len(pl)] += pl[:N - i] * g; PADR[i:i + len(pr_)] += pr_[:N - i] * g
    for b in range(4):
        tb = t0 + b * BEAT
        if sec != 'BREAK':
            do_kick(tb)
            if b % 2 == 1 or sec == 'DROP': add(CL, tb, .5 if sec != 'DROP' or b % 2 else .28, wet=.35)
            add(hat(.11 if sec in ('DROP', 'END') else .035), tb + .25, .2, pan=.25)
        for s in range(4):                       # doubles-croches
            ts = tb + s * .125
            if sec in ('B', 'DROP', 'END') and s % 2: add(hat(.02), ts, .09, pan=-.3)
            if sec == 'BREAK' and s % 2 == 0: add(hat(.02), ts, .05, pan=.4)
            if sec == 'DROP': add(bass(root * (2 if s == 3 else 1), .12), ts, .5)
            elif sec != 'BREAK' and s % 2 == 0: add(bass(root * (2 if (b * 2 + s // 2) % 4 == 3 else 1), .24), ts, .5)
            if not (sec == 'A' and bar < 2):
                n = arp[(b * 4 + s) * 3 % 4] * (2 if sec == 'BREAK' and s % 2 else 1)
                p = pluck(n); j = int(ts * SR); ga = {'A': .13, 'B': .17, 'DROP': .2, 'BREAK': .11, 'END': .2}[sec]
                for rep, (dl, gg, pn) in enumerate(((0, 1, -.35), (.375, .45, .6), (.75, .22, -.6))):   # écho ping-pong
                    jj = j + int(dl * SR)
                    if jj < N:
                        m = min(len(p), N - jj); ARPL[jj:jj + m] += p[:m] * ga * gg * np.cos((pn + 1) * np.pi / 4); ARPR[jj:jj + m] += p[:m] * ga * gg * np.sin((pn + 1) * np.pi / 4)
    if sec == 'BREAK': add(np.sin(2 * np.pi * root * tt(2.0)) * np.minimum(tt(2.0) / .3, 1) * np.minimum((2.0 - tt(2.0)) / .3, 1), t0, .18)

# transitions et ponctuations calées sur le montage
add(whoosh(.75), 9.62, .55, pan=-.2, wet=.3); add(whoosh(.5), 10.05, .3, pan=.5)
for k in range(16): add(CL, 15.0 + k * .0625, .12 + .022 * k, wet=.2)             # roulement avant le drop
add(riser(1.9, 2000), 14.1, .2, wet=.3); add(impact(), 16.0, .85, wet=.4)
for k in range(8): add(hat(.006), 16 + k * .5, .5); add(whoosh(.22), 16 + k * .5 - .11, .22, pan=(-1) ** k * .7)
for k in range(6): add(K, 19.75 + k * .0417, .5)                                   # bégaiement final du drop
add(impact(), 20.0, .35, wet=.6); add(riser(1.8, 3000), 22.2, .2, wet=.4)
add(whoosh(.8), 23.35, .5, wet=.4); add(impact(), 24.0, .85, wet=.4)
add(riser(1.0, 3000), 27.0, .16, wet=.3)
# accord final à 28 s
add(impact(), 28.0, 1.0, wet=.7); pl, pr_ = pad(CH['Am'][1] + [110.0, 440.0], 2.0)
e = np.exp(-tt(2.0) / .7); i = int(28 * SR); PADL[i:i + len(pl)] += pl * e * .7; PADR[i:i + len(pr_)] += pr_ * e * .7
for k, f in enumerate((440.0, 659.25, 880.0, 1318.5)): add(pluck(f, .6), 28.0 + k * .06, .22, pan=(-1) ** k * .5, wet=1.0)

# mixage : sidechain, réverbération, limiteur doux
dk = duck; L += (PADL * .5 + ARPL) * dk; R += (PADR * .5 + ARPR) * dk
WL += (PADL * .25 + ARPL * .45) * dk; WR += (PADR * .25 + ARPR * .45) * dk
ir_t = tt(2.2); M = len(WL) + len(ir_t)
for bus, out in ((WL, L), (WR, R)):
    ir = filt(rs.randn(len(ir_t)), 250, 7000) * np.exp(-ir_t / .55); ir /= np.sqrt(np.sum(ir ** 2))
    out += np.fft.irfft(np.fft.rfft(bus, M) * np.fft.rfft(ir, M), M)[:N] * .3
mix = np.stack([L, R], 1)
mix = filt(mix[:, 0], 25), filt(mix[:, 1], 25); mix = np.stack(mix, 1)
mix = np.tanh(mix * 1.15 / np.percentile(np.abs(mix), 99.9)); mix *= .92 / np.abs(mix).max()
fade = np.minimum(1, (DUR - np.arange(N) / SR) / 1.2).clip(0, 1) ** 1.5; mix *= fade[:, None]
with wave.open(sys.argv[1], 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype('<i2').tobytes())
print('ok', sys.argv[1], 'crête', float(np.abs(mix).max()))
