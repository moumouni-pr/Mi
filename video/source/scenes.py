import math, random
from engine import *
from chars import *
from icons import *

FLOOR = 1660

# ============================================================ backgrounds
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
        cloud(ctx, s, '#FFFFFF', 0.95)  if False else None
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

def headline(ctx, t, t0, n, txt, c=CORAL, y=650):
    def f(c2):
        font(c2, 50, 'xbold')
        w = text_w(c2, txt)
        tot = w + (130 if n else 0)
        x0 = -tot / 2
        if n:
            c2.save(); c2.translate(x0 + 50, 0); number_badge(c2, n, c, 50); c2.restore()
            x0 += 130
        c2.move_to(x0, 18); col(c2, NAVY); c2.show_text(txt)
    show(ctx, t, t0, W / 2, y, f, kind='up')

def row_item(ctx, icon_fn, label, w=520, h=150, ok=None, lc=NAVY, ls=36):
    card(ctx, w, h, '#FFFFFF', r=30)
    ctx.save(); ctx.translate(-w / 2 + 85, 0); icon_fn(ctx); ctx.restore()
    text(ctx, label, -w / 2 + 165, 13, ls, lc, 'bold', align='l')
    if ok == 'check':
        ctx.save(); ctx.translate(w / 2 - 55, 0); check(ctx, 0.7); ctx.restore()
    elif ok == 'cross':
        ctx.save(); ctx.translate(w / 2 - 55, 0); cross(ctx, 0.7); ctx.restore()

def walk_x(t, t0, d, x0, x1):
    p = prog(t, t0, d)
    x = lerp(x0, x1, ease_io(p))
    return x, (t * 1.7 if 0 < p < 1 else None)

# ================================================================= scenes
def sc_title(ctx, t, S, end=False):
    bg_grad(ctx, '#DCEBFF', '#C6DEFF')
    # right half: business side
    ctx.rectangle(W / 2, 0, W / 2, H); col(ctx, '#D3F5E3'); ctx.fill()
    ctx.rectangle(0, 1560, W / 2, 400); col(ctx, '#B9CCF0'); ctx.fill()
    ctx.rectangle(W / 2, 1560, W / 2, 400); col(ctx, '#A6E3C2'); ctx.fill()
    line(ctx, W / 2, 0, W / 2, H, 6, '#FFFFFF', 0.8)
    ctx.save(); ctx.translate(270, 1300); university(ctx, 400); ctx.restore()
    ctx.save(); ctx.translate(810, 1390); shop_stand(ctx, 420, sign='BUSINESS', t=t); ctx.restore()
    # title words
    q1 = 'un pied a l\'ecole' ; q2 = 'un autre dans le business'
    if end:
        t1 = tw('un pied', S); t2 = tw('un autre', t1)
    else:
        t1 = 0.0; t2 = tw('un autre', 0)
    def l1(c2):
        font(c2, 96, 'xbold'); s = "UN PIED À L'ÉCOLE,"
        c2.move_to(-text_w(c2, s) / 2, 0); col(c2, BLUE); c2.show_text(s)
    def l2(c2):
        font(c2, 80, 'xbold'); s = 'UN AUTRE DANS'
        c2.move_to(-text_w(c2, s) / 2, 0); col(c2, NAVY); c2.show_text(s)
    def l3(c2):
        fill_rrect(c2, -330, -100, 660, 140, 30, GREEN)
        font(c2, 96, 'xbold'); s = 'LE BUSINESS !'
        c2.move_to(-text_w(c2, s) / 2, 0); col(c2, '#FFFFFF'); c2.show_text(s)
    show(ctx, t, t1 + 0.05, W / 2, 420, l1, kind='pop')
    show(ctx, t, t2, W / 2, 560, l2, kind='pop')
    show(ctx, t, t2 + 0.55, W / 2, 720, l3, kind='pop', dur=0.5)
    # Élisée straddling
    p = ease_back(prog(t, t1 + 0.2, 0.5))
    draw_char(ctx, ELISEE, W / 2, FLOOR + 40, 0.95 * max(0.01, p), pose='cheer' if t > t2 else 'wave', t=t,
              mouth='big', bag=True)
    if end:
        draw_char(ctx, FABRICE, 170, FLOOR + 110, 0.62, pose='wave', t=t, mouth='big', bag=True)
        confetti(ctx, t, t2 + 0.6, W / 2, 900, n=50, seed=4)

def checklist_scene(ctx, t, S):
    bg_soft(ctx, t, '#F3F7FF', '#E3ECFF', dots='#A9C2FF', floor='#D6E0F5', fy=1600)
    t_err = tw('erreur', S); t_exp = tw('explique', S)
    # student (Fabrice as "toi")
    mouth = 'o' if t > t_err - 0.3 else 'smile'
    pose = pose_seq(t, [(0, 'idle'), (tw('penses', S), 'think'), (t_err - 0.4, 'scratch'), (t_exp - 0.1, 'idle')])
    draw_char(ctx, FABRICE, 230, FLOOR + 20, 0.82, pose=pose, t=t, mouth=mouth, bag=True,
              brows=1.0 if t > t_err - 0.3 else 0, look=0.8 if t < t_exp else 0)
    if t > t_err:
        show(ctx, t, t_err, 360, 1000, lambda c: sweat(c, 1.2), kind='pop', t1=t_exp)
    items = [('ecole', lambda c: (c.save(), c.scale(0.16, 0.16), c.translate(0, -60), university(c, 560), c.restore()), "Aller à l'école"),
             ('cours', lambda c: book(c, 0.42, BLUE, open_=True), 'Assister aux cours'),
             ('examens', lambda c: notes(c, 0.45), 'Préparer tes examens'),
             ('diplome', lambda c: diploma(c, 0.5), 'Attendre ton diplôme')]
    t_out = t_exp - 0.05
    keys = {'ecole': "l'ecole", 'cours': 'cours', 'examens': 'examens', 'diplome': 'diplome'}
    for i, (k, fn, lab) in enumerate(items):
        ti = tw(keys[k], S) - 0.1
        show(ctx, t, ti, 705, 690 + i * 175, lambda c, fn=fn, lab=lab: row_item(c, fn, lab, w=640, h=150, ls=30, ok='check'),
             kind='left', t1=t_out)
    t_m = tw('gagner', S) - 0.1
    def money(c):
        card(c, 600, 170, '#FFF6D6', r=30)
        c.save(); c.translate(-215, 0); coin(c, 1.0, t * 3); c.restore()
        text(c, "Gagner de l'argent ?", 40, 14, 36, '#B07A00', 'xbold')
    show(ctx, t, t_m, 700, 1400, money, kind='pop', t1=t_out)
    if t > tw('apres', S) if False else False: pass
    # big X
    if t >= t_err:
        p = prog(t, t_err, 0.35)
        def x(c): big_x(c, 2.4, RED, p)
        show(ctx, t, t_err, 700, 1040, x, kind='fade', dur=0.1, t1=t_out)
        show(ctx, t, t_err + 0.2, 700, 1040, lambda c: pill(c, 'GROSSE ERREUR !', 0, 0, 52, RED), kind='pop', t1=t_out)
    # Je t'explique -> bulb
    show(ctx, t, t_exp, 640, 1050, lambda c: bulb(c, 2.0, 0.5 + 0.5 * math.sin(t * 6)), kind='pop')

