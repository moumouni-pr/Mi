// Showreel 4K — moteur de rendu image par image (Canvas 2D, 3840x2160).
// Chaque scène est une fonction pure du temps : render(t) dessine l'image exacte de l'instant t.
const W = 3840, H = 2160, FPS = 60, DUR = 30;
const cv = document.getElementById('c'); cv.width = W; cv.height = H;
const ctx = cv.getContext('2d');
const mk = () => { const c = document.createElement('canvas'); c.width = W; c.height = H; return [c, c.getContext('2d')]; };
const [CA, GA] = mk(), [CB, GB] = mk(), [CT, GT] = mk();

// ---------------------------------------------------------------- outils
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const lerp = (a, b, t) => a + (b - a) * t;
const pr = (t, a, b) => clamp((t - a) / (b - a));
const eOut3 = x => 1 - Math.pow(1 - x, 3);
const eInOut = x => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
const eOutExpo = x => x >= 1 ? 1 : 1 - Math.pow(2, -10 * x);
const eInExpo = x => x <= 0 ? 0 : Math.pow(2, 10 * x - 10);
const eOutBack = x => { const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); };
const imp = (t, t0, amp, tau) => t >= t0 ? amp * Math.exp(-(t - t0) / tau) : 0;
function rng(seed) { return function () { seed |= 0; seed = seed + 0x6D2B79F5 | 0; let t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
function vnoise(x, seed = 0) { const i = Math.floor(x), f = x - i; const h = n => { const s = Math.sin(n * 127.1 + seed * 311.7) * 43758.5453; return s - Math.floor(s); }; const u = f * f * (3 - 2 * f); return lerp(h(i), h(i + 1), u); }
const fbm = (x, seed) => vnoise(x, seed) * .55 + vnoise(x * 2.1, seed + 3) * .28 + vnoise(x * 4.3, seed + 7) * .17;

// Espace logique 1920x1080, rendu réel 3840x2160 (tout est vectoriel).
function begin(g) { g.setTransform(2, 0, 0, 2, 0, 0); g.globalAlpha = 1; g.globalCompositeOperation = 'source-over'; g.shadowBlur = 0; g.shadowColor = 'transparent'; g.setLineDash([]); g.lineCap = 'butt'; g.lineJoin = 'miter'; }
function txt(g, s, x, y, o = {}) {
  const { size = 40, weight = 700, font = 'Inter', color = '#fff', align = 'left', base = 'alphabetic', ls = 0, alpha = 1 } = o;
  g.save(); g.font = `${weight} ${size}px "${font}"`; g.letterSpacing = ls + 'px'; g.textAlign = align; g.textBaseline = base;
  g.fillStyle = color; g.globalAlpha *= alpha; g.fillText(s, x, y); g.restore();
}
const MONO = 'JetBrains Mono', DISP = 'Inter Display';
const fmt = n => String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, ' ');

function lowerThird(g, t, dur, num, title, sub, acc, ink = '#fff', back = '0,0,0') {
  if (t < 0 || t > dur) return;
  const pin = eOutExpo(pr(t, 0, .7)), pout = eInOut(pr(t, dur - .45, dur));
  const x = 130, y = 790;
  g.save(); begin(g); g.globalAlpha = 1 - pout;
  const bk = g.createLinearGradient(0, 0, 1500, 0); bk.addColorStop(0, `rgba(${back},${.72 * pin})`); bk.addColorStop(.6, `rgba(${back},${.5 * pin})`); bk.addColorStop(1, `rgba(${back},0)`);
  g.fillStyle = bk; for (let yy = y - 90; yy < y + 250; yy += 4) { g.globalAlpha = (1 - pout) * Math.sin(Math.PI * (yy - y + 90) / 340) ** 1.2; g.fillRect(0, yy, 1500, 4); }
  g.globalAlpha = 1 - pout;
  g.fillStyle = acc; g.fillRect(x, y + 4, 6, 118 * pin);
  txt(g, num, x + 30, y + 22, { size: 20, weight: 500, font: MONO, color: acc, ls: 5, alpha: pin });
  g.save(); g.beginPath(); g.rect(x + 20, y + 30, 1500, 78); g.clip();
  txt(g, title, x + 28, y + 96 + (1 - eOutExpo(pr(t, .1, .9))) * 90, { size: 70, weight: 800, font: DISP, color: ink, ls: -1 });
  g.restore();
  txt(g, sub, x + 30, y + 138 + (1 - eOut3(pr(t, .45, 1.1))) * 14, { size: 25, weight: 400, color: ink, alpha: .82 * pr(t, .45, 1.1) });
  g.restore();
}

// ---------------------------------------------------------------- S0 · intro
const stars0 = (() => { const r = rng(7); return Array.from({ length: 520 }, () => ({ a: r() * 6.2832, d: .04 + r(), z: .3 + r() * 1.7, s: .5 + r() * 1.3, ph: r() * 6.28 })); })();
function S0(g, t) {
  begin(g); g.fillStyle = '#03040a'; g.fillRect(0, 0, 1920, 1080);
  const ga = .12 + .4 * pr(t, .8, 2.2);
  const gl = g.createRadialGradient(960, 520, 0, 960, 520, 950);
  gl.addColorStop(0, `rgba(96,56,230,${ga})`); gl.addColorStop(.45, `rgba(20,70,170,${ga * .45})`); gl.addColorStop(1, 'rgba(0,0,0,0)');
  g.fillStyle = gl; g.fillRect(0, 0, 1920, 1080);
  // champ d'étoiles avec accélération finale
  const wp = eInExpo(pr(t, 3.1, 4)), warp = 1 + t * .07 + wp * 2.5;
  g.lineCap = 'round';
  for (const s of stars0) {
    const d = ((s.d * warp * s.z) % 1.15) * 1150, d2 = d * (1 + .02 + wp * .35);
    const c = Math.cos(s.a), sn = Math.sin(s.a) * .62;
    g.globalAlpha = clamp(d / 260) * (.45 + .55 * Math.sin(t * 3 + s.ph) ** 2) * pr(t, 0, .7);
    g.strokeStyle = '#d5e8ff'; g.lineWidth = s.s * (1 + d / 900);
    g.beginPath(); g.moveTo(960 + c * d, 540 + sn * d); g.lineTo(960 + c * d2, 540 + sn * d2); g.stroke();
  }
  g.globalAlpha = 1;
  // trait de lumière
  const hp = pr(t, .3, 1.4);
  if (hp > 0 && t < 2.4) {
    const hx = lerp(-300, 2700, eInOut(hp));
    const lg = g.createLinearGradient(hx - 900, 0, hx, 0);
    lg.addColorStop(0, 'rgba(45,226,230,0)'); lg.addColorStop(.8, 'rgba(45,226,230,.8)'); lg.addColorStop(1, '#fff');
    g.strokeStyle = lg; g.lineWidth = 2.5; g.beginPath(); g.moveTo(hx - 900, 520); g.lineTo(hx, 520); g.stroke();
    g.globalAlpha = .25; g.lineWidth = 12; g.stroke(); g.globalAlpha = 1;
  }
  // « 4K »
  g.save();
  g.font = `900 580px "${DISP}"`; g.textAlign = 'center'; g.textBaseline = 'middle'; g.letterSpacing = '-10px';
  const cx = 960, cy = 510, tw = g.measureText('4K').width, w4 = g.measureText('4').width;
  const px = cx - tw / 2 + w4 + 580 * .135, py = cy;
  const zp = eInExpo(pr(t, 3.25, 4));
  const sc = (1 + .16 * (1 - eOutExpo(pr(t, 2, 2.7)))) * (1 + zp * 70);
  g.translate(px, py); g.scale(sc, sc); g.translate(-px, -py);
  const op = eInOut(pr(t, .8, 2.0));
  if (t >= 2) {
    const fg = g.createLinearGradient(cx - tw / 2, cy - 200, cx + tw / 2, cy + 200);
    fg.addColorStop(0, '#2de2e6'); fg.addColorStop(.5, '#f5f7ff'); fg.addColorStop(1, '#ff2a6d');
    if (zp < .05) { g.shadowColor = 'rgba(90,120,255,.55)'; g.shadowBlur = 140; }
    g.fillStyle = fg; g.fillText('4K', cx, cy); g.shadowBlur = 0; g.shadowColor = 'transparent';
  }
  if (op > 0 && zp < .3) {
    g.setLineDash([op * 2700, 2700]); g.lineWidth = 2.2; g.strokeStyle = t >= 2 ? 'rgba(255,255,255,.55)' : '#fff'; g.lineJoin = 'round';
    g.strokeText('4K', cx, cy);
  }
  g.restore();
  // sous-titre
  const fo = 1 - pr(t, 3.2, 3.5);
  if (t > 2.25 && fo > 0) {
    const s = '3840 × 2160', n = Math.ceil(s.length * pr(t, 2.25, 2.85));
    g.save(); g.globalAlpha = fo;
    txt(g, s.slice(0, n) + (n < s.length ? '▌' : ''), 960, 880, { size: 46, weight: 500, font: MONO, align: 'center', ls: 14 });
    const lw = 330 * eOutExpo(pr(t, 2.4, 3.2));
    g.fillStyle = 'rgba(255,255,255,.5)'; g.fillRect(960 - 290 - lw, 866, lw, 1.5); g.fillRect(960 + 290, 866, lw, 1.5);
    txt(g, fmt(8294400 * eOut3(pr(t, 2.45, 3.2))) + '  PIXELS PAR IMAGE', 960, 936, { size: 21, weight: 500, font: MONO, color: '#2de2e6', align: 'center', ls: 8 });
    g.restore();
  }
  const fl = t >= 2 ? .85 * Math.pow(1 - pr(t, 2, 2.4), 2) : 0;
  if (fl > 0) { g.fillStyle = `rgba(255,255,255,${fl})`; g.fillRect(0, 0, 1920, 1080); }
}

// ---------------------------------------------------------------- S1 · paysage synthwave
const stars1 = (() => { const r = rng(21); return Array.from({ length: 260 }, () => ({ x: r() * 2100 - 90, y: r() * 430 - 40, s: .4 + r() * 1.1, ph: r() * 6.28 })); })();
function S1(g, t) {
  begin(g);
  const HZ = 630, z = 1 + .09 * pr(t, -.5, 6.5);
  g.fillStyle = '#07021a'; g.fillRect(0, 0, 1920, 1080);
  g.translate(960, 600); g.scale(z, z); g.translate(-960, -600 + 8 * pr(t, 0, 6));
  const sky = g.createLinearGradient(0, -60, 0, HZ);
  sky.addColorStop(0, '#07021a'); sky.addColorStop(.42, '#1c0b48'); sky.addColorStop(.74, '#6b1b7c'); sky.addColorStop(.93, '#ff3d77'); sky.addColorStop(1, '#ffa24d');
  g.fillStyle = sky; g.fillRect(-200, -200, 2320, HZ + 200);
  for (const s of stars1) { g.globalAlpha = (.35 + .65 * Math.sin(t * 2.2 + s.ph) ** 2) * clamp(1 - s.y / 430); g.fillStyle = '#fff'; g.beginPath(); g.arc(s.x, s.y, s.s, 0, 6.2832); g.fill(); }
  g.globalAlpha = 1;
  // étoile filante
  const sp = pr(t, 2.3, 3.0);
  if (sp > 0 && sp < 1) {
    const x = lerp(1500, 1150, sp), y = lerp(70, 250, sp), lg = g.createLinearGradient(x + 170, y - 88, x, y);
    lg.addColorStop(0, 'rgba(255,255,255,0)'); lg.addColorStop(1, `rgba(255,255,255,${Math.sin(sp * Math.PI)})`);
    g.strokeStyle = lg; g.lineWidth = 2; g.beginPath(); g.moveTo(x + 170, y - 88); g.lineTo(x, y); g.stroke();
  }
  // soleil
  const sx = 960, sy = 430, R = 255;
  const halo = g.createRadialGradient(sx, sy, R * .8, sx, sy, R * 2.5);
  halo.addColorStop(0, 'rgba(255,80,130,.42)'); halo.addColorStop(1, 'rgba(255,80,130,0)');
  g.fillStyle = halo; g.fillRect(sx - 700, sy - 700, 1400, 1400);
  g.save(); g.beginPath(); g.arc(sx, sy, R, 0, 6.2832); g.clip();
  const sg = g.createLinearGradient(0, sy - R, 0, sy + R);
  sg.addColorStop(0, '#fff07a'); sg.addColorStop(.45, '#ff9a3c'); sg.addColorStop(1, '#ff2a6d');
  g.fillStyle = sg; g.fillRect(sx - R, sy - R, 2 * R, 2 * R);
  g.fillStyle = sky; const top = sy - 30, span = R + 40;
  for (let k = 0; k < 9; k++) { const u = ((k * span / 9 + t * 16) % span) / span; g.fillRect(sx - R, top + u * span, 2 * R, 2 + u * 22); }
  g.restore();
  // montagnes
  const layers = [{ h: 210, c: '#2b0f55', e: 'rgba(255,90,170,.55)', sp: 5, sd: 3, f: .0042 }, { h: 135, c: '#150733', e: 'rgba(45,226,230,.75)', sp: 13, sd: 11, f: .0065 }];
  for (const L of layers) {
    g.beginPath(); g.moveTo(-220, HZ + 2);
    for (let x = -220; x <= 2140; x += 5) {
      const env = .22 + .78 * Math.pow(clamp(Math.abs(x - 960) / 760), 1.4);
      g.lineTo(x, HZ - L.h * env * Math.pow(fbm((x + t * L.sp) * L.f + 40, L.sd), 1.25) * 1.5);
    }
    g.lineTo(2140, HZ + 2); g.closePath(); g.fillStyle = L.c; g.fill(); g.strokeStyle = L.e; g.lineWidth = 1.3; g.stroke();
  }
  // sol + grille en perspective
  const gr = g.createLinearGradient(0, HZ, 0, 1100); gr.addColorStop(0, '#1a0540'); gr.addColorStop(1, '#04010d');
  g.fillStyle = gr; g.fillRect(-220, HZ, 2360, 600);
  const grid = (lw, a) => {
    g.lineWidth = lw; g.beginPath();
    for (let i = -34; i <= 34; i++) { g.moveTo(960 + i * 9, HZ); g.lineTo(960 + i * 300, 1160); }
    g.strokeStyle = `rgba(255,50,170,${a})`; g.stroke();
    const ph = (t * 1.6) % 1;
    for (let k = 0; k < 30; k++) {
      const zz = k + 1 - ph, y = HZ + 520 / zz; if (y > 1160) continue;
      g.globalAlpha = clamp(1.25 - zz / 26); g.lineWidth = lw * (1 + 2.2 / zz);
      g.beginPath(); g.moveTo(-220, y); g.lineTo(2140, y); g.strokeStyle = `rgba(60,225,240,${a})`; g.stroke();
    }
    g.globalAlpha = 1;
  };
  grid(7, .1); grid(1.4, .9);
  const hz = g.createLinearGradient(0, HZ - 4, 0, HZ + 110); hz.addColorStop(0, 'rgba(255,150,120,.75)'); hz.addColorStop(.12, 'rgba(255,60,140,.4)'); hz.addColorStop(1, 'rgba(255,60,140,0)');
  g.fillStyle = hz; g.fillRect(-220, HZ - 4, 2360, 114);
  lowerThird(g, t - .9, 4.6, '01 — MOTION DESIGN', 'Un décor sans caméra', 'Soleil, reliefs et grille : chaque image est calculée par du code, sans aucun rush.', '#2de2e6');
}

// ---------------------------------------------------------------- S2 · étalonnage
const bokeh = (() => { const r = rng(33); return Array.from({ length: 42 }, () => ({ x: r() * 1920, y: r() * 1080, r: 18 + r() * 95, h: r() < .5 ? 22 + r() * 25 : 178 + r() * 25, v: 6 + r() * 22, ph: r() * 6.28 })); })();
function divX(t) {
  let x = lerp(1960, 1080, eInOut(pr(t, .5, 1.6)));
  x = lerp(x, 680, eInOut(pr(t, 2.1, 3.1))); x = lerp(x, 1240, eInOut(pr(t, 3.3, 4.2))); return lerp(x, -40, eInOut(pr(t, 4.6, 5.5)));
}
function S2(g, t) {
  begin(g);
  const bg = g.createLinearGradient(0, 0, 1920, 1080); bg.addColorStop(0, '#03181d'); bg.addColorStop(1, '#0a0612');
  g.fillStyle = bg; g.fillRect(0, 0, 1920, 1080);
  g.globalCompositeOperation = 'lighter'; g.lineCap = 'round';
  for (let i = 0; i < 58; i++) {
    const u = i / 57, warm = i % 3 === 0, hue = warm ? 24 + 16 * Math.sin(i * 1.7) : 186 + 22 * Math.sin(i * .7);
    g.beginPath();
    for (let x = -60; x <= 1980; x += 14) {
      const y = 540 + (u - .5) * 560 + 150 * Math.sin(x * .0028 + t * .55 + u * 5) + 72 * Math.sin(x * .0061 - t * .85 + i * 1.3) + 26 * Math.sin(x * .013 + t * 1.4 + i);
      x === -60 ? g.moveTo(x, y) : g.lineTo(x, y);
    }
    const wide = 3 + 30 * Math.abs(Math.sin(i * 2.1));
    g.strokeStyle = `hsla(${hue},95%,${warm ? 58 : 52}%,${warm ? .16 : .12})`; g.lineWidth = wide; g.stroke();
    g.strokeStyle = `hsla(${hue},100%,74%,.55)`; g.lineWidth = .7; g.stroke();
  }
  for (const b of bokeh) {
    const y = ((b.y - t * b.v) % 1240 + 1240) % 1240 - 80, x = b.x + 30 * Math.sin(t * .4 + b.ph), a = .05 + .05 * Math.sin(t * .9 + b.ph) ** 2;
    g.fillStyle = `hsla(${b.h},90%,60%,${a})`; g.beginPath(); g.arc(x, y, b.r, 0, 6.2832); g.fill();
    g.strokeStyle = `hsla(${b.h},90%,72%,${a * 1.6})`; g.lineWidth = 1.5; g.stroke();
  }
  g.globalCompositeOperation = 'source-over';
  const dx = divX(t), amt = clamp(1 - dx / 1920);
  if (dx > 0) { // côté « brut » : désaturé, contraste aplati
    g.save(); g.beginPath(); g.rect(0, 0, dx, 1080); g.clip();
    g.globalCompositeOperation = 'saturation'; g.globalAlpha = .86; g.fillStyle = '#808080'; g.fillRect(0, 0, 1920, 1080);
    g.globalCompositeOperation = 'source-over'; g.globalAlpha = .42; g.fillStyle = '#6f7478'; g.fillRect(0, 0, 1920, 1080);
    g.restore();
    if (dx < 1930) {
      g.fillStyle = '#fff'; g.fillRect(dx - 1, 0, 2, 1080);
      g.beginPath(); g.arc(dx, 540, 30, 0, 6.2832); g.fillStyle = '#fff'; g.fill();
      txt(g, '‹ ›', dx, 541, { size: 26, weight: 800, color: '#111', align: 'center', base: 'middle', ls: 2 });
    }
  }
  const pill = (s, x, al, a) => {
    if (a <= 0) return; g.save(); g.globalAlpha = a; g.font = `600 19px "${MONO}"`; g.letterSpacing = '5px';
    const w = g.measureText(s).width + 36, x0 = al === 'right' ? x - w : x;
    g.fillStyle = 'rgba(0,0,0,.55)'; g.beginPath(); g.roundRect(x0, 150, w, 42, 21); g.fill();
    g.strokeStyle = 'rgba(255,255,255,.5)'; g.lineWidth = 1; g.stroke(); g.fillStyle = '#fff'; g.textBaseline = 'middle'; g.fillText(s, x0 + 18, 172); g.restore();
  };
  pill('BRUT · LOG', dx - 26, 'right', clamp((dx - 260) / 120) * pr(t, .3, .8));
  pill('ÉTALONNÉ', dx + 26, 'left', clamp((1700 - dx) / 120) * clamp((dx + 30) / 60));
  // histogramme RVB
  const pa = pr(t, .6, 1.2) * (1 - pr(t, 5.5, 5.9));
  if (pa > 0) {
    g.save(); g.globalAlpha = pa; const X = 1480, Y = 215, PW = 310, PH = 150;
    g.fillStyle = 'rgba(0,0,0,.55)'; g.beginPath(); g.roundRect(X, Y, PW, PH + 34, 8); g.fill(); g.strokeStyle = 'rgba(255,255,255,.25)'; g.lineWidth = 1; g.stroke();
    txt(g, 'HISTOGRAMME RVB', X + 14, Y + 22, { size: 12, weight: 500, font: MONO, ls: 3, alpha: .8 });
    g.globalCompositeOperation = 'lighter';
    [['#ff3b3b', .62, 1.0], ['#35e06a', .5, .8], ['#3b7bff', .36, 1.25]].forEach(([c, mu, wd], k) => {
      g.beginPath(); g.moveTo(X + 10, Y + PH + 24);
      for (let i = 0; i <= 96; i++) {
        const u = i / 96, s1 = lerp(.07, .2 * wd, amt), m = lerp(.5, mu, amt);
        let v = Math.exp(-((u - m) ** 2) / (2 * s1 * s1)) * lerp(1, .6, amt) + amt * .5 * Math.exp(-((u - (k === 2 ? .12 : .9)) ** 2) / .004);
        v *= .82 + .18 * vnoise(i * .7 + t * 3, k);
        g.lineTo(X + 10 + u * (PW - 20), Y + PH + 24 - v * (PH - 20));
      }
      g.lineTo(X + PW - 10, Y + PH + 24); g.closePath(); g.fillStyle = c; g.globalAlpha = pa * .55; g.fill();
    });
    g.restore();
  }
  lowerThird(g, t - .7, 4.7, '02 — ÉTALONNAGE', 'Avant / après', 'Saturation, contraste et teinte : la même image, brute puis étalonnée.', '#ff9f1c');
}

// ---------------------------------------------------------------- S3 · coupes au rythme
const SHOTS = ['COUPE', 'RYTHME', 'ZOOM', 'FLASH', 'GLITCH', 'SPLIT', 'SPEED', 'DROP'];
const speedL = (() => { const r = rng(55); return Array.from({ length: 110 }, () => ({ y: r() * 1080, l: 160 + r() * 800, v: 2600 + r() * 5200, x: r() * 3000, w: .8 + r() * 3.2, c: r() < .3 })); })();
function bigWord(g, s, color, x = 960, y = 545, size = 310) { txt(g, s, x, y, { size, weight: 900, font: DISP, color, align: 'center', base: 'middle', ls: -6 }); }
function S3(g, t) {
  begin(g);
  const i = Math.min(7, Math.floor(t / .5)), lt = t - i * .5, w = SHOTS[i];
  g.fillStyle = '#000'; g.fillRect(0, 0, 1920, 1080);
  g.save();
  const z = 1 + .2 * (1 - eOutExpo(lt / .38)); g.translate(960, 540); g.scale(z, z); g.translate(-960, -540);
  if (i === 0) {
    g.fillStyle = '#ff2a6d'; g.fillRect(-200, -200, 2320, 1480);
    g.save(); g.translate(960, 540); g.rotate(-.35); g.fillStyle = '#d9124f';
    for (let k = -14; k < 14; k++) g.fillRect(k * 170 + (lt * 520) % 170, -1400, 70, 2800);
    g.restore();
    const off = 26 * eOutExpo(lt / .3);
    g.save(); g.beginPath(); g.rect(-200, -200, 2320, 745); g.clip(); bigWord(g, w, '#fff', 960 - off); g.restore();
    g.save(); g.beginPath(); g.rect(-200, 545, 2320, 900); g.clip(); bigWord(g, w, '#fff', 960 + off); g.restore();
    g.fillStyle = '#0a0a0a'; g.fillRect(-200, 542, 2320 * eOutExpo(lt / .25), 6);
  } else if (i === 1) {
    g.fillStyle = '#05060d'; g.fillRect(-200, -200, 2320, 1480);
    for (let k = 0; k < 16; k++) { const r = (k * 88 + lt * 640) % 1408; g.strokeStyle = `rgba(45,226,230,${.15 + .6 * (r / 1408)})`; g.lineWidth = 1.5 + r * .012; g.beginPath(); g.arc(960, 540, r, 0, 6.2832); g.stroke(); }
    for (let k = 0; k < 64; k++) { const h = 20 + 150 * Math.abs(Math.sin(k * 1.9 + Math.floor(t * 15) * 2.3)) * Math.abs(Math.sin(k * .12)); g.fillStyle = k % 2 ? '#2de2e6' : '#ff2a6d'; g.fillRect(160 + k * 25, 960 - h, 14, h); }
    bigWord(g, w, '#fff', 960, 520, 290);
  } else if (i === 2) {
    g.fillStyle = '#ffb703'; g.fillRect(-200, -200, 2320, 1480);
    g.save(); g.translate(960, 540); g.rotate(lt * .9); g.fillStyle = '#fb8500';
    for (let k = 0; k < 18; k++) { g.beginPath(); g.moveTo(0, 0); g.arc(0, 0, 1700, k * 6.2832 / 18, (k + .5) * 6.2832 / 18); g.closePath(); g.fill(); }
    g.restore();
    g.save(); const s = 1 + 2.4 * (1 - eOutExpo(lt / .3)); g.translate(960, 540); g.scale(s, s); g.translate(-960, -540); bigWord(g, w, '#0a0a0a'); g.restore();
  } else if (i === 3) {
    g.fillStyle = '#f4f1ea'; g.fillRect(-200, -200, 2320, 1480); g.fillStyle = '#111';
    for (let y = -6; y < 1100; y += 30) for (let x = -6; x < 1940; x += 30) {
      const d = Math.hypot(x - 960, y - 540), r = 13 * (.5 + .5 * Math.sin(d * .02 - lt * 12));
      if (r > .4) { g.beginPath(); g.arc(x, y, r, 0, 6.2832); g.fill(); }
    }
    g.fillStyle = '#111'; const bw = 1500 * eOutExpo(lt / .25); g.fillRect(960 - bw / 2, 385, bw, 320);
    bigWord(g, w, '#f4f1ea');
  } else if (i === 4) {
    g.fillStyle = '#08080a'; g.fillRect(-200, -200, 2320, 1480);
    g.fillStyle = 'rgba(255,255,255,.035)'; for (let y = 0; y < 1080; y += 4) g.fillRect(0, y, 1920, 1.5);
    const r = rng(900 + Math.floor(t * 15)), a = 10 + 34 * r();
    g.globalCompositeOperation = 'lighter'; bigWord(g, w, '#ff0040', 960 - a, 545 + 6 * (r() - .5)); bigWord(g, w, '#00ff9c', 960, 545); bigWord(g, w, '#2a5bff', 960 + a, 545 + 6 * (r() - .5));
    g.globalCompositeOperation = 'source-over';
  } else if (i === 5) {
    const cols = ['#7b2ff7', '#2de2e6', '#ff2a6d', '#ff9f1c'];
    for (let k = 0; k < 4; k++) {
      const p = eOutExpo(pr(lt, k * .035, .28 + k * .035)), dir = k % 2 ? 1 : -1;
      g.save(); g.beginPath(); g.rect(k * 480, 0, 480, 1080); g.clip();
      g.fillStyle = cols[k]; g.fillRect(k * 480, dir * (1 - p) * 1080, 480, 1080);
      bigWord(g, w, k % 2 ? '#0a0a0a' : '#fff', 960, 545 + dir * (40 + (1 - p) * 500), 330); g.restore();
    }
  } else if (i === 6) {
    g.fillStyle = '#0b132b'; g.fillRect(-200, -200, 2320, 1480); g.lineCap = 'round';
    for (const s of speedL) { const x = 2400 - ((s.x + t * s.v) % 3400); g.strokeStyle = s.c ? 'rgba(45,226,230,.8)' : 'rgba(255,255,255,.55)'; g.lineWidth = s.w; g.beginPath(); g.moveTo(x, s.y); g.lineTo(x + s.l, s.y); g.stroke(); }
    g.save(); g.translate(960, 545); g.transform(1, 0, -.28, 1, 0, 0); g.translate(-960, -545);
    const sl = 900 * (1 - eOutExpo(lt / .3));
    for (let k = 7; k >= 1; k--) { g.globalAlpha = .1; bigWord(g, w, '#2de2e6', 960 + sl + k * 34); }
    g.globalAlpha = 1; bigWord(g, w, '#fff', 960 + sl); g.restore();
  } else {
    g.fillStyle = '#7b2ff7'; g.fillRect(-200, -200, 2320, 1480); g.fillStyle = '#5a17c9';
    for (let y = 0; y < 8; y++) for (let x = 0; x < 13; x++) {
      g.save(); g.translate(x * 160, y * 160 - 20); g.rotate(eOutExpo(pr(lt, (x + y) * .012, .35 + (x + y) * .012)) * 1.5708 + .7854);
      g.fillRect(-46, -46, 92, 92); g.restore();
    }
    bigWord(g, w, '#fff', 960, lerp(-260, 545, eOutBack(pr(lt, 0, .3))));
  }
  g.restore();
  if (i === 7 && lt > .25 && Math.floor(lt * 30) % 2 === 1) { g.globalCompositeOperation = 'difference'; g.fillStyle = '#fff'; g.fillRect(0, 0, 1920, 1080); g.globalCompositeOperation = 'source-over'; }
  if (i === 4) { // tranches décalées
    const r = rng(300 + Math.floor(t * 15));
    g.setTransform(1, 0, 0, 1, 0, 0);
    for (let k = 0; k < 7; k++) { const y = Math.floor(r() * H), h = 20 + Math.floor(r() * 150), d = Math.floor((r() - .5) * 420); g.drawImage(g.canvas, 0, y, W, h, d, y, W, h); }
    begin(g);
  }
  const fl = .75 * Math.pow(1 - pr(lt, 0, .13), 2); if (fl > 0) { g.fillStyle = `rgba(255,255,255,${fl})`; g.fillRect(0, 0, 1920, 1080); }
  g.globalCompositeOperation = 'difference';
  txt(g, `PLAN 0${i + 1} / 08`, 960, 992, { size: 20, weight: 600, font: MONO, align: 'center', ls: 8 });
  for (let k = 0; k < 8; k++) { g.fillStyle = '#fff'; g.globalAlpha = k <= i ? 1 : .35; g.fillRect(960 - 190 + k * 48, 1010, 40, k === i ? 6 : 3); }
  g.globalAlpha = 1; g.globalCompositeOperation = 'source-over';
}

// ---------------------------------------------------------------- S4 · détail 4K (loupe)
const MICRO = ' 3840 × 2160 • 8 294 400 PIXELS • ULTRA HD •';
function plate(g, t) {
  const pg = g.createRadialGradient(1240, 520, 100, 1240, 520, 1350); pg.addColorStop(0, '#f6f2e9'); pg.addColorStop(1, '#e6e0d2');
  g.fillStyle = pg; g.fillRect(-100, -100, 2120, 1280);
  g.fillStyle = 'rgba(20,33,61,.32)';
  for (let y = 12; y < 1080; y += 12) for (let x = 12; x < 1920; x += 12) g.fillRect(x - .25, y - .25, .5, .5);
  g.save(); g.translate(1240, 520);
  const ring = (R0, A, n, K, col, m = 0, rot = 0) => {
    g.strokeStyle = col; g.lineWidth = .5;
    for (let k = 0; k < K; k++) {
      g.beginPath();
      for (let s = 0; s <= 900; s++) {
        const a = s / 900 * 6.2832, r = R0 + A * Math.sin(n * a + k * 6.2832 / K + rot) + m * Math.sin(3 * n * a - k * 6.2832 / K * 2);
        const x = Math.cos(a) * r, y = Math.sin(a) * r; s ? g.lineTo(x, y) : g.moveTo(x, y);
      }
      g.closePath(); g.stroke();
    }
  };
  ring(325, 52, 12, 30, 'rgba(20,33,61,.8)', 10, t * .35);
  ring(190, 46, 8, 22, 'rgba(214,40,40,.8)', 0, -t * .5);
  ring(96, 22, 5, 14, 'rgba(20,33,61,.8)', 5, t * .7);
  g.strokeStyle = 'rgba(20,33,61,.9)'; g.lineWidth = .5; g.beginPath();
  for (let k = 0; k < 720; k++) { const a = k / 720 * 6.2832, r2 = k % 10 ? 437 : 443; g.moveTo(Math.cos(a) * 430, Math.sin(a) * 430); g.lineTo(Math.cos(a) * r2, Math.sin(a) * r2); }
  g.stroke();
  g.font = `600 7px "${MONO}"`; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillStyle = '#14213d';
  const str = MICRO.repeat(10), n = str.length;
  for (let k = 0; k < n; k++) { g.save(); g.rotate(k / n * 6.2832 + t * .06); g.translate(0, -412); g.fillText(str[k], 0, 0); g.restore(); }
  g.fillStyle = '#f3efe6'; g.beginPath(); g.arc(0, 0, 58, 0, 6.2832); g.fill(); g.strokeStyle = '#14213d'; g.lineWidth = .8; g.stroke();
  txt(g, '4K', 0, 2, { size: 54, weight: 900, font: DISP, color: '#14213d', align: 'center', base: 'middle', ls: -1 });
  g.restore();
}
function S4(g, t, next) {
  begin(g); plate(g, t);
  const fl = .8 * Math.pow(1 - pr(t, 0, .3), 2); if (fl > 0) { g.fillStyle = `rgba(255,255,255,${fl})`; g.fillRect(0, 0, 1920, 1080); }
  lowerThird(g, t - .4, 2.9, '03 — DÉFINITION', 'Le détail au pixel près', 'Traits d\'un pixel, micro-texte de 7 px : grossi 4 fois, rien ne bave.', '#d62828', '#14213d', '243,239,230');
  const ip = eInExpo(pr(t, 3.35, 4)), pop = eOutBack(pr(t, .25, .8));
  const lx = 1240 + 330 * Math.cos(.95 * t + 2.5), ly = 455 + 200 * Math.sin(1.35 * t + .9), R = 185 * pop + ip * 2600;
  if (R <= 2) return;
  g.save(); g.shadowColor = 'rgba(0,0,0,.4)'; g.shadowBlur = 90; g.shadowOffsetY = 36; g.fillStyle = '#14213d';
  g.beginPath(); g.arc(lx, ly, R + 7, 0, 6.2832); g.fill(); g.restore();
  g.save(); g.beginPath(); g.arc(lx, ly, R, 0, 6.2832); g.clip();
  g.save(); g.translate(lx, ly); g.scale(4, 4); g.translate(-lx, -ly); plate(g, t); g.restore();
  const na = pr(t, 3.35, 3.7);
  if (na > 0 && next) { g.setTransform(1, 0, 0, 1, 0, 0); g.globalAlpha = na; g.drawImage(next, 0, 0); begin(g); }
  g.restore();
  if (ip < .9) {
    g.strokeStyle = '#14213d'; g.lineWidth = 7; g.beginPath(); g.arc(lx, ly, R + 3.5, 0, 6.2832); g.stroke();
    g.strokeStyle = 'rgba(255,255,255,.75)'; g.lineWidth = 1.2; g.beginPath(); g.arc(lx, ly, R - 1, 0, 6.2832); g.stroke();
    g.save(); g.globalAlpha = pop * (1 - pr(t, 3.3, 3.5)); g.fillStyle = '#d62828'; g.beginPath(); g.roundRect(lx + R * .62, ly + R * .72, 86, 40, 20); g.fill();
    txt(g, '×4', lx + R * .62 + 43, ly + R * .72 + 21, { size: 22, weight: 700, font: MONO, align: 'center', base: 'middle' }); g.restore();
  }
}

// ---------------------------------------------------------------- S5 · générique
const stars5 = (() => { const r = rng(77); return Array.from({ length: 200 }, () => ({ x: r() * 1920, y: r() * 1080, s: .4 + r() * 1.1, ph: r() * 6.28 })); })();
const CHIPS = ['3840 × 2160', '60 IMAGES / S', 'H.264 HIGH', 'AAC STÉRÉO 48 kHz', '1 800 IMAGES', '100 % CODE'];
function S5(g, t) {
  begin(g); g.fillStyle = '#04050b'; g.fillRect(0, 0, 1920, 1080);
  const z = 1 + .035 * pr(t, 0, 6); g.translate(960, 540); g.scale(z, z); g.translate(-960, -540);
  g.globalCompositeOperation = 'lighter';
  [[520, 420, 760, '123,47,247', .5, .31, 0], [1400, 620, 800, '255,42,109', .34, .23, 2], [980, 900, 700, '45,226,230', .26, .4, 4]].forEach(([x, y, r, c, a, sp, ph]) => {
    const X = x + 190 * Math.sin(t * sp + ph), Y = y + 120 * Math.cos(t * sp * 1.3 + ph), rg = g.createRadialGradient(X, Y, 0, X, Y, r);
    rg.addColorStop(0, `rgba(${c},${a})`); rg.addColorStop(1, `rgba(${c},0)`); g.fillStyle = rg; g.fillRect(-100, -100, 2120, 1280);
  });
  g.globalCompositeOperation = 'source-over';
  for (const s of stars5) { g.globalAlpha = .2 + .6 * Math.sin(t * 1.8 + s.ph) ** 2; g.fillStyle = '#fff'; g.beginPath(); g.arc(s.x, s.y, s.s, 0, 6.2832); g.fill(); }
  g.globalAlpha = 1;
  if (t >= 0) {
    g.save(); g.beginPath(); g.rect(0, 250, 1920, 80); g.clip();
    txt(g, 'MONTÉ  PAR', 975, 318 + (1 - eOutExpo(pr(t, 0, .6))) * 90, { size: 50, weight: 500, color: '#d6dcff', align: 'center', ls: 30 }); g.restore();
  }
  if (t >= .5) {
    g.save(); g.font = `900 330px "${DISP}"`; g.letterSpacing = '-6px'; g.textBaseline = 'middle'; g.textAlign = 'left';
    const word = 'CLAUDE', tw = g.measureText(word).width, x0 = 960 - tw / 2 + 3;
    const fg = g.createLinearGradient(x0, 0, x0 + tw, 0); fg.addColorStop(0, '#2de2e6'); fg.addColorStop(.5, '#f5f7ff'); fg.addColorStop(1, '#ff2a6d');
    g.fillStyle = fg; g.beginPath(); g.rect(0, 360, 1920, 330); g.clip();
    for (let k = 0; k < word.length; k++) {
      const p = eOutExpo(pr(t, .5 + k * .05, 1.15 + k * .05));
      g.fillText(word[k], x0 + g.measureText(word.slice(0, k)).width, 535 + (1 - p) * 340);
    }
    g.restore();
    const bw = 880 * eOutExpo(pr(t, 1, 1.8)), bg = g.createLinearGradient(960 - 440, 0, 960 + 440, 0); bg.addColorStop(0, '#2de2e6'); bg.addColorStop(1, '#ff2a6d');
    g.fillStyle = bg; g.fillRect(960 - bw / 2, 712, bw, 5);
  }
  // pastilles techniques
  g.save(); g.font = `500 21px "${MONO}"`; g.letterSpacing = '4px'; g.textBaseline = 'middle';
  const ws = CHIPS.map(s => g.measureText(s).width + 44);
  [[0, 1, 2], [3, 4, 5]].forEach((row, ri) => {
    let x = 960 - (row.reduce((a, k) => a + ws[k], 0) + 20 * (row.length - 1)) / 2;
    for (const k of row) {
      const p = pr(t, 2 + k * .25, 2.35 + k * .25);
      if (p > 0) {
        const s = eOutBack(p), cxk = x + ws[k] / 2, cyk = 800 + ri * 66;
        g.save(); g.translate(cxk, cyk); g.scale(s, s); g.translate(-cxk, -cyk); g.globalAlpha = clamp(p * 2);
        g.fillStyle = 'rgba(255,255,255,.07)'; g.beginPath(); g.roundRect(x, cyk - 24, ws[k], 48, 24); g.fill();
        g.strokeStyle = k === 5 ? '#2de2e6' : 'rgba(255,255,255,.55)'; g.lineWidth = 1.2; g.stroke();
        g.fillStyle = k === 5 ? '#2de2e6' : '#fff'; g.fillText(CHIPS[k], x + 22, cyk + 1); g.restore();
      }
      x += ws[k] + 20;
    }
  });
  g.restore();
  txt(g, 'Image, montage et bande-son : tout est synthétisé, rien n\'est filmé.', 960, 960, { size: 24, weight: 400, color: '#d6dcff', align: 'center', alpha: .85 * pr(t, 3.6, 4.2) });
  const fl = t >= 4 ? .7 * Math.pow(1 - pr(t, 4, 4.4), 2) : 0; if (fl > 0) { g.fillStyle = `rgba(255,255,255,${fl})`; g.fillRect(-100, -100, 2120, 1280); }
  const fo = eInOut(pr(t, 4.9, 5.85)); if (fo > 0) { g.fillStyle = `rgba(0,0,0,${fo})`; g.fillRect(-100, -100, 2120, 1280); }
}

// ---------------------------------------------------------------- montage
const NAMES = [[0, '00 OUVERTURE'], [4, '01 MOTION DESIGN'], [10, '02 ÉTALONNAGE'], [16, '03 COUPES AU RYTHME'], [20, '04 DÉFINITION'], [24, '05 GÉNÉRIQUE']];
function hud(g, t) {
  begin(g); g.globalCompositeOperation = 'difference'; g.globalAlpha = pr(t, .2, .8) * (1 - pr(t, 29, 29.6));
  const c = '#c9c9c9', f = Math.round(t * FPS), tc = `00:00:${String(Math.floor(f / FPS)).padStart(2, '0')}:${String(f % FPS).padStart(2, '0')}`;
  const o = { size: 17, weight: 500, font: MONO, color: c, ls: 4 };
  if (Math.floor(t * 2) % 2 === 0) { g.fillStyle = '#ff3b3b'; g.globalCompositeOperation = 'source-over'; g.beginPath(); g.arc(66, 53, 6, 0, 6.2832); g.fill(); g.globalCompositeOperation = 'difference'; }
  txt(g, 'SHOWREEL · UHD 4K', 84, 59, o); txt(g, 'TC ' + tc, 1860, 59, { ...o, align: 'right' });
  txt(g, '3840 × 2160 · 60P', 60, 1037, o);
  let nm = NAMES[0][1]; for (const [a, s] of NAMES) if (t >= a) nm = s; txt(g, nm, 1860, 1037, { ...o, align: 'right' });
  g.strokeStyle = c; g.lineWidth = 1.5; g.beginPath();
  for (const [x, y, sx, sy] of [[34, 30, 1, 1], [1886, 30, -1, 1], [34, 1050, 1, -1], [1886, 1050, -1, -1]]) { g.moveTo(x + 18 * sx, y); g.lineTo(x, y); g.lineTo(x, y + 18 * sy); }
  g.stroke(); g.globalAlpha = 1; g.globalCompositeOperation = 'source-over';
}
function render(t) {
  let ca = imp(t, 2, 16, .12) + imp(t, 4, 12, .12) + imp(t, 24, 12, .12) + imp(t, 28, 16, .15), vig = .5;
  if (t < 4) S0(GA, t);
  else if (t < 9.75) { S1(GA, t - 4); const fl = .9 * Math.pow(1 - pr(t, 4, 4.45), 2); if (fl > 0) { begin(GA); GA.fillStyle = `rgba(255,255,255,${fl})`; GA.fillRect(0, 0, 1920, 1080); } }
  else if (t < 10.25) { // panoramique filé
    S1(GB, t - 4); S2(GT, t - 10);
    const p = eInOut(pr(t, 9.75, 10.25)), blur = Math.sin(p * Math.PI) * 42;
    GA.setTransform(1, 0, 0, 1, 0, 0); GA.globalCompositeOperation = 'source-over';
    for (let k = 0; k < 25; k++) { const o = -p * W + (k - 12) * blur; GA.globalAlpha = 1 / (k + 1); GA.drawImage(CB, o, 0); GA.drawImage(CT, o + W, 0); }
    GA.globalAlpha = 1; ca += Math.sin(p * Math.PI) * 10;
  }
  else if (t < 16) {
    S2(GA, t - 10);
    if (t >= 15.7) { // décrochage numérique avant le drop
      const r = rng(Math.floor(t * 20)); GA.setTransform(1, 0, 0, 1, 0, 0);
      for (let k = 0; k < 10; k++) { const y = Math.floor(r() * H), h = 16 + Math.floor(r() * 220), d = Math.floor((r() - .5) * 900 * pr(t, 15.7, 16)); GA.drawImage(CA, 0, y, W, h, d, y, W, h); }
      ca += 26 * pr(t, 15.7, 16);
    }
  }
  else if (t < 20) { S3(GA, t - 16); ca += imp((t - 16) % .5, 0, 9, .06); vig = .22; }
  else if (t < 24) { const n = t >= 23.3; if (n) S5(GB, t - 24); S4(GA, t - 20, n ? CB : null); vig = lerp(.12, .5, pr(t, 23.5, 24)); }
  else S5(GA, t - 24);

  ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = 1; ctx.globalCompositeOperation = 'source-over';
  if (ca > .4) { // aberration chromatique : les trois canaux à des échelles légèrement différentes
    ctx.fillStyle = '#000'; ctx.fillRect(0, 0, W, H); ctx.globalCompositeOperation = 'lighter';
    [['#f00', 2 * ca], ['#0f0', ca], ['#00f', 0]].forEach(([c, e]) => {
      GT.setTransform(1, 0, 0, 1, 0, 0); GT.globalAlpha = 1; GT.globalCompositeOperation = 'copy'; GT.drawImage(CA, -e, -e * H / W, W + 2 * e, H + 2 * e * H / W);
      GT.globalCompositeOperation = 'multiply'; GT.fillStyle = c; GT.fillRect(0, 0, W, H); ctx.drawImage(CT, 0, 0);
    });
    ctx.globalCompositeOperation = 'source-over';
  } else ctx.drawImage(CA, 0, 0);
  begin(ctx);
  const vg = ctx.createRadialGradient(960, 540, 560, 960, 540, 1150); vg.addColorStop(0, 'rgba(0,0,0,0)'); vg.addColorStop(1, `rgba(0,0,0,${vig})`);
  ctx.fillStyle = vg; ctx.fillRect(0, 0, 1920, 1080);
  const bar = 92 * eOut3(pr(t, 4.1, 4.9)) * (1 - eInOut(pr(t, 15.4, 15.95)));
  if (bar > 0) { ctx.fillStyle = '#000'; ctx.fillRect(0, 0, 1920, bar); ctx.fillRect(0, 1080 - bar, 1920, bar); }
  hud(ctx, t);
}
window.render = render;
window.grab = (i, q) => { render(i / FPS); return cv.toDataURL('image/jpeg', q || .95).split(',')[1]; };
