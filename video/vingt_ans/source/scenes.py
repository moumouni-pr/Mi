import math, random
from engine import *
from chars import *
from icons import *

FLOOR = 1660

# ============================================================ fonds
def bg_grad(ctx, c1, c2, y0=0, y1=H):
    g = cairo.LinearGradient(0, y0, 0, y1)
    g.add_color_stop_rgba(0, *hexc(c1)); g.add_color_stop_rgba(1, *hexc(c2))
    ctx.rectangle(0, 0, W, H); ctx.set_source(g); ctx.fill()

def bg_sky(ctx, t, ground='#A8DC8E', ground2='#93CF78', sky1='#9FD8FF', sky2='#E8F6FF', sun=True, gy=1500):
    bg_grad(ctx, sky1, sky2, 0, gy)
    if sun:
        circle(ctx, 880, 700, 90, '#FFE08A', 0.35); circle(ctx, 880, 700, 64, '#FFD447')
    for i, (x0, y, s) in enumerate(((150, 640, 1.0), (620, 560, 0.8), (980, 900, 0.9))):
        x = (x0 + t * (14 + i * 6)) % (W + 400) - 200
        ctx.save(); ctx.translate(x, y); cloud(ctx, s, '#FFFFFF', 0.9); ctx.restore()
    ctx.rectangle(0, gy, W, H - gy); col(ctx, ground); ctx.fill()
    ctx.rectangle(0, gy, W, 24); col(ctx, ground2); ctx.fill()

def bg_room(ctx, wall='#F1ECFF', wall2='#E6DEFB', floor='#E8D3BC', fy=1560, window=True, night=False):
    bg_grad(ctx, wall, wall2, 0, fy)
    if window:
        x, y = 760, 640
        fill_rrect(ctx, x - 130, y - 150, 260, 300, 18, '#FFFFFF')
        fill_rrect(ctx, x - 112, y - 132, 224, 264, 10, '#1E2A5A' if night else '#BFE6FF')
        if night:
            circle(ctx, x + 50, y - 60, 34, '#FFF3C4'); circle(ctx, x + 66, y - 72, 30, '#1E2A5A')
            for (sx, sy) in ((-60, -80), (-20, 30), (40, 70), (-70, 60)): circle(ctx, x + sx, y + sy, 4, '#FFFFFF')
        line(ctx, x, y - 132, x, y + 132, 10, '#FFFFFF'); line(ctx, x - 112, y, x + 112, y, 10, '#FFFFFF')
    ctx.rectangle(0, fy, W, H - fy); col(ctx, floor); ctx.fill()
    ctx.rectangle(0, fy - 18, W, 22); col(ctx, '#FFFFFF', 0.7); ctx.fill()

def bg_soft(ctx, t, c1='#FFF4E6', c2='#FFE7D1', dots='#FFB98A', floor=None, fy=1600):
    bg_grad(ctx, c1, c2)
    rnd = random.Random(7)
    for i in range(14):
        x = rnd.uniform(0, W); y = rnd.uniform(560, 1800); r = rnd.uniform(6, 16)
        y += math.sin(t * 0.8 + i) * 8
        circle(ctx, x, y, r, dots, 0.35)
    if floor:
        ctx.rectangle(0, fy, W, H - fy); col(ctx, floor); ctx.fill()

# ============================================================ aides
def put(ctx, x, y, fn, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s); fn(ctx); ctx.restore()

def P(txt, c, size=42, fg='#FFFFFF'):
    return lambda c2: pill(c2, txt, 0, 0, size, c, fg)

def row_item(ctx, icon_fn, label, w=640, h=140, ok=None, lc=NAVY, ls=34):
    card(ctx, w, h, '#FFFFFF', r=30)
    ctx.save(); ctx.translate(-w / 2 + 85, 0); icon_fn(ctx); ctx.restore()
    text(ctx, label, -w / 2 + 165, 13, ls, lc, 'bold', align='l')
    if ok == 'check': put(ctx, w / 2 - 55, 0, lambda c: check(c, 0.7))
    elif ok == 'cross': put(ctx, w / 2 - 55, 0, lambda c: cross(c, 0.7))

def walk_x(t, t0, d, x0, x1):
    p = prog(t, t0, d)
    return lerp(x0, x1, ease_io(p)), (t * 1.7 if 0 < p < 1 else None)

def boxed(txt, size, bg, fg='#FFFFFF', padx=46, h=None):
    def f(c):
        font(c, size, 'xbold'); w = text_w(c, txt); hh = h or size * 1.45
        fill_rrect(c, -w / 2 - padx, -hh / 2, w + 2 * padx, hh, 30, bg)
        c.move_to(-w / 2, size * 0.36); col(c, fg); c.show_text(txt)
    return f

def plain(txt, size, c=NAVY, kind='xbold'):
    return lambda c2: text(c2, txt, 0, size * 0.36, size, c, kind)