def sc_intro(ctx, t, S):
    bg_sky(ctx, t)
    t_e = tw('elisee', S); t_f = tw('fabrice', S); t_d = tw('deux etudiants', S)
    xe, we = walk_x(t, S, 1.6, -200, 300)
    xf, wf = walk_x(t, S + 0.2, 1.6, 1300, 790)
    draw_char(ctx, ELISEE, xe, FLOOR, 0.95, pose='wave' if t > t_e else 'idle', t=t, walk=we, bag=True,
              mouth='big' if t > t_e else 'smile', look=0.6)
    draw_char(ctx, FABRICE, xf, FLOOR, 0.95, pose='wave' if t > t_f else 'idle', t=t, walk=wf, bag=True,
              mouth='big' if t > t_f else 'smile', look=-0.6, blink_seed=1)
    name_tag(ctx, t, t_e, ELISEE, 300, 880, 1.25)
    name_tag(ctx, t, t_f, FABRICE, 790, 880, 1.25)
    show(ctx, t, t_d - 0.1, W / 2, 680, lambda c: pill(c, '2 ÉTUDIANTS', 0, 0, 46, PURPLE), kind='down')

def sc_same(ctx, t, S):
    bg_sky(ctx, t, sun=False)
    ctx.save(); ctx.translate(W / 2, 1270); university(ctx, 640); ctx.restore()
    ctx.rectangle(0, 1530, W, 400); col(ctx, '#A8DC8E'); ctx.fill()
    draw_char(ctx, ELISEE, 250, FLOOR + 40, 0.8, pose='idle', t=t, bag=True, look=0.5)
    draw_char(ctx, FABRICE, 830, FLOOR + 40, 0.8, pose='idle', t=t, bag=True, look=-0.5, blink_seed=1)
    for i, (q, lab, c) in enumerate((('universite', 'Même université', PURPLE), ('filiere', 'Même filière', BLUE),
                                     ('troisieme annee', 'Licence 3', CORAL))):
        show(ctx, t, tw(q, S) - 0.1, W / 2, 660 + i * 115, lambda c2, lab=lab, c=c: pill(c2, lab, 0, 0, 42, c), kind='pop')

def sc_contrary(ctx, t, S):
    bg_sky(ctx, t, ground='#B9E3A4')
    t_c = tw('contrairement', S); t_d = tw('decide', S); t_v = tw('vie active', S)
    # Fabrice reading, faded
    def fab():
        h = draw_char(ctx, FABRICE, 260, FLOOR, 0.8, pose='hold', t=t, look=0.0, blink_seed=1, mouth='neutral')
        ctx.save(); ctx.translate(260, h['l'][1] - 20); book(ctx, 0.75, BLUE, open_=True); ctx.restore()
    fade = 1 - 0.45 * ease_out(prog(t, t_d, 0.6))
    with_alpha(ctx, fade, fab)
    show(ctx, t, t_c, 260, 860, lambda c: pill(c, 'Il attend', 0, 0, 38, '#8A90B0'), kind='pop')
    xe, we = walk_x(t, t_v - 0.2, 1.2, 760, 860)
    pose = 'think' if t < t_v else 'cheer'
    draw_char(ctx, ELISEE, xe, FLOOR, 0.9, pose=pose, t=t, walk=we, bag=True, mouth='big' if t > t_d else 'smile', look=0.5)
    show(ctx, t, t_d, 760, 880, lambda c: bulb(c, 0.9, 1.0), kind='pop', t1=t_v - 0.2)
    def sign(c):
        fill_rrect(c, -14, 0, 28, 260, 8, '#8C5A3C')
        poly(c, [(-170, -80), (130, -80), (190, -10), (130, 60), (-170, 60)], GREEN)
        text(c, 'VIE ACTIVE', -20, 0, 44, '#FFFFFF', 'xbold')
    show(ctx, t, t_v - 0.1, 760, 820, sign, kind='pop')
    if t > t_v: show(ctx, t, t_v + 0.2, 980, 700, lambda c: sparkle(c, 1.1), kind='pop')

def sc_shop(ctx, t, S):
    bg_sky(ctx, t, ground='#E8D3B0', ground2='#D9C29C', sky1='#BDE5FF', sky2='#F3FAFF')
    t_c = tw('cours', S); t_com = tw('commerce', S); t_acc = tw("d'accessoires", S); t_tel = tw('telephones', S)
    show(ctx, t, t_c - 0.1, 330, 690, lambda c: pill(c, 'Cours', 0, 0, 44, BLUE), kind='pop')
    show(ctx, t, t_com - 0.1, 540, 690, lambda c: text(c, '+', 0, 22, 70, NAVY, 'xbold'), kind='pop')
    show(ctx, t, t_com, 760, 690, lambda c: pill(c, 'Commerce', 0, 0, 44, GREEN), kind='pop')
    p = ease_back(prog(t, t_com, 0.6))
    hands = draw_char(ctx, ELISEE, 540, FLOOR - 40, 0.85, pose='wave' if t > t_tel else 'idle', t=t, mouth='big', look=0.0)
    if p > 0.01:
        ctx.save(); ctx.translate(540, 1500); ctx.scale(p, p)
        shop_stand(ctx, 640, t=t, items=t > t_acc)
        ctx.restore()
    show(ctx, t, t_tel, 900, 1080, lambda c: phone(c, 1.1, TEAL), kind='pop')
    show(ctx, t, t_tel + 0.15, 180, 1060, lambda c: earphones(c, 1.1), kind='pop')

def sc_hard(ctx, t, S):
    bg_sky(ctx, t, sky1='#B6C2D9', sky2='#E3E8F2', ground='#C5C9B4', ground2='#B3B7A2', sun=False)
    t_f = tw('faciles', S)
    draw_char(ctx, ELISEE, 540, FLOOR, 1.0, pose='scratch', t=t, mouth='sad', brows=-1.0, look=-0.3)
    show(ctx, t, S + 0.2, 540, 820, lambda c: rain_cloud(c, 1.6, t), kind='down')
    show(ctx, t, t_f - 0.2, 680, 1040, lambda c: sweat(c, 1.4), kind='pop')
    show(ctx, t, t_f, W / 2, 1720, lambda c: pill(c, 'Pas facile...', 0, 0, 44, '#6B7290'), kind='up')

