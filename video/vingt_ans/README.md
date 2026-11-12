# Faut-il passer 20 ans sur les bancs de l'école pour réussir ?

`vingt_ans_sur_les_bancs_1080p.mp4` — 2 min 09, 1080 × 1920, 30 i/s. Même style que
`../un_pied_a_l_ecole_1080p.mp4` : personnages animés, 24 scènes, sous-titres mot à mot.

- `voix_off.mp3` : voix off (voix Charon), copie de `../voix_off/voix_off_charon_naturelle.mp3`.
- `source/align.py` : cale chaque mot du script sur les pauses de la voix (`python3 align.py . 128.95`).
- `source/scenes.py` : les scènes ; `source/render.py` : sous-titres et rendu
  (`python3 render.py range 0 3870 sortie.mp4`, puis ajout de la voix avec ffmpeg).
- Prérequis : pycairo, ffmpeg, police Poppins.
