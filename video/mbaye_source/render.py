import sys, os, subprocess, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import *
from icons import GREEN, BLUE, CORAL, PURPLE, ORANGE, RED, NAVY
import scenes

DUR = 192.6
KEY = {
    'mbaye': ORANGE, 'abandonner': RED, 'difficile': RED, 'difficiles': RED, 'business': GREEN, 'master': PURPLE,
    'marketing': BLUE, 'digital': BLUE, 'entrepreneur': GREEN, 'chomeur': RED, 'emploi': PURPLE, 'projet': GREEN,
    'marque': ORANGE, 'vetements': BLUE, 'chaussures': ORANGE, 'casques': PURPLE, 'baskets': CORAL,
    'reussir': GREEN, 'positifs': GREEN, "l'ampleur": GREEN, 'ampleur': GREEN, 'bascule': RED, 'politique': PURPLE,
    'international': BLUE, "s'impatienter": RED, 'emprunter': ORANGE, 'millions': GREEN, 'erreur': RED,
    'maritime': BLUE, 'geopolitique': PURPLE, 'resultat': PURPLE, 'an': RED, 'catastrophe': RED, 'mode': ORANGE,
    'annulees': RED, 'stock': ORANGE, 'dette': RED, 'vente': RED, 'perdu': RED, 'tiktok': CORAL,
    'opportunite': GREEN, 'nigerien': ORANGE, 'nigeriens': ORANGE, 'interessants': GREEN, 'baissee': RED,
    'marche': BLUE, 'transport': BLUE, 'risques': ORANGE, 'previsionnel': PURPLE, 'transporteurs': BLUE,
    'grossistes': PURPLE, 'avance': GREEN, "d'exportation": ORANGE, 'echec': RED, 'aventure': GREEN,
    'entrepreneuriale': GREEN, 'exportateur': ORANGE, "l'international": BLUE, 'forcement': GREEN,
    'produit': CORAL, 'strategie': PURPLE, 'erreurs': RED, "s'adapter": PURPLE, 'opportunites': GREEN,
}

# ---------------------------------------------------------------- pages
def build_pages():
    sents = []; cur = []
    for i, w in enumerate(WORDS):
        cur.append(i)
        if re.search(r'[.!?]$', w['w'].strip()) or i == len(WORDS) - 1:
            sents.append(cur); cur = []
    # merge very short sentence into the following one
    merged = []
    carry = []
    for st in sents:
        st = carry + st; carry = []
        if sum(len(WORDS[j]['w']) + 1 for j in st) < 18 and st[-1] != len(WORDS) - 1 and merged:
            carry = st; continue
        merged.append(st)
    pages = []
    for st in merged:
        L = sum(len(WORDS[j]['w']) + 1 for j in st)
        k = max(1, math.ceil(L / 92))
        if k == 1: pages.append(st); continue
        # choose k-1 cut points near equal length, prefer commas
        cum = []; c = 0
        for j in st: c += len(WORDS[j]['w']) + 1; cum.append(c)
        cuts = []
        for m in range(1, k):
            target = L * m / k
            best = None; bs = 1e9
            for pos in range(1, len(st)):
                score = abs(cum[pos - 1] - target)
                if re.search(r'[,:;]$', WORDS[st[pos - 1]]['w'].strip()): score -= 18
                if score < bs and (not cuts or pos > cuts[-1] + 2): bs = score; best = pos
            cuts.append(best)
        prev = 0
        for ct in cuts + [len(st)]:
            pages.append(st[prev:ct]); prev = ct
    return pages

PAGES = build_pages()
SIZE = 54; LH = 74; CW = 960; PADX = 46; PADY = 34; CX0 = 60; CY0 = 110

_layout_cache = {}
def layout(ctx, pi):
    if pi in _layout_cache: return _layout_cache[pi]
    font(ctx, SIZE, 'bold')
    sp = text_w(ctx, ' ')
    maxw = CW - 2 * PADX
    lines = [[]]; x = 0
    for wi in PAGES[pi]:
        s = WORDS[wi]['w']
        w = text_w(ctx, s)
        if x > 0 and x + w > maxw:
            lines.append([]); x = 0
        lines[-1].append((wi, x, w)); x += w + sp
    # center each line
    out = []
    for li, ln in enumerate(lines):
        tot = ln[-1][1] + ln[-1][2]
        off = (maxw - tot) / 2
        for (wi, x, w) in ln:
            out.append((wi, CX0 + PADX + off + x, CY0 + PADY + SIZE * 0.95 + li * LH))
    h = PADY * 2 + len(lines) * LH - (LH - SIZE * 1.15)
    _layout_cache[pi] = (out, h)
    return out[:], h