# ================================================================= scènes
def sc_title(ctx, t, S):
    bg_grad(ctx, '#DCEBFF', '#C6DEFF')
    ctx.rectangle(0, 1580, W, 400); col(ctx, '#B9CCF0'); ctx.fill()
    t20 = tw('20', 0); ts = tw('sur', 0); tp = tw('pour', 0); tr = tw('reussir', 0)
    show(ctx, t, 0.05, W / 2, 330, plain('FAUT-IL PASSER', 84), kind='pop')
    show(ctx, t, t20 - 0.05, W / 2, 510, boxed('20 ANS', 150, CORAL, h=210), kind='pop', dur=0.5)
    show(ctx, t, ts - 0.05, W / 2, 700, plain("SUR LES BANCS DE L'ÉCOLE", 58, BLUE), kind='up')
    show(ctx, t, tp - 0.05, W / 2, 850, boxed('POUR RÉUSSIR ?', 84, GREEN), kind='pop', dur=0.5)
    put(ctx, 190, 1560, lambda c: book_stack(c, 1.3, 5))
    put(ctx, 900, 1500, lambda c: grad_cap(c, 1.1))
    pose = pose_seq(t, [(0, 'idle'), (t20, 'think'), (tr, 'shrug')])
    p = ease_back(prog(t, 0.15, 0.5))
    draw_char(ctx, ADAMA, W / 2, FLOOR + 60, 0.9 * max(0.01, p), pose=pose, t=t, mouth='o' if t > tr else 'smile',
              bag=True, brows=1.0 if t > tr else 0)
    show(ctx, t, tr, 760, 1080, lambda c: qmark(c, 1.5), kind='pop')
    show(ctx, t, tr + 0.15, 320, 1100, lambda c: qmark(c, 1.1, CORAL), kind='pop')

def sc_friends(ctx, t, S):
    bg_sky(ctx, t)
    ta = tw('adama', S); to = tw('ousmane', S); tam = tw('amis', S); tc = tw('camarades', S)
    xa, wa = walk_x(t, S, 1.2, -200, 290)
    xo, wo = walk_x(t, S + 0.15, 1.2, 1300, 790)
    draw_char(ctx, ADAMA, xa, FLOOR, 0.95, pose='wave' if t > ta else 'idle', t=t, walk=wa, bag=True,
              mouth='big' if t > ta else 'smile', look=0.6)
    draw_char(ctx, OUSMANE, xo, FLOOR, 0.95, pose='wave' if t > to else 'idle', t=t, walk=wo, bag=True,
              mouth='big' if t > to else 'smile', look=-0.6, blink_seed=1)
    name_tag(ctx, t, ta, ADAMA, 290, 880, 1.25)
    name_tag(ctx, t, to, OUSMANE, 790, 880, 1.25)
    show(ctx, t, tam - 0.1, W / 2, 640, P("Amis d'enfance", PURPLE, 46), kind='down')
    show(ctx, t, tam + 0.1, W / 2, 1010, lambda c: heart(c, 1.2), kind='pop')
    show(ctx, t, tc - 0.1, W / 2, 750, P('Camarades de classe', CORAL, 42), kind='pop')

def sc_good(ctx, t, S):
    bg_room(ctx, wall='#EAF3FF', wall2='#DCE9FF', floor='#D9C7AE', window=False)
    # tableau de classe
    fill_rrect(ctx, 190, 600, 700, 330, 18, '#8C5A3C'); fill_rrect(ctx, 208, 618, 664, 294, 10, '#2F6B55')
    tb = tw('bons', S); tt = tw('travailleurs', S); ta = tw('ambitieux', S)
    for i, (ti, lab, c) in enumerate(((tb, 'Bons élèves', YELLOW), (tt, 'Travailleurs', '#FFFFFF'), (ta, 'Ambitieux', '#9DE8C4'))):
        show(ctx, t, ti - 0.08, 540, 690 + i * 82, plain(lab, 54, c), kind='left')
        show(ctx, t, ti + 0.1, 300, 690 + i * 82, lambda c2: star(c2, 0.55), kind='pop')
    ha = draw_char(ctx, ADAMA, 290, FLOOR + 20, 0.88, pose='hold', t=t, mouth='big' if t > tb else 'smile', look=0.4)
    put(ctx, 290, ha['l'][1] - 20, lambda c: book(c, 0.75, BLUE, open_=True))
    draw_char(ctx, OUSMANE, 790, FLOOR + 20, 0.88, pose='cheer' if t > ta else 'raiseR', t=t,
              mouth='big', look=-0.4, blink_seed=1)

def sc_families(ctx, t, S):
    bg_grad(ctx, '#DCE8FF', '#C9DBFF')
    ctx.rectangle(W / 2, 0, W / 2, H); col(ctx, '#D8F5E6'); ctx.fill()
    ctx.rectangle(0, 1560, W / 2, 400); col(ctx, '#B9CCF0'); ctx.fill()
    ctx.rectangle(W / 2, 1560, W / 2, 400); col(ctx, '#A6E3C2'); ctx.fill()
    line(ctx, W / 2, 560, W / 2, H, 6, '#FFFFFF', 0.9)
    tf = tw('familles', S); tm = tw('meme', S); tr = tw('reussite', S)
    show(ctx, t, S + 0.1, 270, 1150, lambda c: house_bg(c, 400, '#FFFFFF'), kind='grow')
    show(ctx, t, S + 0.25, 810, 1150, lambda c: house_bg(c, 400, '#FFFDF3'), kind='grow')
    draw_char(ctx, ADAMA, 270, FLOOR + 30, 0.62, pose='idle', t=t, look=0.6, bag=True)
    draw_char(ctx, OUSMANE, 810, FLOOR + 30, 0.62, pose='idle', t=t, look=-0.6, bag=True, blink_seed=1)
    show(ctx, t, tf - 0.1, 270, 820, P("Famille d'Adama", BLUE, 34), kind='down')
    show(ctx, t, tf + 0.05, 810, 820, P("Famille d'Ousmane", GREEN, 34), kind='down')
    def neq(c):
        circle(c, 0, 0, 92, '#FFFFFF'); circle(c, 0, 0, 80, CORAL)
        line(c, -38, -18, 38, -18, 14, '#FFFFFF'); line(c, -38, 18, 38, 18, 14, '#FFFFFF'); line(c, -22, 44, 22, -44, 12, '#FFFFFF')
    show(ctx, t, tm - 0.05, W / 2, 1150, neq, kind='pop', dur=0.5)
    show(ctx, t, tr - 0.1, W / 2, 660, P('2 visions de la réussite', NAVY, 44), kind='pop')

