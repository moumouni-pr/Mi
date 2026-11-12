import sys, wave, numpy as np
w = wave.open(sys.argv[1]); sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), '<i2').astype(np.float64) / 32768
KEEP = float(sys.argv[3]); hop = sr // 200                       # trames de 5 ms
n = len(x) // hop; db = 20 * np.log10(np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1)) + 1e-9)
quiet = db < db.max() - 42
out = []; i = 0; cut = 0; fade = int(.008 * sr)
segs = []; s = 0
while i < n:
    if quiet[i]:
        j = i
        while j < n and quiet[j]: j += 1
        if (j - i) * hop / sr > KEEP + .04 or i == 0 or j == n:
            k = 0 if (i == 0 or j == n) else KEEP
            a = i * hop + int(k * sr / 2); b = j * hop - int(k * sr / 2)
            segs.append((s, a)); s = b; cut += (b - a) / sr
        i = j
    else: i += 1
segs.append((s, len(x)))
for a, b in segs:
    seg = x[a:b].copy()
    if len(seg) > 2 * fade: seg[:fade] *= np.linspace(0, 1, fade); seg[-fade:] *= np.linspace(1, 0, fade)
    out.append(seg)
y = np.concatenate(out)
with wave.open(sys.argv[2], 'wb') as o: o.setnchannels(1); o.setsampwidth(2); o.setframerate(sr); o.writeframes((y * 32767).astype('<i2').tobytes())
print('coupes', len(segs) - 1, '| retiré %.1f s | durée %.1f s' % (cut, len(y) / sr))