def sc_juggle(ctx, t, S):
    bg_soft(ctx, t, '#FFF4E6', '#FFE2C7', dots='#FFB98A', floor='#F2CFA9', fy=1600)
    draw_char(ctx, ELISEE, 540, FLOOR, 0.95, pose='juggle', t=t, mouth='open', look=math.sin(t * 3) * 0.8, brows=0.5)
    items = [('cours', lambda c: book(c, 0.75, BLUE), 'Cours', BLUE),
             ('revisions', lambda c: notes(c, 0.75), 'Révisions', PURPLE),
             ('commandes', lambda c: package(c, 0.8), 'Commandes', ORANGE),
             ('clients', lambda c: person_icon(c, 1.0, CORAL), 'Clients', CORAL)]
    for i, (q, fn, lab, cc) in enumerate(items):
        ti = tw(q, S) - 0.1
        a = t * 1.6 + i * math.pi / 2
        x = 540 + 340 * math.cos(a); y = 790 + 100 * math.sin(a) - 30 * math.sin(2 * a)
        def f(c, fn=fn, lab=lab, cc=cc):
            circle(c, 0, 0, 105, '#FFFFFF'); fn(c)
            c.save(); c.translate(0, 120); pill(c, lab, 0, 0, 30, cc); c.restore()
        show(ctx, t, ti, x, y, f, kind='pop')

def sc_grow(ctx, t, S):
    bg_sky(ctx, t, ground='#E8D3B0', ground2='#D9C29C')
    t_p = tw('progressivement', S); t_m = tw('marcher', S)
    # chart
    def chart(c):
        card(c, 400, 330, '#FFFFFF')
        vals = [0.25, 0.4, 0.6, 0.85]
        for i, v in enumerate(vals):
            g = ease_out(prog(t, t_p + i * 0.35, 0.5))
            hh = 230 * v * g
            fill_rrect(c, -150 + i * 85, 130 - hh, 60, hh, 10, GREEN if i == 3 else '#7FD6AE')
        arrow(c, -150, 80, 160, -120, CORAL, 12, 40, ease_out(prog(t, t_m, 0.5)))
    show(ctx, t, S + 0.1, 800, 790, chart, kind='pop')
    draw_char(ctx, ELISEE, 300, FLOOR - 40, 0.8, pose='wave' if t > t_m else 'idle', t=t, mouth='big')
    ctx.save(); ctx.translate(300, 1520); shop_stand(ctx, 480, t=t); ctx.restore()
    xc, wc = walk_x(t, S + 0.3, 1.6, 1300, 730)
    draw_char(ctx, CUST1, xc, FLOOR + 30, 0.7, pose='holdR', t=t, walk=wc, look=-0.8, blink_seed=2)
    xc2, wc2 = walk_x(t, S + 0.9, 1.6, 1400, 940)
    draw_char(ctx, CUST2, xc2, FLOOR + 50, 0.66, t=t, walk=wc2, look=-0.8, blink_seed=3)
    if t > t_m:
        for k in range(3):
            show(ctx, t, t_m + 0.15 * k, 300 + (k - 1) * 120, 980 - (k % 2) * 40, lambda c: coin(c, 0.9, t * 4), kind='pop')

def sc_profits(ctx, t, S):
    bg_soft(ctx, t, '#EFFBF4', '#D9F3E5', dots='#7FD6AE', floor='#CBEBD9', fy=1620)
    t_b = tw('benefices', S)
    h = draw_char(ctx, ELISEE, 220, FLOOR, 0.8, pose='hold', t=t, mouth='big', look=0.7)
    # coins falling into hands
    if t > t_b:
        for k in range(4):
            ph = math.fmod((t - t_b) * 0.9 + k * 0.25, 1.0)
            cx_ = h['r'][0] + 40 + ph * 260; cy_ = h['r'][1] - 60 - math.sin(ph * math.pi) * 200
            ctx.save(); ctx.translate(cx_, cy_); coin(ctx, 0.6 * (1 - ph * 0.4), t * 5 + k); ctx.restore()
        ctx.save(); ctx.translate((h['l'][0] + h['r'][0]) / 2, h['l'][1] - 20); banknote(ctx, 0.8); ctx.restore()
    cards = [('transport', bus, 'Transport', 620, 780), ('alimentation', plate, 'Nourriture', 880, 780),
             ('fournitures', supplies, 'Fournitures', 620, 1030), ('personnelles', tshirt, 'Perso', 880, 1030)]
    for q, fn, lab, x, y in cards:
        show(ctx, t, tw(q, S) - 0.1, x, y, lambda c, fn=fn, lab=lab: icon_card(c, lambda c3: fn(c3, 0.8), lab, 240, 230), kind='pop')
    t_p = tw('parents', S)
    def par(c):
        card(c, 500, 150, '#FFFFFF', r=30)
        c.save(); c.translate(-170, 10); parents(c, 0.8); c.restore()
        text(c, 'Plus autonome', 20, 13, 36, '#168556', 'xbold')
        c.save(); c.translate(190, 0); check(c, 0.7); c.restore()
    show(ctx, t, tw('sans toujours', S) - 0.1, 750, 1300, par, kind='up')

def sc_study(ctx, t, S):
    bg_room(ctx, wall='#2E3769', wall2='#252D5A', floor='#5A4A7A', night=True)
    t_x = tw('exclusivement', S)
    draw_char(ctx, FABRICE, 430, FLOOR - 60, 0.85, pose='hold', t=t, mouth='neutral', look=0.0)
    ctx.save(); ctx.translate(430, 1225); book(ctx, 0.9, BLUE, open_=True); ctx.restore()
    ctx.save(); ctx.translate(540, 1460); desk(ctx, 820); ctx.restore()
    ctx.save(); ctx.translate(800, 1340); book_stack(ctx, 0.9, 5); ctx.restore()
    ctx.save(); ctx.translate(170, 1350); lamp(ctx, 1.0); ctx.restore()
    # lamp light
    circle(ctx, 210, 1330, 260, '#FFE9A8', 0.10)
    ctx.save(); ctx.translate(250, 700); clock(ctx, 1.1, t * 3); ctx.restore()
    show(ctx, t, t_x - 0.15, W / 2, 1760, lambda c: pill(c, '100 % études', 0, 0, 48, BLUE), kind='up')

def sc_after(ctx, t, S):
    bg_soft(ctx, t, '#F2F6FF', '#DDE7FF', dots='#A9C2FF', floor='#CDD8F2', fy=1620)
    t_b = tw('business', S); t_a = tw('apres', S); t_d = tw('diplome', S)
    draw_char(ctx, FABRICE, 240, FLOOR, 0.82, pose='think', t=t, mouth='smile', look=0.8)
    def bub(c):
        thought_bubble(c, 820, 430, '#FFFFFF', tx=-1)
    show(ctx, t, S + 0.1, 600, 860, bub, kind='pop')
    show(ctx, t, t_d - 0.05, 380, 820, lambda c: (diploma_doc(c, 0.95), pill(c, '1. Diplôme', 0, 140, 32, PURPLE)), kind='pop')
    if t > t_a:
        arrow(ctx, 530, 820, 640, 820, NAVY, 12, 36, ease_out(prog(t, t_a, 0.4)))
    show(ctx, t, t_b, 820, 840, lambda c: (c.save(), c.scale(0.4, 0.4), shop_stand(c, 520, sign='BUSINESS', t=t), c.restore(),
                                         pill(c, '2. Business', 0, 120, 32, GREEN)), kind='pop')