def _adama_room(ctx):
    bg_room(ctx, wall='#EEF0FF', wall2='#E0E4FB', floor='#D8CBB8', window=False)
    fill_rrect(ctx, 400, 610, 280, 190, 12, '#C9A46A'); fill_rrect(ctx, 414, 624, 252, 162, 6, '#FFF6E0')
    put(ctx, 540, 705, lambda c: grad_cap(c, 0.8))

def sc_adama_family(ctx, t, S):
    _adama_room(ctx)
    tl = tw('longues', S); td = tw('diplomes', S); tob = tw('obligation', S)
    show(ctx, t, S + 0.1, W / 2, 900, P("Chez Adama", BLUE, 44), kind='down', t1=tl - 0.2)
    draw_char(ctx, DAD, 200, FLOOR + 10, 0.86, pose='hips' if t > tob else 'idle', t=t, look=0.6,
              mouth='neutral', brows=-0.6 if t > tob else 0)
    draw_char(ctx, MOM, 880, FLOOR + 10, 0.84, pose='present' if t > td else 'idle', t=t, look=-0.6, blink_seed=2, flip=True)
    draw_char(ctx, ADAMA, 540, FLOOR + 50, 0.74, pose='hold' if t > tl else 'idle', t=t, bag=True,
              mouth='o' if t > tob else 'smile', blink_seed=1)
    show(ctx, t, tl - 0.05, 540, 960, lambda c: book_stack(c, 0.9, 5), kind='pop', t1=td - 0.1)
    for i, lab in enumerate(('LICENCE', 'MASTER', 'DOCTORAT')):
        show(ctx, t, td + i * 0.18, 290 + i * 250, 960 - (50 if i == 1 else 0),
             lambda c, lab=lab: diploma_doc(c, 0.9, lab), kind='pop', t1=tob - 0.15)
    show(ctx, t, tob - 0.05, W / 2, 950, boxed('OBLIGATION', 78, RED), kind='pop', dur=0.5)

def sc_rate(ctx, t, S):
    _adama_room(ctx)
    tp = tw('parents', S); tu = tw("l'universite", S); tr = tw('rate', S); tv = tw('vagabond', S)
    draw_char(ctx, DAD, 240, FLOOR + 10, 0.95, pose='point' if t > tp else 'hips', t=t, look=0.8,
              mouth='open' if (t > tp and math.sin(t * 20) > 0) else 'neutral', brows=-1.0)
    draw_char(ctx, ADAMA, 820, FLOOR + 30, 0.8, pose='idle', t=t, bag=True, look=-0.7,
              mouth='o' if t > tr else 'neutral', brows=1.0, blink_seed=1)
    def bub(c):
        speech_bubble(c, 560, 230, '#FFFFFF', tail='bl')
        text(c, "Pas d'université ?", 0, -20, 46, NAVY, 'xbold')
        put(c, -150, 55, lambda c2: grad_cap(c2, 0.35)); put(c, -150, 55, lambda c2: big_x(c2, 0.5, RED, 1.0))
        text(c, 'Inacceptable !', 50, 72, 36, RED, 'bold')
    show(ctx, t, tu - 0.3, 470, 760, bub, kind='pop')
    show(ctx, t, tr - 0.05, 800, 900, boxed('UN RATÉ', 62, RED), kind='pop')
    show(ctx, t, tv - 0.05, 780, 1010, boxed('UN VAGABOND', 52, '#B5364A'), kind='pop')
    if t > tr: show(ctx, t, tr, 940, 1120, lambda c: sweat(c, 1.2), kind='pop')

def _ousmane_room(ctx):
    bg_room(ctx, wall='#FFF6E3', wall2='#FFEBC9', floor='#D9B98F', window=False)

def sc_ousmane_family(ctx, t, S):
    _ousmane_room(ctx)
    ti = tw('ignorance', S); tc = tw('connaissances', S); tm = tw('monde', S); ta = tw('autrement', S)
    show(ctx, t, S + 0.1, W / 2, 640, P("Chez Ousmane", GREEN, 44), kind='down')
    show(ctx, t, ta - 0.05, W / 2, 760, P('Une autre vision', ORANGE, 38), kind='pop', t1=ti - 0.3)
    draw_char(ctx, DAD2, 200, FLOOR + 10, 0.8, pose='present' if t > ti else 'idle', t=t, look=0.6, mouth='big')
    draw_char(ctx, MOM2, 880, FLOOR + 10, 0.78, pose='idle', t=t, look=-0.6, blink_seed=2, mouth='big', flip=True)
    draw_char(ctx, OUSMANE, 540, FLOOR + 50, 0.7, pose='cheer' if t > tm else 'idle', t=t, bag=True, mouth='big', blink_seed=1)
    rows = ((ti, lambda c: bulb(c, 0.5, 1.0), "Sortir de l'ignorance"), (tc, lambda c: book(c, 0.45, BLUE, open_=True), 'Acquérir des connaissances'),
            (tm, lambda c: globe(c, 0.6), 'Comprendre le monde'))
    for i, (tt, fn, lab) in enumerate(rows):
        show(ctx, t, tt - 0.1, W / 2, 775 + i * 145, lambda c, fn=fn, lab=lab: row_item(c, fn, lab, w=760, h=128, ok='check'), kind='left')

