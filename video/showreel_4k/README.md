# Showreel 4K

`showreel_4k_2160p60.mp4` — 30 s, 3840 × 2160, 60 i/s, H.264 High + AAC stéréo 48 kHz.

Tout est synthétisé, sans rush ni banque d'images ou de sons :

| Temps | Séquence | Ce qu'elle montre |
|---|---|---|
| 0–4 s | Ouverture | Titre tracé puis rempli, traversée du titre |
| 4–10 s | Motion design | Paysage synthwave en parallaxe, titrage, bandes cinéma |
| 10–16 s | Étalonnage | Volet avant / après, histogramme, panoramique filé en entrée |
| 16–20 s | Coupes au rythme | 8 plans calés sur le tempo (120 BPM) |
| 20–24 s | Définition | Traits d'un pixel et micro-texte sous une loupe ×4, sortie en iris |
| 24–30 s | Générique | Typographie animée, fiche technique |

- `source/reel.js` : les scènes et le montage (Canvas 2D, une fonction du temps par scène).
- `source/render.js` : rendu des 1 800 images dans Chromium.
- `source/music.py` : bande-son synthétisée avec numpy.
- `source/build.sh` : reconstruit la vidéo de bout en bout.