def sc_years(ctx, t, S):
    bg_sky(ctx, t)
    t_o = tw('obtiennent', S); t_l = tw('licence', S)
    yrs = ['2023', '2024', '2025', '2026']
    k = int(clamp((t - S) / max(0.3, (t_o - S - 0.2)) * 3.999, 0, 3))
    def cal(c):
        calendar(c, 1.0, yrs[k], CORAL)
        if k < 3:
            ph = math.fmod((t - S) / max(0.3, (t_o - S - 0.2)) * 4, 1.0)
            if ph < 0.35:
                c.save(); c.translate(0, -30 - ph * 300); c.rotate(-ph * 2); c.scale(1, 1 - ph * 2)
                fill_rrect(c, -100, -10, 200, 140, 16, '#FFFFFF', 1 - ph * 2.5); c.restore()
    show(ctx, t, S, W / 2, 800, cal, kind='pop', t1=t_o - 0.1, out=0.3)
    show(ctx, t, S + 0.2, W / 2, 1030, lambda c: pill(c, '3 ans plus tard', 0, 0, 44, NAVY), kind='up', t1=t_o - 0.1)
    if t > t_o - 0.15:
        pe = ease_back(prog(t, t_o - 0.15, 0.5))
        draw_char(ctx, ELISEE, 310, FLOOR, 0.92 * max(pe, 0.01), pose='cheer' if t > t_l else 'idle', t=t, grad=True, mouth='big')
        draw_char(ctx, FABRICE, 770, FLOOR, 0.92 * max(pe, 0.01), pose='cheer' if t > t_l else 'idle', t=t, grad=True,
                  mouth='big', blink_seed=1)
        show(ctx, t, t_l, W / 2, 760, lambda c: pill(c, 'LICENCE OBTENUE !', 0, 0, 50, PURPLE), kind='pop')
        confetti(ctx, t, t_l, W / 2, 900, n=60, seed=2)

def sc_interesting(ctx, t, S):
    bg_grad(ctx, '#1E2450', '#2C3470')
    for x, c in ((310, '#FFFFFF'), (770, '#FFFFFF')):
        poly(ctx, [(x - 40, 520), (x + 40, 520), (x + 240, 1700), (x - 240, 1700)], c, 0.08)
        ellipse(ctx, x, 1690, 240, 40, c, 0.12)
    ctx.rectangle(0, 1700, W, 300); col(ctx, '#151A3D'); ctx.fill()
    t_i = tw('interessantes', S)
    draw_char(ctx, ELISEE, 310, 1690, 0.9, pose='shrug', t=t, grad=True, mouth='o', brows=1, look=0.4)
    draw_char(ctx, FABRICE, 770, 1690, 0.9, pose='shrug', t=t, grad=True, mouth='o', brows=1, look=-0.4, blink_seed=1)
    show(ctx, t, S + 0.2, W / 2, 790, lambda c: exclaim(c, 2.0 + 0.08 * math.sin(t * 8), ORANGE), kind='pop')
    for k, (x, y) in enumerate(((330, 700), (760, 660), (900, 900), (180, 940))):
        show(ctx, t, t_i - 0.4 + k * 0.1, x, y, lambda c: sparkle(c, 0.8 + 0.2 * math.sin(t * 6 + k)), kind='pop')

def sc_elisee_now(ctx, t, S):
    bg_sky(ctx, t, ground='#E8D3B0', ground2='#D9C29C')
    t_d = tw('diplome', S); t_x = tw('trois annees', S); t_c = tw('commerce', S)
    show(ctx, t, t_c - 0.4, 770, 1380, lambda c: big_shop(c, 520, t), kind='grow')
    h = draw_char(ctx, ELISEE, 300, FLOOR, 0.92, pose='present' if t > t_d else 'idle', t=t, mouth='big', look=0.6)
    if t > t_d:
        show(ctx, t, t_d, h['r'][0] + 10, h['r'][1] - 40, lambda c: diploma_doc(c, 0.55), kind='pop')
    show(ctx, t, t_d - 0.05, 600, 660, lambda c: row_item(c, lambda c3: diploma(c3, 0.5), 'Diplôme', w=600, h=130, ls=32, ok='check'), kind='left')
    show(ctx, t, t_x - 0.05, 600, 810, lambda c: row_item(c, lambda c3: text(c3, '+3', 0, 20, 56, GREEN, 'xbold'),
                                                         "ans d'expérience", w=600, h=130, ls=32, ok='check'), kind='left')

def sc_skills(ctx, t, S):
    bg_soft(ctx, t, '#EFFBF4', '#D7F2E3', dots='#7FD6AE', floor='#C4E8D3', fy=1680)
    draw_char(ctx, ELISEE, 170, 1740, 0.66, pose='present', t=t, mouth='big', look=0.8)
    rows = [('negocier', handshake, 'Négocier', 0.55), ('stocks', boxes, 'Gérer les stocks', 0.6),
            ('fideliser', heart, 'Fidéliser les clients', 0.7), ('depenses', receipt, 'Suivre ses dépenses', 0.55),
            ('calculer', calculator, 'Calculer ses bénéfices', 0.55)]
    for i, (q, fn, lab, sc) in enumerate(rows):
        ti = tw(q, S) - 0.1
        show(ctx, t, ti, 640, 650 + i * 182, lambda c, fn=fn, lab=lab, sc=sc:
             row_item(c, lambda c3: fn(c3, sc), lab, w=640, h=150, ls=34, ok='check'), kind='right')

def sc_fabrice_now(ctx, t, S):
    bg_soft(ctx, t, '#F2F6FF', '#DDE7FF', dots='#A9C2FF', floor='#CDD8F2', fy=1640)
    t_d = tw('diplome', S); t_t = tw('theoriques', S); t_m = tw('mais il decouvre', S); t_a = tw('affaires', S)
    pose = 'present' if t < t_m else 'scratch'
    h = draw_char(ctx, FABRICE, 300, FLOOR, 0.9, pose=pose, t=t, mouth='smile' if t < t_m else 'o',
                  brows=1 if t > t_m else 0, look=0.6)
    if t_d < t < t_m:
        show(ctx, t, t_d, h['r'][0] + 10, h['r'][1] - 40, lambda c: diploma_doc(c, 0.55), kind='pop')
    show(ctx, t, t_d - 0.05, 560, 660, lambda c: row_item(c, lambda c3: diploma(c3, 0.5), 'Diplôme', w=520, h=130, ok='check'),
         kind='left')
    show(ctx, t, t_t - 0.4, 560, 810, lambda c: row_item(c, lambda c3: book_stack(c3, 0.4, 3), 'Théorie', w=520, h=130, ok='check'),
         kind='left')
    show(ctx, t, t_a - 0.6, 800, 1300, lambda c: (big_shop(c, 380, t), pill(c, 'Monde des affaires', 0, 230, 32, GREEN)), kind='grow')
    for k, (x, y) in enumerate(((170, 960), (420, 920), (560, 1060))):
        show(ctx, t, t_m + 0.3 + k * 0.2, x, y + 10 * math.sin(t * 3 + k), lambda c: qmark(c, 0.75, PURPLE), kind='pop')