def sc_life(ctx, t, S):
    bg_soft(ctx, t, '#F2FBF4', '#DDF3E4', dots='#8FD9AE', floor='#C7E9D3')
    tv = tw('vie', S); tl = tw('limite', S); td = tw('diplomes', S)
    show(ctx, t, tv - 0.08, W / 2, 700, boxed('LA VIE', 110, GREEN, h=170), kind='pop', dur=0.5)
    show(ctx, t, tl - 0.05, W / 2, 880, plain('ne se limite pas à…', 50, NAVY, 'bold'), kind='up')
    show(ctx, t, td - 0.1, W / 2, 1090, lambda c: diploma_doc(c, 1.5, 'UN PAPIER'), kind='pop', dur=0.5)
    for i, (dx, fn) in enumerate(((-380, lambda c: handshake(c, 0.9)), (380, lambda c: bulb(c, 0.9, 1.0)))):
        show(ctx, t, td + 0.25 + i * 0.15, W / 2 + dx, 1090, fn, kind='pop')
    draw_char(ctx, OUSMANE, W / 2, FLOOR + 60, 0.62, pose='shrug' if t > td else 'idle', t=t, mouth='big', bag=True)

def sc_bepc(ctx, t, S):
    bg_sky(ctx, t, ground='#E8D3B0', ground2='#D9C29C', sky1='#BDE5FF', sky2='#F3FAFF')
    tb = tw('bepc', S); te = tw('envoye', S); to = tw('oncle', S); tm = tw('monde', S)
    p = ease_back(prog(t, to - 0.3, 0.6))
    if p > 0.01:
        ctx.save(); ctx.translate(840, 1500); ctx.scale(p, p)
        shop_stand(ctx, 430, sign="CHEZ L'ONCLE", t=t, sub='Commerce général'); ctx.restore()
    if t > to - 0.3:
        with_alpha(ctx, ease_out(prog(t, to - 0.3, 0.4)), lambda: draw_char(ctx, UNCLE, 540, FLOOR + 10, 0.8, pose='wave' if t > to else 'idle',
                                                                    t=t, mouth='big', look=-0.6, blink_seed=3, flip=True))
    xo, wo = walk_x(t, te - 0.1, 1.6, -150, 220)
    draw_char(ctx, OUSMANE, xo, FLOOR + 30, 0.78, pose='wave' if t > to + 0.6 else 'idle', t=t, walk=wo, bag=True,
              mouth='big', look=0.7, blink_seed=1)
    show(ctx, t, tb - 0.1, 300, 760, lambda c: diploma_doc(c, 1.25, 'BEPC'), kind='pop', dur=0.5)
    show(ctx, t, tb + 0.15, 440, 660, lambda c: check(c, 0.9), kind='pop')
    show(ctx, t, tm - 0.1, W / 2, 1790, P('Découvrir le monde des affaires', GREEN, 40), kind='up')

def sc_bac(ctx, t, S):
    bg_sky(ctx, t, ground='#B9E3A4')
    tp = tw('parallele', S); te = tw('etudes', S); tb = tw('baccalaureat', S); tm = tw('mention', S)
    show(ctx, t, te - 0.1, 320, 660, P('Études', BLUE, 46), kind='pop')
    show(ctx, t, tp - 0.05, 540, 660, plain('+', 76), kind='pop')
    show(ctx, t, tp - 0.1, 770, 660, P('Commerce', GREEN, 46), kind='pop')
    put(ctx, 850, 1440, lambda c: shop_stand(c, 400, sign="CHEZ L'ONCLE", t=t))
    h = draw_char(ctx, OUSMANE, 230, FLOOR + 10, 0.9, pose='cheer' if t > tb + 0.3 else 'hold', t=t,
                  mouth='big' if t > tb else 'smile', look=0.3, bag=True)
    if t < tb + 0.3: put(ctx, 230, h['l'][1] - 20, lambda c: book(c, 0.75, BLUE, open_=True))
    show(ctx, t, tb - 0.1, 640, 880, lambda c: diploma_doc(c, 1.5, 'BACCALAURÉAT'), kind='pop', dur=0.5)
    show(ctx, t, tm - 0.05, 660, 1075, P('Mention passable', ORANGE, 44), kind='pop')
    confetti(ctx, t, tb, 640, 900, n=30, seed=3)

def sc_licence(ctx, t, S):
    bg_sky(ctx, t, sun=False)
    put(ctx, W / 2, 1270, lambda c: university(c, 680, label='ÉCOLE DE COMMERCE', ls=30))
    ctx.rectangle(0, 1530, W, 400); col(ctx, '#A8DC8E'); ctx.fill()
    tl = tw('licence', S)
    xo, wo = walk_x(t, S, 1.3, -150, 250)
    draw_char(ctx, OUSMANE, xo, FLOOR + 50, 0.85, pose='cheer' if t > tl else 'idle', t=t, walk=wo,
              bag=t < tl, grad=t > tl, mouth='big', look=0.0)
    show(ctx, t, tl - 0.1, 600, 800, lambda c: diploma_doc(c, 1.5, 'LICENCE'), kind='pop', dur=0.5)
    confetti(ctx, t, tl, 600, 820, n=44, seed=5)

def sc_decision(ctx, t, S):
    _ousmane_room(ctx)
    td = tw('decision', S); ta = tw('annonce', S); tar = tw('arreter', S); tc = tw('commerce', S)
    sur = t > tar
    draw_char(ctx, OUSMANE, 230, FLOOR + 20, 0.92, pose=pose_seq(t, [(0, 'think'), (ta, 'present'), (tc, 'cheer')]), t=t,
              mouth='big', look=0.7, talk=ta < t < tc)
    draw_char(ctx, DAD2, 700, FLOOR + 10, 0.78, pose='scratch' if sur else 'idle', t=t, look=-0.7,
              mouth='o' if sur else 'smile', brows=1.0 if sur else 0, blink_seed=2, flip=True)
    draw_char(ctx, MOM2, 930, FLOOR + 10, 0.76, pose='shrug' if sur else 'idle', t=t, look=-0.7,
              mouth='o' if sur else 'smile', brows=1.0 if sur else 0, blink_seed=4, flip=True)
    show(ctx, t, td - 0.1, 230, 900, lambda c: bulb(c, 0.9, 1.0), kind='pop', t1=ta - 0.1)
    def bub(c):
        speech_bubble(c, 640, 210, '#FFFFFF', tail='bl')
        text(c, "« J'arrête les études »", 0, 16, 46, NAVY, 'xbold')
    show(ctx, t, ta - 0.05, 470, 800, bub, kind='pop')
    show(ctx, t, tar + 0.1, 700, 1010, lambda c: exclaim(c, 1.0), kind='pop')
    show(ctx, t, tar + 0.25, 930, 1030, lambda c: exclaim(c, 1.0, ORANGE), kind='pop')
    show(ctx, t, tc - 0.3, W / 2, 1790, P('100 % commerce', GREEN, 48), kind='up')