PSTART = [WORDS[p[0]]['s'] - 0.12 for p in PAGES]

def draw_captions(ctx, T):
    pi = -1
    for i, s in enumerate(PSTART):
        if T >= s: pi = i
    if pi < 0: return
    # hide during title scenes (big title is on screen)
    first = PAGES[pi][0]; last = PAGES[-1][0]
    if pi == 0: return
    if T > 190.25: return
    items, h = layout(ctx, pi)
    # card height eases from previous page
    ph = layout(ctx, pi - 1)[1] if pi > 1 else h
    k = ease_out(prog(T, PSTART[pi], 0.25))
    hh = lerp(ph, h, k)
    a_card = 1.0
    if pi == 1:
        a_card = ease_out(prog(T, PSTART[1], 0.3))
    a_card *= 1 - prog(T, 190.0, 0.25)
    def draw():
        shadow(ctx, CX0, CY0, CW, hh, 40, a=0.16, off=12)
        fill_rrect(ctx, CX0, CY0, CW, hh, 40, '#FFFFFF', 0.96)
        font(ctx, SIZE, 'bold')
        for (wi, x, y) in items:
            w = WORDS[wi]
            p = prog(T, w['s'] - 0.06, 0.22)
            if p <= 0: continue
            nk = norm(w['w'])
            c = KEY.get(nk, NAVY)
            a = ease_out(p)
            dy = (1 - ease_out(p)) * 22
            ctx.move_to(x, y + dy); col(ctx, c, a); ctx.show_text(w['w'])
            if nk in KEY and p > 0:
                # underline swoosh
                ul = ease_out(prog(T, w['s'] + 0.05, 0.3))
                ww = text_w(ctx, w['w'].rstrip(' ,.!?:;'))
                line(ctx, x, y + 14, x + ww * ul, y + 14, 6, c, 0.35 * a)
    with_alpha(ctx, a_card, draw)

# ---------------------------------------------------------------- frames
STARTS = scenes.scene_starts()
XF = 0.32

def render_frame(ctx, T):
    k = 0
    for i, (s, fn) in enumerate(STARTS):
        if T >= s: k = i
    s, fn = STARTS[k]
    def draw_scene(idx):
        ss, ff = STARTS[idx]
        # gentle camera push-in
        nxt = STARTS[idx + 1][0] if idx + 1 < len(STARTS) else DUR
        z = 1.0 + 0.035 * ease_io(prog(T, ss, max(1.0, nxt - ss)))
        ctx.save()
        ctx.translate(W / 2, H * 0.6); ctx.scale(z, z); ctx.translate(-W / 2, -H * 0.6)
        ff(ctx, T, ss)
        ctx.restore()
    if k > 0 and T < s + XF:
        draw_scene(k - 1)
        p = ease_io(prog(T, s, XF))
        ctx.push_group(); draw_scene(k); ctx.pop_group_to_source(); ctx.paint_with_alpha(p)
    else:
        draw_scene(k)
    draw_captions(ctx, T)
    # final fade out
    if T > DUR - 0.6:
        ctx.rectangle(0, 0, W, H); col(ctx, '#FFFFFF', prog(T, DUR - 0.6, 0.6)); ctx.fill()

def still(T, path):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); ctx = cairo.Context(surf)
    render_frame(ctx, T); surf.write_to_png(path)

def render_range(f0, f1, out):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    cmd = ['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}', '-r', str(FPS),
           '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', out]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for f in range(f0, f1):
        ctx = cairo.Context(surf)
        ctx.set_source_rgb(1, 1, 1); ctx.paint()
        render_frame(ctx, f / FPS)
        surf.flush()
        pr.stdin.write(bytes(surf.get_data()))
    pr.stdin.close(); pr.wait()

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'still':
        for T in sys.argv[3:]:
            still(float(T), os.path.join(sys.argv[2], f'f_{float(T):07.2f}.png'))
    elif mode == 'range':
        render_range(int(sys.argv[2]), int(sys.argv[3]), sys.argv[4])
    elif mode == 'info':
        for s, fn in STARTS: print(f'{s:7.2f} {fn.__name__}')
        for p in PAGES[:5]: print(' '.join(WORDS[i]['w'] for i in p))
        print(len(PAGES), 'pages')