def sc_which(ctx, t, S):
    bg_soft(ctx, t, '#FFF4E6', '#FFE2C7', dots='#FFB98A', floor='#F2CFA9', fy=1620)
    t_m = tw('marche du travail', S)
    draw_char(ctx, ELISEE, 190, FLOOR, 0.78, t=t, look=0.6)
    draw_char(ctx, FABRICE, 890, FLOOR, 0.78, t=t, look=-0.6, blink_seed=1)
    name_tag(ctx, t, S, ELISEE, 190, 1060, 0.9)
    name_tag(ctx, t, S, FABRICE, 890, 1060, 0.9)
    tilt = 0.18 * math.sin(t * 2.4)
    show(ctx, t, S + 0.2, W / 2, 1180, lambda c: scale_balance(c, 1.25, tilt), kind='pop')
    show(ctx, t, tw('lequel', S), W / 2, 850, lambda c: qmark(c, 1.3, PURPLE), kind='pop')
    show(ctx, t, t_m - 0.1, W / 2, 680, lambda c: pill(c, 'MARCHÉ DU TRAVAIL', 0, 0, 44, NAVY), kind='down')

def sc_depends(ctx, t, S):
    bg_soft(ctx, t, '#F6F1FF', '#E6DCFF', dots='#C3A8FF')
    t_p = tw('poste', S); t_c = tw('competences', S)
    def jc(c):
        card(c, 640, 760, '#FFFFFF')
        fill_rrect(c, -320, -380, 640, 110, 34, PURPLE); fill_rrect(c, -320, -320, 640, 50, 0, PURPLE)
        text(c, "OFFRE D'EMPLOI", 0, -305, 44, '#FFFFFF', 'xbold')
        if t > t_p:
            a = ease_out(prog(t, t_p, 0.3))
            text(c, 'Poste :', -270, -190, 40, NAVY, 'xbold', align='l', a=a)
            fill_rrect(c, -270, -160, 420, 22, 11, '#E3E6F2'); fill_rrect(c, -270, -120, 300, 22, 11, '#E3E6F2')
        if t > t_c:
            text(c, 'Compétences recherchées :', -270, -30, 38, NAVY, 'xbold', align='l')
            for i in range(4):
                ti = t_c + 0.3 + i * 0.25
                if t > ti:
                    c.save(); c.translate(-240, 40 + i * 85); check(c, 0.55, GREEN if i % 2 == 0 else BLUE); c.restore()
                    fill_rrect(c, -190, 28 + i * 85, 300 - (i % 2) * 90, 24, 12, '#E3E6F2')
    show(ctx, t, S + 0.1, W / 2, 1150, jc, kind='up')
    mx = W / 2 + 200 * math.sin(t * 1.5); my = 1100 + 120 * math.cos(t * 1.1)
    show(ctx, t, S + 0.6, mx, my, lambda c: magnifier(c, 1.0), kind='pop')

def sc_hire(ctx, t, S):
    bg_room(ctx, wall='#EAF4FF', wall2='#D8E9FB', floor='#C9D7E8', window=False)
    t_a = tw('appreciera', S); t_d = tw('diplome', S); t_e = tw('experience', S)
    # frame
    fill_rrect(ctx, 640, 600, 300, 200, 14, '#FFFFFF'); fill_rrect(ctx, 655, 615, 270, 170, 8, '#B9E8D2')
    poly(ctx, [(655, 785), (760, 680), (840, 760), (880, 720), (925, 785)], GREEN)
    draw_char(ctx, RECRUITER, 790, FLOOR - 60, 0.85, pose='raiseR' if t > t_e + 0.5 else 'idle', t=t, mouth='big' if t > t_a else 'smile', look=-0.7)
    ctx.save(); ctx.translate(780, 1500); desk(ctx, 560); ctx.restore()
    show(ctx, t, S, 300, 1500, lambda c: (None), kind='fade')
    draw_char(ctx, ELISEE, 230, FLOOR + 30, 0.85, pose='holdR', t=t, mouth='smile', look=0.8)
    def cvc(c):
        cv(c, 1.0, ELISEE)
        if t > t_d:
            c.save(); c.translate(-95, -10); check(c, 0.5); c.restore()
            text(c, 'Diplôme', -60, 2, 30, NAVY, 'bold', align='l')
        if t > t_e:
            c.save(); c.translate(-95, 70); check(c, 0.5); c.restore()
            text(c, 'Expérience', -60, 82, 30, NAVY, 'bold', align='l')
            text(c, 'terrain', -60, 118, 30, '#168556', 'bold', align='l')
    show(ctx, t, S + 0.2, 470, 900, cvc, kind='pop')
    if t > t_a:
        for k in range(3):
            show(ctx, t, t_a + k * 0.15, 900 + (k - 1) * 70, 860 - (k % 2) * 50, lambda c: heart(c, 0.5), kind='pop')

def sc_dont_wait(ctx, t, S):
    bg_sky(ctx, t, sky1='#FFD9B0', sky2='#FFF1DE', ground='#F2CFA9', ground2='#E4BD93')
    t_at = tw('attendre', S); t_en = tw('entreprendre', S)
    def hg(c):
        hourglass(c, 1.4, clamp((t - S) / 4))
    show(ctx, t, S + 0.1, 290, 900, hg, kind='pop')
    show(ctx, t, t_at - 0.1, 290, 900, lambda c: big_x(c, 1.5, RED, prog(t, t_at - 0.1, 0.4)), kind='fade', dur=0.05)
    show(ctx, t, t_at, 290, 1160, lambda c: pill(c, "N'attends pas", 0, 0, 40, RED), kind='pop')
    if t > t_en - 0.2:
        p = prog(t, t_en - 0.2, 1.8)
        y = lerp(1300, 700, ease_in(p) * 0.6 + ease_out(p) * 0.4)
        for k in range(6):
            circle(ctx, 790 + math.sin(k * 2 + t * 8) * 10, y + 150 + k * 40, 26 - k * 3, '#FFFFFF', 0.7 - k * 0.1)
        ctx.save(); ctx.translate(790, y); rocket(ctx, 1.3); ctx.restore()
        show(ctx, t, t_en, 790, 1180, lambda c: pill(c, 'Entreprendre', 0, 0, 40, GREEN), kind='pop')
    draw_char(ctx, ELISEE, 540, FLOOR + 30, 0.72, pose='cheer' if t > t_en else 'point', t=t, mouth='big', look=0.6)