def sc_launch(ctx, t, S):
    bg_soft(ctx, t, '#EFFBF3', '#D6F2E0', dots='#7FD6AE', floor='#BFE6CE')
    tc = tw('connaissances', S); te = tw('experience', S); tl = tw('lance', S)
    show(ctx, t, tc - 0.1, 290, 820, lambda c: icon_card(c, lambda c2: book(c2, 0.9, BLUE, open_=True), 'Connaissances', w=400, h=330, ls=38), kind='pop')
    show(ctx, t, te - 0.15, 540, 820, plain('+', 90), kind='pop')
    show(ctx, t, te - 0.1, 790, 820, lambda c: icon_card(c, lambda c2: handshake(c2, 1.1), 'Expérience', w=400, h=330, ls=38), kind='pop')
    q = ease_in(prog(t, tl + 0.2, 1.6))
    if t > tl - 0.1:
        show(ctx, t, tl - 0.1, 820, 1380 - q * 1300, lambda c: rocket(c, 1.5), kind='pop')
        for k in range(5):
            circle(ctx, 820 + math.sin(t * 9 + k) * 14, 1620 - q * 1300 + k * 34, 26 - k * 4, '#FFFFFF', 0.5 * (1 - k / 6))
    draw_char(ctx, OUSMANE, 330, FLOOR + 40, 0.9, pose='cheer' if t > tl else 'idle', t=t, mouth='big', look=0.7)
    show(ctx, t, tl - 0.05, W / 2, 1800, P('Il se lance dans les affaires', GREEN, 44), kind='up')

def sc_two(ctx, t, S):
    bg_sky(ctx, t, ground='#B9E3A4')
    td = tw('deux ans', S); te = tw('entreprises', S); ti = tw('import-export', S); tt = tw('transport', S)
    show(ctx, t, td - 0.1, 250, 760, lambda c: calendar(c, 0.9, '2', GREEN), kind='pop', t1=ti - 0.15)
    show(ctx, t, td + 0.1, 600, 770, plain('ans seulement', 64), kind='left', t1=ti - 0.15)
    show(ctx, t, te - 0.1, W / 2, 1000, boxed('2 ENTREPRISES', 70, NAVY), kind='pop', t1=ti - 0.15)
    show(ctx, t, ti - 0.1, 290, 860, lambda c: icon_card(c, lambda c2: ship_boxes(c2, 1.25), 'Import-export', w=440, h=400, ls=40), kind='pop')
    show(ctx, t, tt - 0.1, 790, 860, lambda c: icon_card(c, lambda c2: truck(c2, 1.5), 'Transport', w=440, h=400, ls=40), kind='pop')
    show(ctx, t, ti + 0.1, 130, 690, lambda c: number_badge(c, 1, GREEN, 46), kind='pop')
    show(ctx, t, tt + 0.1, 630, 690, lambda c: number_badge(c, 2, GREEN, 46), kind='pop')
    draw_char(ctx, OUSMANE, W / 2, FLOOR + 40, 0.82, pose='cheer' if t > te else 'idle', t=t, mouth='big')
    confetti(ctx, t, tt, 540, 1000, n=36, seed=8)

def sc_adama_uni(ctx, t, S):
    bg_room(ctx, wall='#2E3769', wall2='#252D5A', floor='#5A4A7A', night=True)
    tf = tw('faculte', S); td = tw('droit', S)
    draw_char(ctx, ADAMA, 430, FLOOR - 60, 0.85, pose='hold', t=t, mouth='neutral', look=0.0)
    put(ctx, 430, 1225, lambda c: book(c, 0.9, BLUE, open_=True))
    put(ctx, 540, 1460, lambda c: desk(c, 820))
    put(ctx, 800, 1340, lambda c: book_stack(c, 0.9, 5))
    put(ctx, 170, 1350, lambda c: lamp(c, 1.0))
    circle(ctx, 210, 1330, 260, '#FFE9A8', 0.10)
    put(ctx, 250, 700, lambda c: clock(c, 1.1, t * 3))
    show(ctx, t, S + 0.3, W / 2, 1760, P('Pendant ce temps…', PURPLE, 44), kind='up', t1=tf - 0.2)
    show(ctx, t, tf - 0.1, W / 2, 1760, P('Faculté de droit', BLUE, 50), kind='up')
    show(ctx, t, td - 0.1, 470, 860, lambda c: (circle(c, 0, 0, 120, '#FFFFFF', 0.95), put(c, 0, -16, lambda c2: scale_balance(c2, 0.5))), kind='pop')

