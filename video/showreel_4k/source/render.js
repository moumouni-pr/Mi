// Usage : node render.js <dossier_sortie> <worker> <nb_workers> [liste d'images "12,45,..."]
// Rend les images 4K une par une dans Chromium et les écrit en JPEG.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const [out, wi = '0', wn = '1', list] = process.argv.slice(2);
  fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 960, height: 540 } });
  p.on('pageerror', e => { console.error('ERREUR PAGE', e); process.exit(1); });
  await p.goto('file://' + path.join(__dirname, 'index.html'));
  await p.evaluate(async () => { await Promise.all(['900 100px "Inter Display"', '800 100px "Inter Display"', '500 20px "JetBrains Mono"', '600 20px "JetBrains Mono"', '700 20px "JetBrains Mono"', '400 20px Inter', '500 20px Inter', '800 20px Inter'].map(f => document.fonts.load(f))); });
  const frames = list ? list.split(',').map(Number) : Array.from({ length: 1800 }, (_, i) => i).filter(i => i % +wn === +wi);
  const t0 = Date.now();
  for (const i of frames) {
    const f = path.join(out, `f_${String(i).padStart(5, '0')}.jpg`);
    if (!list && fs.existsSync(f)) continue;
    fs.writeFileSync(f, Buffer.from(await p.evaluate(i => window.grab(i, .95), i), 'base64'));
  }
  console.log(`worker ${wi}: ${frames.length} images en ${((Date.now() - t0) / 1000).toFixed(1)} s`);
  await b.close();
})();