def sc_advantages(ctx, t, S):
    bg_soft(ctx, t, '#EFFBF4', '#D7F2E3', dots='#7FD6AE', floor='#C4E8D3', fy=1640)
    t_a = tw('avantages', S)
    show(ctx, t, S + 0.1, W / 2, 700, lambda c: pill(c, 'BUSINESS + ÉTUDES', 0, 0, 52, GREEN), kind='pop')
    show(ctx, t, t_a - 0.3, W / 2, 860, lambda c: text(c, 'LES AVANTAGES', 0, 30, 84, NAVY, 'xbold'), kind='up')
    for i in range(3):
        show(ctx, t, t_a + i * 0.18, W / 2 + (i - 1) * 200, 1040, lambda c, i=i: number_badge(c, i + 1, [CORAL, BLUE, PURPLE][i], 70), kind='pop')
    draw_char(ctx, ELISEE, W / 2, FLOOR + 40, 0.72, pose='cheer' if t > t_a else 'idle', t=t, mouth='big')

def sc_adv1(ctx, t, S):
    bg_soft(ctx, t, '#FFF8E6', '#FFEBC2', dots='#FFD266', floor='#F5DDA8', fy=1640)
    t_i = tw('independance', S); t_r = tw('reduire', S)
    headline(ctx, t, S, 1, 'Indépendance financière', CORAL)
    h = draw_char(ctx, ELISEE, 270, FLOOR, 0.86, pose='holdR' if t > t_i else 'idle', t=t, mouth='big', look=0.5)
    show(ctx, t, t_i, h['r'][0] + 20, h['r'][1] - 30, lambda c: wallet(c, 0.75), kind='pop')
    v = lerp(0.85, 0.18, ease_io(prog(t, t_r, 1.4)))
    def g(c):
        card(c, 400, 440, '#FFFFFF')
        c.save(); c.translate(0, -10); gauge(c, 1.2, v); c.restore()
        text(c, 'Dépendance', 0, 120, 34, NAVY, 'xbold')
        c.save(); c.translate(0, -150); parents(c, 0.55); c.restore()
    show(ctx, t, t_r - 0.6, 780, 1100, g, kind='pop')

def sc_adv2(ctx, t, S):
    bg_soft(ctx, t, '#EEF4FF', '#DBE6FF', dots='#A9C2FF', floor='#CDD8F2', fy=1660)
    headline(ctx, t, S, 2, 'Le monde des affaires', BLUE)
    tags = [('vendre', 'Vendre', GREEN, 300, 830), ('negocier', 'Négocier', PURPLE, 760, 860),
            ('budget', 'Gérer un budget', ORANGE, 400, 990), ('decisions', 'Prendre des décisions', BLUE, 600, 1120),
            ('difficultes', 'Faire face aux difficultés', CORAL, W / 2, 1260)]
    for q, lab, c, x, y in tags:
        ti = tw(q, S) - 0.1
        show(ctx, t, ti, x, y + 6 * math.sin(t * 2 + x), lambda c2, lab=lab, c=c: pill(c2, lab, 0, 0, 42, c), kind='pop')
    draw_char(ctx, ELISEE, 260, FLOOR + 60, 0.62, pose='present', t=t, mouth='big', look=0.6)
    ctx.save(); ctx.translate(800, 1560); big_shop(ctx, 330, t); ctx.restore()

def sc_adv3(ctx, t, S):
    bg_soft(ctx, t, '#F6F1FF', '#E6DCFF', dots='#C3A8FF', floor='#D9CCF5', fy=1680)
    t_c = tw('competences', S); t_k = tw('carriere', S)
    headline(ctx, t, S, 3, 'Compétences pratiques', PURPLE)
    labels = ['Études', 'Pratique', 'Emploi', 'Carrière']
    ctx.save(); ctx.translate(560, 1560); stairs(ctx, 1.0, 4, labels); ctx.restore()
    # climb
    span = max(0.5, t_k - S)
    step = clamp((t - S - 0.4) / span * 3.0, 0, 3)
    si = int(step); fr = step - si
    hop = math.sin(fr * math.pi) * 60 if si < 3 else 0
    x = 560 - 225 + step * 150
    y = 1560 - 0 - (si * 110 + (110 * ease_io(fr) if si < 3 else 0)) - hop
    draw_char(ctx, ELISEE, x, y, 0.55, pose='cheer' if step >= 3 else 'holdR', t=t, mouth='big', look=0.5,
              walk=(t * 2) if 0 < fr < 1 and si < 3 else None)
    show(ctx, t, t_k, 900, 900, lambda c: star(c, 1.4 + 0.1 * math.sin(t * 6)), kind='pop')
    show(ctx, t, t_c, 230, 900, lambda c: briefcase(c, 0.9), kind='pop')

def sc_attention(ctx, t, S):
    t_a = tw('attention', S); t_ab = tw('abandonner', S); t_ar = tw("l'argent", S)
    bg_soft(ctx, t, '#FFF0EE', '#FFD9D3', dots='#FF9C8F', floor='#F5C6BE', fy=1640)
    show(ctx, t, t_a - 0.15, W / 2, 1000, lambda c: warning(c, 1.8 + 0.06 * math.sin(t * 10)), kind='pop', t1=t_ab - 0.6)
    show(ctx, t, t_a, W / 2, 1300, lambda c: pill(c, 'ATTENTION !', 0, 0, 60, RED), kind='pop', t1=t_ab - 0.6)
    if t > t_ab - 0.6:
        # running after money, books dropping
        run = t - (t_ab - 0.6)
        xe = 340 + math.sin(run * 2) * 20
        for k in range(4):
            bx = 760 + k * 70 + math.sin(t * 3 + k) * 20
            by = 860 + math.sin(t * 4 + k * 1.3) * 50 - k * 30
            ctx.save(); ctx.translate(bx, by); ctx.rotate(math.sin(t * 5 + k) * 0.4); banknote(ctx, 0.7); ctx.restore()
        for k in range(3):
            ph = math.fmod(run * 0.9 + k * 0.33, 1.0)
            ctx.save(); ctx.translate(140 - k * 30, 1300 + ph * 300); ctx.rotate(ph * 3); book(ctx, 0.5, [BLUE, PURPLE, CORAL][k])
            ctx.restore()
        draw_char(ctx, ELISEE, xe, FLOOR, 0.82, pose='run', t=t, walk=t * 2.4, mouth='open', look=1.0, brows=0.5)
        show(ctx, t, t_ab - 0.5, W / 2, 680, lambda c: pill(c, "Abandonner ses études ?", 0, 0, 44, RED), kind='down')
        show(ctx, t, t_ab + 0.3, 900, 1330, lambda c: cross(c, 1.8), kind='pop')
        show(ctx, t, t_ar, 760, 1150, lambda c: text(c, 'NON !', 0, 0, 80, RED, 'xbold'), kind='pop')