def sc_seven(ctx, t, S):
    bg_soft(ctx, t, '#F3EEFF', '#E4DBFB', dots='#B9A3F0', floor='#D5C9F2')
    ts = tw('sept', S); td = tw('diplome', S)
    pr_ = prog(t, ts, max(0.5, td - ts - 0.35))
    n = min(7, 1 + int(pr_ * 7))
    done = t > td - 0.1
    def counter(c):
        card(c, 560, 330, '#FFFFFF', r=40)
        text(c, str(n), -110, 80, 250, CORAL if not done else GREEN, 'xbold')
        text(c, 'ans' if n > 1 else 'an', 120, 20, 90, NAVY, 'xbold')
        text(c, "d'université", 120, 90, 38, '#6B7196', 'bold')
    show(ctx, t, ts - 0.1, W / 2, 830, counter, kind='pop')
    for i in range(7):
        fill_rrect(ctx, 190 + i * 102, 1040, 88, 30, 15, '#FFFFFF' if i >= n else (GREEN if done else CORAL), 1.0 if t > ts - 0.1 else 0.0)
    show(ctx, t, ts - 0.1, 160, 1250, lambda c: hourglass(c, 1.0, pr_), kind='pop', t1=td)
    draw_char(ctx, ADAMA, 540, FLOOR + 40, 0.86, pose='cheer' if done else 'hold', t=t, grad=done,
              mouth='big' if done else 'neutral', brows=0 if done else -0.4)
    if not done: put(ctx, 540, 1245, lambda c: book(c, 0.8, BLUE, open_=True))
    show(ctx, t, td - 0.1, 860, 1230, lambda c: diploma_doc(c, 1.15, 'DROIT'), kind='pop', dur=0.5)
    confetti(ctx, t, td, 540, 1200, n=40, seed=6)