def sc_tips(ctx, t, S):
    bg_soft(ctx, t, '#FFF8E6', '#FFEBC2', dots='#FFD266', floor='#F5DDA8', fy=1640)
    t_c = tw('conseils', S)
    show(ctx, t, S + 0.1, W / 2, 920, lambda c: bulb(c, 2.0, 0.6 + 0.4 * math.sin(t * 5)), kind='pop')
    show(ctx, t, t_c - 0.2, W / 2, 1220, lambda c: text(c, 'NOS CONSEILS', 0, 30, 84, NAVY, 'xbold'), kind='up')
    for i in range(4):
        show(ctx, t, t_c + 0.1 + i * 0.12, W / 2 + (i - 1.5) * 170, 1400,
             lambda c, i=i: number_badge(c, i + 1, [CORAL, BLUE, PURPLE, GREEN][i], 60), kind='pop')

def sc_tip1(ctx, t, S):
    bg_soft(ctx, t, '#EFFBF4', '#D7F2E3', dots='#7FD6AE', floor='#C4E8D3', fy=1660)
    t_p = tw('petit', S); t_c = tw('capital', S); t_b = tw('besoin autour', S); t_s = tw('solution', S)
    headline(ctx, t, S, 1, 'Commence petit', CORAL)
    show(ctx, t, t_p - 0.1, 330, 920, lambda c: plant(c, 0.9, 0.12), kind='grow')
    show(ctx, t, t_p, 330, 1100, lambda c: pill(c, 'Petit début', 0, 0, 34, GREEN), kind='pop')
    def cap(c):
        for k in range(5):
            c.save(); c.translate(0, 40 - k * 22); banknote(c, 0.9); c.restore()
    show(ctx, t, t_c - 0.3, 770, 900, cap, kind='pop')
    show(ctx, t, t_c, 860, 840, lambda c: cross(c, 1.0), kind='pop')
    show(ctx, t, t_c + 0.1, 770, 1100, lambda c: pill(c, 'Grand capital', 0, 0, 34, RED), kind='pop')
    show(ctx, t, t_b - 0.1, 330, 1380, lambda c: (magnifier(c, 0.9), pill(c, 'Un besoin', 0, 150, 32, PURPLE)), kind='pop')
    if t > t_b + 0.3: arrow(ctx, 470, 1390, 630, 1390, NAVY, 12, 36, ease_out(prog(t, t_b + 0.3, 0.4)))
    show(ctx, t, t_s - 0.15, 770, 1370, lambda c: (bulb(c, 0.8, 1.0), pill(c, 'Une solution', 0, 150, 32, ORANGE)), kind='pop')

def sc_tip2(ctx, t, S):
    bg_soft(ctx, t, '#EEF4FF', '#DBE6FF', dots='#A9C2FF', floor='#CDD8F2', fy=1660)
    t_c = tw('compatible', S); t_p = tw('priorite', S)
    headline(ctx, t, S, 2, 'Un emploi du temps compatible', BLUE, y=650) if False else headline(ctx, t, S, 2, 'Activité compatible', BLUE)
    show(ctx, t, S + 0.2, W / 2, 1040, lambda c: timetable(c, 1.1, t, t_c), kind='up')
    def leg(c):
        fill_rrect(c, -330, -22, 44, 44, 10, BLUE); text(c, 'Cours', -270, 14, 32, NAVY, 'bold', align='l')
        fill_rrect(c, -110, -22, 44, 44, 10, '#9DB7F5'); text(c, 'Révisions', -50, 14, 32, NAVY, 'bold', align='l')
        fill_rrect(c, 160, -22, 44, 44, 10, GREEN); text(c, 'Business', 220, 14, 32, NAVY, 'bold', align='l')
    show(ctx, t, t_c, W / 2, 1360, leg, kind='up')
    show(ctx, t, t_p - 0.2, W / 2, 1520, lambda c: (book_stack(c, 0.6, 3), None), kind='pop')
    show(ctx, t, t_p - 0.1, W / 2, 1720, lambda c: pill(c, 'ÉTUDES = PRIORITÉ', 0, 0, 46, NAVY), kind='up')

def sc_tip3(ctx, t, S):
    bg_soft(ctx, t, '#FFF0F4', '#FFDDE6', dots='#F7A1B5', floor='#F5C9D5', fy=1660)
    t_g = tw('argent', S); t_d = tw('depense', S); t_e = tw('epargne', S); t_r = tw('reinvestis', S)
    headline(ctx, t, S, 3, 'Gère ton argent', PURPLE)
    show(ctx, t, S + 0.2, 400, 1180, lambda c: piggy(c, 1.4), kind='pop')
    # don't spend everything: notes flying away, crossed
    if t_d - 0.1 < t < t_e:
        for k in range(3):
            ph = math.fmod((t - t_d) * 0.8 + k * 0.33, 1.0)
            ctx.save(); ctx.translate(700 + ph * 300, 900 - ph * 250 + k * 30); ctx.rotate(ph * 2); banknote(ctx, 0.7)
            ctx.restore()
        show(ctx, t, t_d + 0.2, 820, 980, lambda c: pill(c, 'Pas tout dépenser', 0, 0, 34, RED), kind='pop')
    if t > t_e:
        for k in range(4):
            ph = math.fmod((t - t_e) * 1.3 + k * 0.25, 1.0)
            ctx.save(); ctx.translate(400, 700 + ph * 300); coin(ctx, 0.8, t * 5 + k); ctx.restore()
        show(ctx, t, t_e, 400, 1440, lambda c: pill(c, 'Épargne', 0, 0, 38, PURPLE), kind='pop')
    if t > t_r - 0.1:
        arrow(ctx, 600, 1180, 720, 1180, NAVY, 12, 36, ease_out(prog(t, t_r - 0.1, 0.4)))
        show(ctx, t, t_r - 0.1, 880, 1200, lambda c: (big_shop(c, 280, t), pill(c, 'Réinvestis', 0, 200, 34, GREEN)), kind='pop')

def sc_tip4(ctx, t, S):
    bg_sky(ctx, t, ground='#A8DC8E')
    t_r = tw('riche', S); t_a = tw('apprendre', S); t_c = tw('construire', S); t_d = tw('durable', S)
    headline(ctx, t, S, 4, 'Sois patient', GREEN, y=650)
    show(ctx, t, t_r - 0.2, W / 2, 800, lambda c: (pill(c, 'Riche en 3 mois ?', 0, 0, 44, RED)), kind='pop', t1=t_a - 0.2)
    show(ctx, t, t_r + 0.3, W / 2 + 270, 800, lambda c: cross(c, 0.9), kind='pop', t1=t_a - 0.2)
    g = clamp((t - t_a + 0.3) / max(1.0, t_d - t_a + 0.3))
    ctx.save(); ctx.translate(300, 1500); plant(ctx, 1.0, 0.1 + 0.9 * ease_io(g)); ctx.restore()
    hp = clamp((t - t_c + 0.2) / max(0.6, t_d - t_c + 0.6))
    if t > t_c - 0.2:
        ctx.save(); ctx.translate(780, 1530); bricks_house(ctx, 1.0, hp); ctx.restore()
    show(ctx, t, t_d, 780, 1000, lambda c: pill(c, 'Durable', 0, 0, 44, GREEN), kind='pop')
    draw_char(ctx, ELISEE, 540, FLOOR + 140, 0.62, pose='hips', t=t, mouth='smile', look=0.3)

def sc_remember(ctx, t, S):
    t_p = tw('portes', S); t_m = tw('mais ton experience', S); t_av = tw("d'avance", S)
    if t < t_m:
        bg_soft(ctx, t, '#F6F1FF', '#E6DCFF', dots='#C3A8FF', floor='#D9CCF5', fy=1640)
        show(ctx, t, S + 0.1, W / 2, 680, lambda c: pill(c, 'RETIENS CECI', 0, 0, 46, PURPLE), kind='down')
        dp = ease_io(prog(t, t_p - 0.6, 0.9))
        ctx.save(); ctx.translate(W / 2, 1240); door(ctx, 1.6, dp); ctx.restore()
        show(ctx, t, tw('diplome', S), W / 2, 830, lambda c: diploma_doc(c, 0.8), kind='pop')
        draw_char(ctx, FABRICE, 200, FLOOR + 40, 0.7, pose='point', t=t, mouth='big', look=0.6)
    else:
        bg_sky(ctx, t, ground='#E07A5F', ground2='#C9674D')
        ctx.rectangle(0, 1560, W, 400); col(ctx, '#E07A5F'); ctx.fill()
        for k in range(3): line(ctx, 0, 1620 + k * 90, W, 1620 + k * 90, 6, '#FFFFFF', 0.7)
        # finish line
        for k in range(8):
            fill_rrect(ctx, 960, 1500 + k * 50, 30, 50, 0, NAVY if k % 2 else '#FFFFFF')
        run = t - t_m
        xf = 220 + run * 70; xe = 420 + run * 110
        draw_char(ctx, FABRICE, min(xf, 700), 1780, 0.6, pose='run', t=t, walk=t * 2.2, mouth='open', look=1, blink_seed=1)
        draw_char(ctx, ELISEE, min(xe, 880), 1700, 0.64, pose='run' if xe < 880 else 'cheer', t=t,
                  walk=t * 2.4 if xe < 880 else None, mouth='big', look=1)
        show(ctx, t, t_m, W / 2, 700, lambda c: pill(c, 'EXPÉRIENCE', 0, 0, 50, GREEN), kind='down')
        show(ctx, t, t_av - 0.2, W / 2, 840, lambda c: text(c, "Une longueur d'avance !", 0, 0, 56, NAVY, 'xbold'), kind='pop')

def sc_future(ctx, t, S):
    t_a = tw('avenir', S)
    sp = ease_out(prog(t, S, 3.5))
    bg_grad(ctx, '#FFB37A', '#FFE7C2', 0, 1300)
    circle(ctx, W / 2, 1300 - 220 * sp, 220, '#FFF3C4', 0.5); circle(ctx, W / 2, 1300 - 220 * sp, 160, '#FFD447')
    ctx.rectangle(0, 1250, W, 700); col(ctx, '#7BC47F'); ctx.fill()
    poly(ctx, [(W / 2 - 40, 1250), (W / 2 + 40, 1250), (W / 2 + 420, 1920), (W / 2 - 420, 1920)], '#5D6182')
    for k in range(6):
        y0 = 1270 + ((k * 120 + t * 160) % 700)
        w0 = 6 + (y0 - 1250) / 50
        line(ctx, W / 2, y0, W / 2, y0 + 20 + (y0 - 1250) / 12, w0, '#FFFFFF', 0.9)
    def sign(c):
        fill_rrect(c, -12, 0, 24, 220, 6, '#8C5A3C')
        poly(c, [(-150, -70), (110, -70), (160, 0), (110, 70), (-150, 70)], ORANGE)
        text(c, 'AVENIR', -20, 18, 48, '#FFFFFF', 'xbold')
    show(ctx, t, t_a - 0.4, 820, 1060, sign, kind='pop')
    draw_char(ctx, ELISEE, 420, 1820, 0.82, pose='wave', t=t, walk=t * 1.4, mouth='big', look=0.3)
    draw_char(ctx, FABRICE, 680, 1840, 0.82, pose='idle', t=t, walk=t * 1.4 + 0.3, mouth='smile', look=-0.3, blink_seed=1)
    show(ctx, t, tw('pourquoi', S), W / 2, 760, lambda c: qmark(c, 1.0, PURPLE), kind='pop', t1=t_a - 0.5)

def sc_end(ctx, t, S):
    sc_title(ctx, t, S, end=True)

# ---------------------------------------------------------- scene table
SCENES = [
    (0.0, sc_title, None),
    ('tu es etudiant', checklist_scene, None),
    ("voici l'histoire", sc_intro, None),
    ('elisee et fabrice frequentent', sc_same, None),
    ('mais contrairement', sc_contrary, None),
    ('en parallele', sc_shop, None),
    ('au debut', sc_hard, None),
    ('il doit jongler', sc_juggle, None),
    ('mais progressivement', sc_grow, None),
    ('avec ses benefices', sc_profits, None),
    ('pendant ce temps', sc_study, None),
    ('pour lui', sc_after, None),
    ('trois ans plus tard', sc_years, None),
    ('mais voila', sc_interesting, None),
    ('elisee a desormais', sc_elisee_now, None),
    ('il sait negocier', sc_skills, None),
    ('fabrice quant', sc_fabrice_now, None),
    ('alors entre les deux', sc_which, None),
    ('bien evidemment', sc_depends, None),
    ('mais une entreprise', sc_hire, None),
    ("et c'est justement", sc_dont_wait, None),
    ('avoir un business', sc_advantages, None),
    ('premierement cela', sc_adv1, None),
    ('deuxiemement tu decouvres', sc_adv2, None),
    ('troisiemement tu developpes', sc_adv3, None),
    ('mais attention', sc_attention, None),
    ('alors voici quelques', sc_tips, None),
    ('premierement commence', sc_tip1, None),
    ('deuxiemement choisis', sc_tip2, None),
    ('troisiemement apprends', sc_tip3, None),
    ('enfin sois', sc_tip4, None),
    ('et surtout', sc_remember, None),
    ('alors pourquoi', sc_future, None),
    ("un pied a l'ecole", sc_end, 120.0),
]

def scene_starts():
    out = []
    last = 0.0
    for q, fn, after in SCENES:
        if isinstance(q, float):
            s = q
        else:
            s = tw(q, after if after is not None else last) - 0.25
        out.append((s, fn))
        last = s + 0.3
    return out