def sc_unemployed(ctx, t, S):
    bg_sky(ctx, t, sky1='#B6C2D9', sky2='#E3E8F2', ground='#C5C9B4', ground2='#B3B7A2', sun=False)
    tc = tw('chomage', S); tca = tw('candidatures', S); tr = tw('reponse', S); tt = tw('trois', S)
    show(ctx, t, S + 0.2, 300, 760, lambda c: rain_cloud(c, 1.5, t), kind='down')
    h = draw_char(ctx, ADAMA, 300, FLOOR, 0.95, pose='holdR', t=t, mouth='sad', brows=-1.0, look=0.5)
    put(ctx, h['r'][0] + 10, h['r'][1] - 40, lambda c: cv(c, 0.42, ADAMA))
    show(ctx, t, tt - 0.05, 730, 700, boxed('3 ANS', 110, RED, h=170), kind='pop', dur=0.5)
    show(ctx, t, tc - 0.1, 730, 850, plain('de chômage', 60, NAVY), kind='up')
    for i in range(5):
        t0 = tca - 0.2 + i * 0.32
        if t < t0: continue
        q = prog(t, t0, 0.7); x = lerp(430, 640 + (i % 3) * 150, ease_out(q)); y = lerp(1250, 1040 + (i // 3) * 250 + (i % 2) * 30, ease_out(q))
        ctx.save(); ctx.translate(x, y); ctx.rotate((i - 2) * 0.09); cv(ctx, 0.5 * (0.4 + 0.6 * ease_out(q)), ADAMA)
        if t > t0 + 0.75: big_x(ctx, 0.45, RED, prog(t, t0 + 0.75, 0.25))
        ctx.restore()
    show(ctx, t, tr - 0.05, 730, 1560, P('0 réponse favorable', '#6B7196', 44), kind='pop')

def sc_job(ctx, t, S):
    bg_room(ctx, wall='#EEF3F8', wall2='#DDE6F0', floor='#C9CED8', window=False)
    te = tw('emploi', S); tm = tw('malheureusement', S); ts = tw('salaire', S); tb = tw('besoins', S); tf = tw('famille', S)
    bad = t > tm
    draw_char(ctx, ADAMA, 240, FLOOR + 20, 0.9, pose='shrug' if t > tf else ('scratch' if bad else ('cheer' if t > te else 'idle')), t=t,
              mouth='sad' if bad else 'big', brows=-0.8 if bad else 0, look=0.6)
    show(ctx, t, te - 0.1, 600, 740, lambda c: briefcase(c, 1.3), kind='pop', t1=tm)
    show(ctx, t, te + 0.05, 600, 900, P('Enfin un emploi !', BLUE, 46), kind='pop', t1=tm)
    def pay(c):
        card(c, 600, 250, '#FFFFFF', r=34)
        put(c, -210, 0, lambda c2: wallet(c2, 0.8))
        text(c, 'Salaire', -100, -50, 40, NAVY, 'xbold', align='l')
        fill_rrect(c, -100, -10, 360, 44, 22, '#E3E6F2')
        fill_rrect(c, -100, -10, 360 * lerp(0.9, 0.2, ease_io(prog(t, ts, 0.9))), 44, 22, RED)
        text(c, 'à peine suffisant', -100, 88, 30, '#6B7196', 'bold', align='l')
    show(ctx, t, ts - 0.2, 700, 780, pay, kind='pop')
    show(ctx, t, tb - 0.1, 700, 1010, lambda c: row_item(c, lambda c2: person_icon(c2, 0.5, BLUE), 'Ses besoins : juste', w=600, ls=32), kind='left')
    show(ctx, t, tf - 0.5, 700, 1170, lambda c: row_item(c, lambda c2: parents(c2, 0.5), 'Une famille ?', w=600, ls=32, ok='cross'), kind='left')

def sc_ousmane_grow(ctx, t, S):
    bg_sky(ctx, t, ground='#B9E3A4')
    labs = [('developper', 'Développer'), ('apprendre', 'Apprendre'), ('former', 'Se former'), ('investir', 'Investir')]
    ts = [tw(q, S) for q, _ in labs]
    k = sum(1 for x in ts if t >= x - 0.1)
    put(ctx, 540, 1500, lambda c: stairs(c, 1.5, 4))
    for i, (q, lab) in enumerate(labs):
        show(ctx, t, ts[i] - 0.1, 540 + (-225 + i * 150) * 1.5, 1500 - i * 165 + 80,
             plain(lab, 31, '#FFFFFF' if i > 1 else '#16634A'), kind='up')
    i = max(0, k - 1)
    tx = 540 + (-225 + i * 150) * 1.5; ty = 1500 - i * 165
    if k >= 1:
        j = max(0, i - 1); q = ease_io(prog(t, ts[i] - 0.1, 0.4)) if i > 0 else 1.0
        px = lerp(540 + (-225 + j * 150) * 1.5, tx, q); py = lerp(1500 - j * 165, ty, q) - math.sin(q * math.pi) * 70
    else:
        px, py = 110, 1500
    draw_char(ctx, OUSMANE, px, py, 0.5, pose='cheer' if k == 4 else 'run', t=t, mouth='big', look=0.6)
    show(ctx, t, ts[3] + 0.1, 640, 760, lambda c: coin(c, 1.4, t * 3), kind='pop')
    show(ctx, t, ts[3] + 0.25, 520, 700, lambda c: coin(c, 1.0, t * 3 + 1), kind='pop')
    show(ctx, t, ts[3] + 0.4, 720, 660, lambda c: sparkle(c, 1.0), kind='pop')
    show(ctx, t, S + 0.2, 260, 700, P('Ousmane', GREEN, 46), kind='down')

def sc_who(ctx, t, S):
    bg_soft(ctx, t, '#FFF4E6', '#FFE7D1', dots='#FFB98A', floor='#F0D2B2')
    tr = tw('raison', S); ta = tw('adama', S); to = tw('ousmane', S)
    tilt = math.sin(t * 2.2) * 0.12
    put(ctx, W / 2, 1150, lambda c: scale_balance(c, 1.25, tilt))
    draw_char(ctx, ADAMA, 190, FLOOR + 20, 0.66, pose='shrug', t=t, look=0.7, mouth='neutral')
    draw_char(ctx, OUSMANE, 890, FLOOR + 20, 0.66, pose='shrug', t=t, look=-0.7, mouth='neutral', blink_seed=1)
    show(ctx, t, tr - 0.3, W / 2, 680, boxed('QUI A RAISON ?', 80, PURPLE), kind='pop', dur=0.5)
    show(ctx, t, tr, W / 2, 860, lambda c: qmark(c, 1.6), kind='pop')
    show(ctx, t, ta - 0.1, 230, 1000, P("Famille d'Adama", BLUE, 34), kind='pop')
    show(ctx, t, to - 0.1, 850, 1000, P("Famille d'Ousmane", GREEN, 34), kind='pop')

def sc_doors(ctx, t, S):
    bg_soft(ctx, t, '#F1F0FF', '#E0DEFB', dots='#B4AEF0', floor='#CFCBEF')
    te = tw('etudes', S); tp = tw('perte', S); td = tw('diplomes', S); tpo = tw('portes', S)
    show(ctx, t, te - 0.1, 300, 720, lambda c: book_stack(c, 1.1, 5), kind='pop', t1=td - 0.1)
    show(ctx, t, tp - 0.3, 690, 700, plain('Les études :', 52), kind='left', t1=td - 0.1)
    show(ctx, t, tp - 0.1, 690, 800, P('PAS une perte de temps', GREEN, 38), kind='pop', t1=td - 0.1)
    show(ctx, t, td - 0.1, W / 2, 740, lambda c: diploma_doc(c, 1.5, 'LICENCE · MASTER'), kind='pop', dur=0.5)
    for i in range(3):
        p = ease_io(prog(t, tpo - 0.35 + i * 0.22, 0.7))
        put(ctx, 230 + i * 310, 1330, lambda c, p=p: door(c, 1.05, p))
    show(ctx, t, tpo + 0.2, W / 2, 1790, P('Les diplômes ouvrent des portes', PURPLE, 40), kind='up')

def sc_error(ctx, t, S):
    bg_soft(ctx, t, '#FFF1F0', '#FFE0DE', dots='#FF9E99', floor='#F5C9C6')
    t20 = tw('20', S); ten = tw('entreprendre', S); tg = tw('gerer', S); ts = tw('saisir', S); te = tw('erreur', S)
    show(ctx, t, t20 - 0.1, 300, 700, boxed('20 ANS', 84, CORAL), kind='pop')
    show(ctx, t, t20 + 0.2, 740, 700, plain("d'école…", 64), kind='left')
    show(ctx, t, ten - 0.6, W / 2, 830, plain('sans jamais apprendre à :', 42, '#6B7196', 'bold'), kind='up')
    rows = ((ten, lambda c: rocket(c, 0.36), 'Entreprendre'), (tg, lambda c: wallet(c, 0.5), 'Gérer son argent'),
            (ts, lambda c: bulb(c, 0.5, 1.0), 'Saisir les opportunités'))
    for i, (tt, fn, lab) in enumerate(rows):
        show(ctx, t, tt - 0.1, W / 2, 960 + i * 165, lambda c, fn=fn, lab=lab: row_item(c, fn, lab, w=780, h=145, ls=38, ok='cross'), kind='left')
    show(ctx, t, te - 0.4, 300, 1560, lambda c: warning(c, 1.3), kind='pop')
    show(ctx, t, te - 0.15, 690, 1560, boxed('UNE ERREUR', 66, RED), kind='pop', dur=0.5)

def sc_success(ctx, t, S):
    bg_grad(ctx, '#FFF8E1', '#FFE9B8')
    ctx.rectangle(0, 1580, W, 400); col(ctx, '#F4D58A'); ctx.fill()
    tv = tw('vraie', S); ta = tw('accumuler', S); tt = tw('transformer', S); tc = tw('connaissances', S); to = tw('opportunites', S)
    show(ctx, t, tv - 0.05, W / 2, 680, boxed('LA VRAIE RÉUSSITE', 70, NAVY), kind='pop', dur=0.5)
    for i in range(3):
        show(ctx, t, ta - 0.1 + i * 0.12, 380 + i * 160, 900 + (i % 2) * 30, lambda c: diploma_doc(c, 0.8, 'DIPLÔME'), kind='pop', t1=tt - 0.2)
    show(ctx, t, ta + 0.4, W / 2, 1060, P('pas seulement…', '#6B7196', 40), kind='pop', t1=tt - 0.2)
    show(ctx, t, tc - 0.4, 250, 960, lambda c: icon_card(c, lambda c2: book(c2, 0.9, BLUE, open_=True), 'Connaissances', w=380, h=330, ls=36), kind='pop')
    p = ease_out(prog(t, tt - 0.1, 0.6))
    if t > tt - 0.1: arrow(ctx, 460, 960, 620, 960, GREEN, 18, 44, p)
    show(ctx, t, to - 0.15, 830, 960, lambda c: icon_card(c, lambda c2: rocket(c2, 0.95), 'Opportunités', w=380, h=330, c='#E9F9F1', ls=36), kind='pop')
    draw_char(ctx, ADAMA, 300, FLOOR + 50, 0.78, pose='cheer' if t > to else 'idle', t=t, mouth='big', look=0.5)
    draw_char(ctx, OUSMANE, 780, FLOOR + 50, 0.78, pose='cheer' if t > to else 'idle', t=t, mouth='big', look=-0.5, blink_seed=1)
    confetti(ctx, t, to, 540, 1000, n=50, seed=9)

def sc_end(ctx, t, S):
    bg_grad(ctx, '#DCE8FF', '#C9DBFF')
    ctx.rectangle(W / 2, 0, W / 2, H); col(ctx, '#D8F5E6'); ctx.fill()
    ctx.rectangle(0, 1560, W / 2, 400); col(ctx, '#B9CCF0'); ctx.fill()
    ctx.rectangle(W / 2, 1560, W / 2, 400); col(ctx, '#A6E3C2'); ctx.fill()
    tt = tw('toi', S); t20 = tw('20', S); te = tw('emploi', S); tou = tw('ou', S); tap = tw('apprendre', S); taf = tw('affaires', S)
    show(ctx, t, tt - 0.1, W / 2, 660, boxed('ET TOI ?', 100, CORAL, h=160), kind='pop', dur=0.5)
    def optA(c):
        card(c, 460, 400, '#FFFFFF', r=36)
        put(c, -110, -70, lambda c2: book_stack(c2, 0.8, 5)); put(c, 110, -80, lambda c2: cv(c2, 0.42, ADAMA))
        text(c, "20 ans d'études", 0, 110, 38, BLUE, 'xbold'); text(c, 'puis chercher un emploi', 0, 160, 30, NAVY, 'bold')
    def optB(c):
        card(c, 460, 400, '#FFFFFF', r=36)
        put(c, -120, -70, lambda c2: book(c2, 0.8, BLUE, open_=True)); put(c, 100, -40, lambda c2: shop_stand(c2, 190, sign='BUSINESS', sub=''))
        text(c, 'Étudier ET', 0, 110, 38, GREEN, 'xbold'); text(c, 'préparer ses affaires', 0, 160, 30, NAVY, 'bold')
    show(ctx, t, t20 - 0.2, 270, 1000, optA, kind='left')
    show(ctx, t, tap - 0.2, 810, 1000, optB, kind='right')
    show(ctx, t, t20 - 0.1, 90, 800, lambda c: number_badge(c, 'A', BLUE, 46), kind='pop')
    show(ctx, t, tap - 0.1, 630, 800, lambda c: number_badge(c, 'B', GREEN, 46), kind='pop')
    def ou(c):
        circle(c, 0, 0, 74, '#FFFFFF'); circle(c, 0, 0, 62, NAVY); text(c, 'OU', 0, 20, 52, '#FFFFFF', 'xbold')
    show(ctx, t, tou - 0.1, W / 2, 1000, ou, kind='pop')
    draw_char(ctx, ADAMA, 270, FLOOR + 40, 0.66, pose='shrug' if t > te else 'idle', t=t, look=0.6, mouth='neutral')
    draw_char(ctx, OUSMANE, 810, FLOOR + 40, 0.66, pose='cheer' if t > taf else 'idle', t=t, look=-0.6, mouth='big', blink_seed=1)
    show(ctx, t, taf + 0.2, W / 2, 1810, P('Dis-le en commentaire', PURPLE, 44), kind='up')

SCENES = [
    (0.0, sc_title, None), ('adama et ousmane', sc_friends, None), ('tous les deux', sc_good, None),
    ('pourtant', sc_families, None), ('dans la famille', sc_adama_family, None), ('pour ses parents', sc_rate, None),
    ('en revanche', sc_ousmane_family, None), ('mais elle estime', sc_life, None), ("c'est ainsi", sc_bepc, None),
    ('en parallele', sc_bac, None), ('il integre', sc_licence, None), ('mais a ce', sc_decision, None),
    ('grace a', sc_launch, None), ('en seulement', sc_two, None), ('pendant ce temps', sc_adama_uni, None),
    ('sept longues', sc_seven, None), ('mais le plus', sc_unemployed, None), ('finalement', sc_job, None),
    ('quant a', sc_ousmane_grow, None), ('mais alors', sc_who, None), ('en realite', sc_doors, None),
    ('mais passer', sc_error, None), ('la vraie', sc_success, None), ('et toi', sc_end, None),
]

def scene_starts():
    out = []; last = 0.0
    for q, fn, after in SCENES:
        s = q if isinstance(q, float) else tw(q, after if after is not None else last) - 0.25
        out.append((s, fn)); last = s + 0.3
    return out
