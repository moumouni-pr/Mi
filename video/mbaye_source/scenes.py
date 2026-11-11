import math, random
from engine import *
from chars import *
from icons import *

FLOOR = 1660

# ============================================================ characters
MBAYE = dict(name='Mbaye', skin='#7A4A2E', skin_d='#5f3822', shirt='#F59E0B', shirt_d='#D97F06',
             trim='#FFFFFF', pants='#263159', shoe='#FFFFFF', shoe2='#3C6FE0', hair='#1A1414',
             hair_style='flat', glasses=False, sleeves='short', collar=False, bag='#3C6FE0')
TRANSP = dict(name='', skin='#6B3E26', skin_d='#55301c', shirt='#2BB3C0', shirt_d='#1f8f9a', trim='#FFFFFF',
              pants='#3D405B', shoe='#3D405B', shoe2='#222222', hair='#120d0d', hair_style='round',
              glasses=False, sleeves='long', collar=True, bag=None)
GROSS = dict(name='', skin='#8A5534', skin_d='#6E4027', shirt='#7B4FD6', shirt_d='#6040AE', trim='#FFC93C',
             pants='#2B2D42', shoe='#2B2D42', shoe2='#1b1c2b', hair='#1A1414', hair_style='wrap', wrap='#FFC93C',
             glasses=False, sleeves='long', collar=False, bag=None, skirt=True)
BANKER = dict(name='', skin='#6B3E26', skin_d='#55301c', shirt='#2F3A5C', shirt_d='#232c47', trim='#FFFFFF',
              pants='#2F3A5C', shoe='#1b1c2b', shoe2='#111111', hair='#120d0d', hair_style='round',
              glasses=True, sleeves='long', collar=True, bag=None)
DAD = dict(DAD, hair='#555555')
POSES['sad'] = dict(la=4, le=2, ra=4, re=2)
POSES['phone'] = dict(la=8, le=4, ra=30, re=-125)
POSES['callR'] = dict(la=8, le=4, ra=20, re=-150)
POSES['stop'] = dict(la=8, le=4, ra=100, re=-60)
POSES['facepalm'] = dict(la=8, le=4, ra=35, re=-160)

# ============================================================ backgrounds
def bg_grad(ctx, c1, c2, y0=0, y1=H):
    g = cairo.LinearGradient(0, y0, 0, y1)
    g.add_color_stop_rgba(0, *hexc(c1)); g.add_color_stop_rgba(1, *hexc(c2))
    ctx.rectangle(0, 0, W, H); ctx.set_source(g); ctx.fill()

def bg_sky(ctx, t, ground='#A8DC8E', ground2='#93CF78', sky1='#9FD8FF', sky2='#E8F6FF', sun=True, gy=1500,
           clouds=True):
    bg_grad(ctx, sky1, sky2, 0, gy)
    if sun:
        circle(ctx, 880, 700, 90, '#FFE08A', 0.35); circle(ctx, 880, 700, 64, '#FFD447')
    if clouds:
        for i, (x0, y, s) in enumerate(((150, 640, 1.0), (620, 560, 0.8), (980, 900, 0.9))):
            x = (x0 + t * (14 + i * 6)) % (W + 400) - 200
            ctx.save(); ctx.translate(x, y); cloud(ctx, s, '#FFFFFF', 0.9); ctx.restore()
    ctx.rectangle(0, gy, W, H - gy); col(ctx, ground); ctx.fill()
    ctx.rectangle(0, gy, W, 24); col(ctx, ground2); ctx.fill()

def bg_soft(ctx, t, c1='#FFF4E6', c2='#FFE7D1', dots='#FFB98A', floor=None, fy=1600):
    bg_grad(ctx, c1, c2)
    rnd = random.Random(7)
    for i in range(14):
        x = rnd.uniform(0, W); y = rnd.uniform(560, 1800); r = rnd.uniform(6, 16)
        y += math.sin(t * 0.8 + i) * 8
        circle(ctx, x, y, r, dots, 0.35)
    if floor:
        ctx.rectangle(0, fy, W, H - fy); col(ctx, floor); ctx.fill()

def bg_sea(ctx, t, sky1='#9FD8FF', sky2='#E8F6FF', sea='#3C8DDB', sea2='#2F74BC', sy=1180, storm=False):
    bg_grad(ctx, sky1, sky2, 0, sy)
    ctx.rectangle(0, sy, W, H - sy); col(ctx, sea); ctx.fill()
    for k in range(7):
        y = sy + 40 + k * 110
        ctx.new_path()
        for x in range(-40, W + 60, 20):
            yy = y + math.sin(x / 70 + t * (2.2 if storm else 1.2) + k) * (14 if storm else 7)
            if x == -40: ctx.move_to(x, yy)
            else: ctx.line_to(x, yy)
        ctx.set_line_width(6); col(ctx, '#FFFFFF', 0.25); ctx.stroke()
    ctx.rectangle(0, sy, W, 16); col(ctx, sea2); ctx.fill()

def bg_night(ctx, t, floor='#3A3F6B', fy=1600):
    bg_grad(ctx, '#1E2350', '#3B3F7A', 0, fy)
    rnd = random.Random(3)
    for i in range(40):
        x = rnd.uniform(0, W); y = rnd.uniform(420, 1400)
        tw_ = 0.5 + 0.5 * math.sin(t * 2 + i)
        circle(ctx, x, y, rnd.uniform(2, 4.5), '#FFFFFF', 0.3 + 0.5 * tw_)
    circle(ctx, 850, 640, 70, '#FFF3C4'); circle(ctx, 880, 620, 62, '#1E2350')
    ctx.rectangle(0, fy, W, H - fy); col(ctx, floor); ctx.fill()

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

def shake(t, t0, d=0.5, amp=14):
    if t < t0 or t > t0 + d: return 0.0
    return math.sin((t - t0) * 60) * amp * (1 - (t - t0) / d)

def big_word(ctx, t, t0, s, y, c, size=110, bg=None, t1=None, kind='pop'):
    def f(c2):
        font(c2, size, 'xbold'); w = text_w(c2, s)
        if bg:
            fill_rrect(c2, -w / 2 - 50, -size * 0.95, w + 100, size * 1.35, 34, bg)
        c2.move_to(-w / 2, size * 0.1); col(c2, c); c2.show_text(s)
    show(ctx, t, t0, W / 2, y, f, kind=kind, t1=t1)

# ============================================================ new icons
def sneaker(ctx, s=1.0, c=CORAL, c2='#FFFFFF'):
    ctx.save(); ctx.scale(s, s)
    ctx.new_path(); ctx.move_to(-90, 20); ctx.line_to(-80, -40); ctx.curve_to(-60, -55, -30, -50, -20, -30)
    ctx.curve_to(10, -20, 60, -10, 90, 10); ctx.line_to(95, 30); ctx.line_to(-90, 30); ctx.close_path()
    col(ctx, c); ctx.fill()
    fill_rrect(ctx, -95, 18, 195, 26, 12, c2)
    for k in range(3): line(ctx, -50 + k * 18, -38 + k * 6, -38 + k * 18, -20 + k * 6, 5, c2)
    circle(ctx, -70, -10, 8, c2)
    ctx.restore()

def shoe(ctx, s=1.0, c='#8C5A3C'):
    ctx.save(); ctx.scale(s, s)
    ctx.new_path(); ctx.move_to(-90, 25); ctx.line_to(-85, -30); ctx.curve_to(-70, -40, -40, -40, -30, -20)
    ctx.curve_to(0, -12, 60, -8, 88, 12); ctx.line_to(90, 25); ctx.close_path(); col(ctx, c); ctx.fill()
    fill_rrect(ctx, -92, 20, 184, 14, 6, '#4A2E1C')
    fill_rrect(ctx, -92, 20, 34, 26, 4, '#4A2E1C')
    ctx.restore()

def headphones(ctx, s=1.0, c=PURPLE):
    ctx.save(); ctx.scale(s, s)
    ctx.new_path(); ctx.arc(0, 10, 70, math.pi, 2 * math.pi); ctx.set_line_width(16); col(ctx, NAVY); ctx.stroke()
    fill_rrect(ctx, -92, -5, 44, 76, 18, c); fill_rrect(ctx, 48, -5, 44, 76, 18, c)
    fill_rrect(ctx, -80, 5, 20, 56, 8, '#FFFFFF', 0.35); fill_rrect(ctx, 60, 5, 20, 56, 8, '#FFFFFF', 0.35)
    ctx.restore()

def money_bag(ctx, s=1.0, label='2 000 000 F'):
    ctx.save(); ctx.scale(s, s)
    ctx.new_path(); ctx.move_to(-40, -95); ctx.line_to(40, -95); ctx.line_to(22, -60); ctx.line_to(-22, -60)
    ctx.close_path(); col(ctx, '#C98B4B'); ctx.fill()
    ellipse(ctx, 0, 20, 120, 100, '#D9A066')
    line(ctx, -30, -62, 30, -62, 12, '#8C5A3C')
    text(ctx, 'F', 0, 48, 90, '#8C5A3C', 'xbold')
    if label:
        ctx.save(); ctx.translate(0, 150); pill(ctx, label, 0, 0, 40, GREEN); ctx.restore()
    ctx.restore()

def container(ctx, s=1.0, c=CORAL, label=None, open_=0.0):
    ctx.save(); ctx.scale(s, s)
    fill_rrect(ctx, -170, -80, 340, 160, 8, c)
    for k in range(9):
        x = -150 + k * 37
        line(ctx, x, -68, x, 68, 6, '#000000', 0.12)
    fill_rrect(ctx, -170, -80, 340, 14, 4, '#000000', 0.15)
    if label:
        fill_rrect(ctx, -90, -30, 180, 60, 10, '#FFFFFF', 0.9)
        text(ctx, label, 0, 13, 32, NAVY, 'xbold')
    if open_ > 0:
        fill_rrect(ctx, 170, -80, 90 * open_, 160, 6, c)
        line(ctx, 170, -80, 170, 80, 6, '#000000', 0.25)
    ctx.restore()

def ship(ctx, s=1.0, t=0.0, cargo=True, c=CORAL):
    ctx.save(); ctx.scale(s, s)
    ctx.rotate(math.sin(t * 1.8) * 0.03)
    if cargo:
        cs = [CORAL, BLUE, YELLOW, GREEN, PURPLE, TEAL]
        for r in range(2):
            for k in range(4 - r):
                fill_rrect(ctx, -170 + k * 85 + r * 40, -110 - r * 55, 80, 52, 5, cs[(k + r * 2) % 6])
    fill_rrect(ctx, 150, -200, 70, 145, 10, '#FFFFFF')
    fill_rrect(ctx, 160, -185, 50, 26, 5, '#BFE6FF')
    fill_rrect(ctx, 172, -250, 26, 55, 4, RED)
    poly(ctx, [(-250, -60), (260, -60), (210, 50), (-215, 50)], NAVY)
    fill_rrect(ctx, -240, -60, 495, 20, 4, RED)
    ctx.restore()

def truck(ctx, s=1.0, t=0.0, c=TEAL, label=None, move=False):
    ctx.save(); ctx.scale(s, s)
    fill_rrect(ctx, -230, -150, 300, 170, 14, '#FFFFFF')
    fill_rrect(ctx, -230, -150, 300, 170, 14, c, 0.18)
    if label: text(ctx, label, -80, -50, 40, NAVY, 'xbold')
    fill_rrect(ctx, 80, -100, 140, 120, 22, c)
    fill_rrect(ctx, 130, -88, 70, 50, 10, '#BFE6FF')
    fill_rrect(ctx, -235, 15, 460, 24, 10, '#4A4E69')
    for x in (-160, -60, 150):
        circle(ctx, x, 45, 38, '#2B2D42'); circle(ctx, x, 45, 16, '#C9CCD8')
        if move:
            a = t * 9
            line(ctx, x, 45, x + 14 * math.cos(a), 45 + 14 * math.sin(a), 5, '#2B2D42')
    ctx.restore()

def laptop(ctx, s=1.0, screen=BLUE, t=0.0):
    ctx.save(); ctx.scale(s, s)
    fill_rrect(ctx, -130, -110, 260, 170, 14, NAVY)
    fill_rrect(ctx, -116, -96, 232, 142, 8, screen)
    vals = [0.3, 0.5, 0.45, 0.75]
    for i, v in enumerate(vals):
        fill_rrect(ctx, -80 + i * 45, 30 - 100 * v, 30, 100 * v, 5, '#FFFFFF', 0.85)
    poly(ctx, [(-160, 60), (160, 60), (175, 85), (-175, 85)], '#C9CCD8')
    ctx.restore()

def bank(ctx, s=1.0):
    ctx.save(); ctx.scale(s, s)
    poly(ctx, [(-260, -170), (0, -290), (260, -170)], '#C9CCD8')
    fill_rrect(ctx, -250, -175, 500, 30, 6, '#AEB3C7')
    text(ctx, 'BANQUE', 0, -195, 44, NAVY, 'xbold')
    for k in range(5):
        fill_rrect(ctx, -220 + k * 100, -140, 40, 260, 6, '#E8EAF2')
    fill_rrect(ctx, -270, 120, 540, 40, 8, '#AEB3C7')
    ctx.restore()

def lightning(ctx, s=1.0, c=YELLOW):
    ctx.save(); ctx.scale(s, s)
    poly(ctx, [(10, -120), (-60, 10), (-5, 10), (-30, 120), (60, -30), (5, -30), (40, -120)], c)
    ctx.restore()

def stamp(ctx, label, c=RED, s=1.0, rot=-0.18):
    ctx.save(); ctx.scale(s, s); ctx.rotate(rot)
    font(ctx, 56, 'xbold'); w = text_w(ctx, label)
    rrect(ctx, -w / 2 - 30, -50, w + 60, 90, 14); ctx.set_line_width(9); col(ctx, c); ctx.stroke()
    ctx.move_to(-w / 2, 18); col(ctx, c); ctx.show_text(label)
    ctx.restore()

def order_ticket(ctx, s=1.0, n=1):
    ctx.save(); ctx.scale(s, s)
    fill_rrect(ctx, -90, -110, 180, 220, 14, '#FFFFFF')
    fill_rrect(ctx, -90, -110, 180, 50, 14, BLUE)
    text(ctx, f'Commande #{n}', 0, -76, 24, '#FFFFFF', 'xbold')
    for k in range(4): line(ctx, -60, -20 + k * 30, 60 - (k % 2) * 30, -20 + k * 30, 8, '#D6DBEA')
    ctx.restore()

def gauge_bar(ctx, w, h, p, c=GREEN, bgc='#E3E7F2', label=None):
    fill_rrect(ctx, -w / 2, -h / 2, w, h, h / 2, bgc)
    if p > 0.01: fill_rrect(ctx, -w / 2, -h / 2, max(h, w * p), h, h / 2, c)
    if label: text(ctx, label, 0, h * 0.18 + 6, h * 0.55, '#FFFFFF' if p > 0.5 else NAVY, 'xbold')

NIGER = [(0.18, 0.62), (0.22, 0.45), (0.38, 0.40), (0.55, 0.20), (0.75, 0.10), (0.92, 0.18), (0.95, 0.42),
         (0.85, 0.60), (0.70, 0.72), (0.48, 0.78), (0.30, 0.76)]

def niger_map(ctx, s=1.0, glow=1.0):
    ctx.save(); ctx.scale(s, s)
    pts = [(-260 + 520 * x, -200 + 400 * y) for x, y in NIGER]
    poly(ctx, [(p[0] + 10, p[1] + 14) for p in pts], '#000000', 0.10)
    poly(ctx, pts, '#FFB347')
    ctx.new_path(); ctx.move_to(*pts[0])
    for p in pts[1:]: ctx.line_to(*p)
    ctx.close_path(); ctx.set_line_width(8); col(ctx, '#FFFFFF'); ctx.stroke()
    text(ctx, 'NIGER', 60, 40, 64, NAVY, 'xbold')
    circle(ctx, -110, 70, 16 + 6 * glow, RED, 0.35); circle(ctx, -110, 70, 12, RED)
    ctx.restore()

def phone_big(ctx, t, t0, s=1.0, night=True):
    """Phone showing a vertical video feed that scrolls."""
    ctx.save(); ctx.scale(s, s)
    fill_rrect(ctx, -170, -330, 340, 660, 44, '#11142B')
    ctx.save(); rrect(ctx, -150, -300, 300, 600, 30); ctx.clip()
    off = ((t - t0) * 260) % 600 if t > t0 else 0
    cs = ['#FF6B57', '#3C6FE0', '#1FA971', '#7B4FD6', '#FF8A3D']
    for k in range(-1, 3):
        y = -300 + k * 600 - off + 600
        y = y - 600
        c = cs[(k + int(((t - t0) * 260) // 600 if t > t0 else 0)) % 5]
        ctx.rectangle(-150, y, 300, 600); col(ctx, c); ctx.fill()
        circle(ctx, 0, y + 260, 70, '#FFFFFF', 0.25)
        poly(ctx, [(-22, y + 230), (-22, y + 290), (30, y + 260)], '#FFFFFF')
        for j in range(3): circle(ctx, 115, y + 330 + j * 70, 20, '#FFFFFF', 0.85)
        fill_rrect(ctx, -125, y + 500, 170, 16, 8, '#FFFFFF', 0.8)
        fill_rrect(ctx, -125, y + 530, 120, 14, 7, '#FFFFFF', 0.6)
    ctx.restore()
    fill_rrect(ctx, -40, -318, 80, 12, 6, '#2C3157')
    ctx.restore()

def globe(ctx, s=1.0, t=0.0):
    ctx.save(); ctx.scale(s, s)
    circle(ctx, 0, 0, 150, '#3C8DDB')
    ctx.save(); ctx.new_path(); ctx.arc(0, 0, 150, 0, 2 * math.pi); ctx.clip()
    off = (t * 30) % 300
    for dx in (-300, 0, 300):
        x0 = dx - off
        poly(ctx, [(x0 - 80, -90), (x0 - 10, -110), (x0 + 20, -40), (x0 - 30, 30), (x0 - 70, -10)], '#5CC48A')
        poly(ctx, [(x0 + 60, -20), (x0 + 130, -40), (x0 + 150, 60), (x0 + 90, 110), (x0 + 50, 50)], '#5CC48A')
    ctx.restore()
    ctx.new_path(); ctx.arc(0, 0, 150, 0, 2 * math.pi); ctx.set_line_width(8); col(ctx, '#FFFFFF', 0.6); ctx.stroke()
    ctx.restore()

def snail(ctx, s=1.0, t=0.0):
    ctx.save(); ctx.scale(s, s)
    fill_rrect(ctx, -90, 20, 200, 40, 20, '#9BD18B')
    circle(ctx, 0, -10, 70, '#E8A55C'); circle(ctx, 0, -10, 45, '#F2C185'); circle(ctx, 0, -10, 20, '#E8A55C')
    line(ctx, 95, 25, 120, -30, 7, '#9BD18B'); line(ctx, 105, 25, 145, -20, 7, '#9BD18B')
    circle(ctx, 120, -32, 9, NAVY); circle(ctx, 146, -22, 9, NAVY)
    ctx.restore()

def bulb_sm(ctx, s, t):
    bulb(ctx, s, 0.6 + 0.4 * math.sin(t * 6))

# ================================================================= scenes
def sc_title(ctx, t, S):
    bg_grad(ctx, '#FFE9D6', '#FFD3B0')
    rnd = random.Random(2)
    for i in range(16):
        x = rnd.uniform(0, W); y = rnd.uniform(500, 1800); circle(ctx, x, y + math.sin(t + i) * 8, rnd.uniform(6, 15), '#FF8A3D', 0.25)
    # hill
    ctx.new_path(); ctx.move_to(0, 1700); ctx.line_to(W, 1250); ctx.line_to(W, H); ctx.line_to(0, H); ctx.close_path()
    col(ctx, '#F2B880'); ctx.fill()
    t1 = tw('abandonner', 0); t2 = tw('difficile', 0)
    def l1(c2):
        font(c2, 92, 'xbold'); s = 'DOIT-ON TOUT'
        c2.move_to(-text_w(c2, s) / 2, 0); col(c2, NAVY); c2.show_text(s)
    def l2(c2):
        font(c2, 104, 'xbold'); s = 'ABANDONNER ?'
        w = text_w(c2, s); fill_rrect(c2, -w / 2 - 40, -95, w + 80, 135, 30, RED)
        c2.move_to(-w / 2, 0); col(c2, '#FFFFFF'); c2.show_text(s)
    def l3(c2):
        font(c2, 50, 'bold'); s = 'quand tout devient difficile en business'
        c2.move_to(-text_w(c2, s) / 2, 0); col(c2, '#8A4B1C'); c2.show_text(s)
    show(ctx, t, 0.15, W / 2, 380, l1, kind='pop')
    show(ctx, t, t1, W / 2, 540, l2, kind='pop', dur=0.5)
    show(ctx, t, t2 - 0.2, W / 2, 680, l3, kind='up')
    # Mbaye pushing a big box up the hill
    x = 430 + 60 * ease_io(prog(t, 0.3, 3.0))
    yb = 1700 - (x / W) * 450
    ctx.save(); ctx.translate(x + 210, yb - 140); ctx.rotate(-0.4); boxes(ctx, 1.6); ctx.restore()
    draw_char(ctx, MBAYE, x, yb + 20, 0.78, pose='hold', t=t, mouth='open', brows=-0.6, tilt=-12,
              walk=t * 1.2)
    show(ctx, t, t2, x + 90, yb - 560, lambda c: sweat(c, 1.3), kind='pop')

def sc_intro(ctx, t, S):
    bg_sky(ctx, t, ground='#B9E3A4')
    t_m = tw('master', S); t_e = tw('entrepreneur', S); t_c = tw('chomeur', S); t_a = tw('attendre un emploi', S)
    t_g = tw('gagner sa vie', S)
    xm, wm = walk_x(t, S, 1.4, -200, 330)
    pose = 'wave' if t < t_c - 0.4 else ('shrug' if t < t_a else 'hips')
    draw_char(ctx, MBAYE, xm, FLOOR, 0.95, pose=pose, t=t, walk=wm, bag=True,
              mouth='big' if t < t_c else ('o' if t < t_a else 'smile'), look=0.5,
              brows=1.0 if t_c < t < t_a else 0)
    name_tag(ctx, t, S + 0.3, MBAYE, 330, 860, 1.25)
    t_out = t_c - 0.15
    show(ctx, t, t_m - 0.1, 770, 760, lambda c: icon_card(c, lambda c3: grad_cap(c3, 0.8), 'Master', 260, 240), kind='pop', t1=t_out)
    show(ctx, t, tw('marketing', S) - 0.05, 770, 1030, lambda c: icon_card(c, lambda c3: laptop(c3, 0.7), 'Marketing digital', 340, 240, ls=28), kind='pop', t1=t_out)
    show(ctx, t, t_e - 0.05, 770, 1260, lambda c: pill(c, 'Entrepreneur', 0, 0, 46, ORANGE), kind='pop', t1=t_out)
    # "chômeur" — the gossip
    def gossip(c):
        speech_bubble(c, 520, 170, '#FFFFFF', tail='br')
        text(c, '« Un chômeur ! »', 0, 18, 50, RED, 'xbold')
    show(ctx, t, t_c - 0.1, 720, 760, gossip, kind='pop', t1=t_a - 0.1)
    if t > t_c - 0.3:
        xc, wc = walk_x(t, t_c - 0.4, 0.8, 1300, 900)
        draw_char(ctx, CUST1, xc, FLOOR + 40, 0.7, pose='pointL', t=t, walk=wc, mouth='big', look=-0.8, blink_seed=2)
    # Not waiting for a job
    def job(c):
        card(c, 420, 170, '#FFFFFF', r=30)
        c.save(); c.translate(-140, 0); briefcase(c, 0.7); c.restore()
        text(c, 'Attendre', 50, -8, 40, NAVY, 'xbold'); text(c, 'un emploi', 50, 40, 34, '#6B7290', 'bold')
    show(ctx, t, t_a - 0.1, 720, 1080, job, kind='left')
    if t > t_a + 0.3:
        show(ctx, t, t_a + 0.3, 720, 1080, lambda c: big_x(c, 1.5, RED, prog(t, t_a + 0.3, 0.3)), kind='fade', dur=0.1)
    def life(c):
        card(c, 460, 160, '#E9F9F0', r=30)
        c.save(); c.translate(-160, 0); coin(c, 0.9, t * 4); c.restore()
        text(c, 'Gagner sa vie', 40, 14, 40, '#168556', 'xbold')
    show(ctx, t, t_g - 0.1, 720, 1300, life, kind='up')

def sc_project(ctx, t, S):
    bg_soft(ctx, t, '#EEF4FF', '#DCE7FF', dots='#9DB8FF', floor='#CFDBF5', fy=1620)
    t_c = tw('competences', S); t_p = tw('propre projet', S)
    draw_char(ctx, MBAYE, 300, FLOOR, 0.9, pose=pose_seq(t, [(S, 'think'), (t_p - 0.2, 'cheer')]), t=t,
              mouth='smile' if t < t_p else 'big', look=0.6)
    show(ctx, t, S + 0.1, 300, 760, lambda c: diploma_doc(c, 1.1, 'MASTER'), kind='pop', t1=t_c - 0.1)
    chips = [('Marketing', BLUE), ('Réseaux sociaux', PURPLE), ('Vente', GREEN)]
    for i, (lab, cc) in enumerate(chips):
        show(ctx, t, t_c + i * 0.25, 760, 720 + i * 120, lambda c, lab=lab, cc=cc: pill(c, lab, 0, 0, 40, cc), kind='left')
    if t > t_p - 0.3:
        arrow(ctx, 760, 1080, 760, 1200, NAVY, 12, 36, ease_out(prog(t, t_p - 0.3, 0.4)))
    def proj(c):
        card(c, 470, 220, '#FFFFFF', r=34)
        c.save(); c.translate(-150, 0); rocket(c, 0.6); c.restore()
        text(c, 'Son projet', 50, -5, 44, NAVY, 'xbold'); text(c, 'à lui !', 50, 50, 38, ORANGE, 'xbold')
    show(ctx, t, t_p, 760, 1330, proj, kind='pop')
    if t > t_p: confetti(ctx, t, t_p + 0.1, 760, 1250, n=24, seed=2, spread=360)

def store_stand(ctx, t, w=600, items=1.0, sign='MBAYE STORE'):
    s = w / 520
    ctx.save(); ctx.scale(s, s)
    line(ctx, -230, -260, -230, 150, 16, '#8C5A3C'); line(ctx, 230, -260, 230, 150, 16, '#8C5A3C')
    for i in range(8):
        c = ORANGE if i % 2 == 0 else '#FFFFFF'
        x = -260 + i * 65
        poly(ctx, [(x, -300), (x + 65, -300), (x + 65, -230), (x, -230)], c)
        ctx.new_path(); ctx.arc(x + 32.5, -230, 32.5, 0, math.pi); col(ctx, c); ctx.fill()
    fill_rrect(ctx, -270, -320, 540, 30, 10, '#D97F06')
    fill_rrect(ctx, -200, -400, 400, 70, 16, NAVY)
    text(ctx, sign, 0, -354, 34, '#FFFFFF', 'xbold')
    fill_rrect(ctx, -260, 0, 520, 170, 14, '#C98B5B')
    fill_rrect(ctx, -260, 0, 520, 26, 10, '#A86E44')
    fill_rrect(ctx, -200, 60, 400, 70, 12, '#B47A4E')
    text(ctx, 'Mode & Style', 0, 108, 32, '#FFF4E3', 'bold')
    ctx.restore()

def sc_brand(ctx, t, S):
    bg_sky(ctx, t, ground='#E8D3B0', ground2='#D9C29C', sky1='#FFD9B8', sky2='#FFF3E6')
    t_m = tw('marque', S)
    p = ease_back(prog(t, t_m - 0.1, 0.6))
    draw_char(ctx, MBAYE, 540, FLOOR - 30, 0.8, pose='present' if t > t_m else 'idle', t=t, mouth='big', look=0.4)
    if p > 0.01:
        ctx.save(); ctx.translate(540, 1500); ctx.scale(p, p); store_stand(ctx, t, 640); ctx.restore()
    items = [('vetements', lambda c: tshirt(c, 0.9, BLUE), 'Vêtements', 230, 760),
             ('chaussures', lambda c: shoe(c, 0.9), 'Chaussures', 850, 760),
             ('casques', lambda c: headphones(c, 0.9), 'Casques', 230, 1020),
             ('baskets', lambda c: sneaker(c, 0.95, CORAL), 'Baskets', 850, 1020)]
    for q, fn, lab, x, y in items:
        show(ctx, t, tw(q, S) - 0.1, x, y, lambda c, fn=fn, lab=lab: icon_card(c, fn, lab, 250, 230), kind='pop')

def sc_success(ctx, t, S):
    bg_soft(ctx, t, '#EFFBF4', '#D9F3E5', dots='#7FD6AE', floor='#CBEBD9', fy=1620)
    t_r = tw('reussir', S); t_c = tw('calculs', S); t_v = tw('ventes', S); t_ret = tw('retours', S)
    draw_char(ctx, MBAYE, 250, FLOOR, 0.82, pose='cheer' if t > t_r else 'idle', t=t, mouth='big', look=0.6)
    show(ctx, t, t_r - 0.1, 250, 820, lambda c: star(c, 1.2), kind='pop')
    rows = [(t_c, lambda c: calculator(c, 0.55), 'Calculs'), (t_v, lambda c: coin(c, 0.8, t * 3), 'Ventes'),
            (t_ret, lambda c: heart(c, 0.7), 'Clients')]
    for i, (ti, fn, lab) in enumerate(rows):
        show(ctx, t, ti - 0.1, 720, 760 + i * 190, lambda c, fn=fn, lab=lab: row_item(c, fn, lab, w=520, h=160, ok='check'), kind='left')
    if t > t_ret + 0.3:
        for k in range(5):
            show(ctx, t, t_ret + 0.3 + k * 0.12, 560 + k * 80, 1360, lambda c: star(c, 0.55), kind='pop')

def sc_growth(ctx, t, S):
    bg_sky(ctx, t, ground='#E8D3B0', ground2='#D9C29C')
    t_a = tw('ampleur', S)
    def chart(c):
        card(c, 420, 330, '#FFFFFF')
        vals = [0.2, 0.35, 0.55, 0.8]
        for i, v in enumerate(vals):
            g = ease_out(prog(t, S + 0.2 + i * 0.3, 0.5))
            hh = 230 * v * g
            fill_rrect(c, -160 + i * 90, 130 - hh, 62, hh, 10, ORANGE if i == 3 else '#FFC78F')
        arrow(c, -160, 80, 170, -120, GREEN, 12, 40, ease_out(prog(t, t_a - 0.3, 0.5)))
    show(ctx, t, S, 790, 790, chart, kind='pop')
    g = 0.75 + 0.25 * ease_out(prog(t, t_a - 0.3, 0.8))
    draw_char(ctx, MBAYE, 320, FLOOR - 120, 0.7, pose='wave', t=t, mouth='big')
    ctx.save(); ctx.translate(320, 1530); ctx.scale(g, g); store_stand(ctx, t, 520); ctx.restore()
    for k, (st, x0, d) in enumerate(((CUST1, 1300, 0.0), (CUST2, 1400, 0.4), (DAD, 1500, 0.8))):
        xc, wc = walk_x(t, S + d, 1.6, x0, 680 + k * 140)
        draw_char(ctx, st, xc, FLOOR + 40 + k * 10, 0.6, pose='holdR', t=t, walk=wc, look=-0.8, blink_seed=k)
    if t > t_a:
        for k in range(3):
            show(ctx, t, t_a + 0.12 * k, 220 + k * 100, 960 - (k % 2) * 40, lambda c: coin(c, 0.9, t * 4), kind='pop')

def sc_bascule(ctx, t, S):
    t_b = tw('bascule', S)
    dark = ease_out(prog(t, t_b - 0.1, 0.3))
    bg_grad(ctx, '#FFE7C7', '#FFD3A1')
    ctx.rectangle(0, 0, W, H); col(ctx, '#232846', 0.85 * dark); ctx.fill()
    ctx.rectangle(0, 1560, W, 400); col(ctx, '#3A3F6B' if dark > 0.5 else '#F2CFA9'); ctx.fill()
    rot = -0.35 * ease_back(prog(t, t_b, 0.6)) if t > t_b else 0
    ctx.save(); ctx.translate(560 + shake(t, t_b, 0.6, 18), 1560); ctx.rotate(rot); ctx.translate(0, -60)
    store_stand(ctx, t, 560); ctx.restore()
    draw_char(ctx, MBAYE, 250, FLOOR + 40, 0.8, pose='shrug' if t > t_b else 'idle', t=t,
              mouth='o' if t > t_b else 'smile', brows=1.2 if t > t_b else 0, look=0.7)
    show(ctx, t, t_b, 540, 760, lambda c: lightning(c, 1.6), kind='pop')
    show(ctx, t, t_b + 0.1, 820, 820, lambda c: exclaim(c, 1.6), kind='pop')
    big_word(ctx, t, t_b + 0.1, 'TOUT BASCULE !', 1040, '#FFFFFF', 86, bg=RED)

def sc_politics(ctx, t, S):
    bg_soft(ctx, t, '#F1EFFF', '#E1DCFA', dots='#B6A6F0')
    t_d = tw('decision politique', S); t_c = tw('commerce international', S)
    def doc(c):
        card(c, 380, 460, '#FFFFFF', r=24)
        text(c, 'DÉCISION', 0, -150, 48, NAVY, 'xbold')
        for k in range(5): line(c, -130, -80 + k * 45, 130 - (k % 2) * 60, -80 + k * 45, 10, '#E1E4EE')
        c.save(); c.translate(0, 150); stamp(c, 'OFFICIEL', PURPLE, 0.75); c.restore()
    show(ctx, t, t_d - 0.1, 300, 1000, doc, kind='down')
    show(ctx, t, t_c - 0.2, 780, 920, lambda c: globe(c, 1.2, t), kind='pop')
    if t > t_c:
        p = ease_out(prog(t, t_c, 0.5))
        for k, (a1, a2) in enumerate(((-2.4, -0.8), (0.7, 2.3))):
            ctx.new_path(); ctx.arc(780, 920, 230, a1, a1 + (a2 - a1) * p)
            ctx.set_line_width(12); ctx.set_dash([28, 18]); col(ctx, ORANGE); ctx.stroke(); ctx.set_dash([])
        show(ctx, t, t_c + 0.4, 780, 920, lambda c: cross(c, 1.6), kind='pop')
    show(ctx, t, t_c + 0.2, 780, 1260, lambda c: pill(c, 'Commerce bouleversé', 0, 0, 40, RED), kind='up')

def sc_delays(ctx, t, S):
    bg_sea(ctx, t, sy=1100)
    t_a = tw('allongent', S); t_t = tw('tardent', S); t_i = tw('impatienter', S)
    x = 300 + 40 * math.sin(t * 0.3)
    ctx.save(); ctx.translate(x, 1120); ship(ctx, 0.9, t); ctx.restore()
    show(ctx, t, S + 0.1, 820, 700, lambda c: (card(c, 300, 300, '#FFFFFF'), clock(c, 1.5, t * 4)), kind='pop')
    show(ctx, t, t_a - 0.1, 820, 920, lambda c: pill(c, 'Délais +++', 0, 0, 42, CORAL), kind='pop')
    show(ctx, t, t_t, 300, 860, lambda c: snail(c, 1.2, t), kind='pop')
    # impatient customers on the dock
    if t > t_i - 0.6:
        ctx.rectangle(560, 1500, 520, 420); col(ctx, '#C9A27A'); ctx.fill()
        for k, (st, x0) in enumerate(((CUST1, 680), (CUST2, 900))):
            draw_char(ctx, st, x0, 1800, 0.55, pose='hips', t=t, mouth='sad', brows=-1.0, look=-0.5, blink_seed=k)
        show(ctx, t, t_i - 0.2, 790, 1260, lambda c: (speech_bubble(c, 420, 130, '#FFFFFF', tail='bl'),
                                                     text(c, 'Ma commande ?!', 0, 14, 40, RED, 'xbold')), kind='pop')

def sc_orders(ctx, t, S):
    bg_soft(ctx, t, '#FFF1F0', '#FFE0DD', dots='#FF9E94', floor='#F7CFC9', fy=1620)
    t_a = tw('accumulent', S); t_s = tw('satisfaire', S)
    n = int(clamp((t - t_a + 0.2) / 0.18, 0, 14)) if t > t_a - 0.2 else 0
    rnd = random.Random(5)
    for k in range(n):
        x = 720 + rnd.uniform(-180, 180); y = 1480 - k * 52 + rnd.uniform(-10, 10)
        ctx.save(); ctx.translate(x, y); ctx.rotate(rnd.uniform(-0.3, 0.3)); order_ticket(ctx, 0.7, k + 1); ctx.restore()
    draw_char(ctx, MBAYE, 260, FLOOR, 0.85, pose='juggle' if t < t_s else 'facepalm', t=t, mouth='open' if t < t_s else 'sad',
              brows=-0.8, look=math.sin(t * 3) * 0.8)
    show(ctx, t, t_a, 260, 820, lambda c: sweat(c, 1.4), kind='pop')
    def counter(c):
        card(c, 380, 150, '#FFFFFF', r=30)
        text(c, f'{max(n, 1) * 7} commandes', 0, 14, 40, RED, 'xbold')
    show(ctx, t, t_a, 720, 700, counter, kind='down')
    show(ctx, t, t_s, 260, 1760, lambda c: pill(c, 'Débordé !', 0, 0, 44, RED), kind='up')

def sc_loan(ctx, t, S):
    bg_sky(ctx, t, ground='#C8D6E8', ground2='#B5C4DA', sky1='#CFE4FF', sky2='#F1F7FF')
    t_c = tw('convaincu', S); t_e = tw('emprunter', S); t_m = tw('millions', S); t_s = tw('augmenter son stock', S)
    ctx.save(); ctx.translate(540, 1380); bank(ctx, 1.25); ctx.restore()
    draw_char(ctx, MBAYE, 260, FLOOR + 20, 0.8, pose='cheer' if t < t_e else 'hold', t=t, mouth='big', look=0.7)
    show(ctx, t, t_c - 0.1, 260, 800, lambda c: (thought_bubble(c, 300, 150, '#FFFFFF', tx=-1),
                                                 text(c, 'Ça va', 0, -6, 40, NAVY, 'xbold'), text(c, 'cartonner !', 0, 40, 34, ORANGE, 'xbold')),
         kind='pop', t1=t_e - 0.1)
    xb, wb = walk_x(t, t_e - 0.3, 1.0, 1300, 820)
    draw_char(ctx, BANKER, xb, FLOOR + 20, 0.78, pose='holdR', t=t, walk=wb, look=-0.8, blink_seed=3)
    if t > t_m - 0.2:
        p = ease_out(prog(t, t_m - 0.2, 0.7))
        ctx.save(); ctx.translate(lerp(760, 300, p), lerp(1250, 1330, p) - math.sin(p * math.pi) * 160)
        money_bag(ctx, 0.75, None); ctx.restore()
    show(ctx, t, t_m, W / 2, 760, lambda c: pill(c, '2 000 000 F CFA', 0, 0, 56, GREEN), kind='pop')
    show(ctx, t, t_s - 0.1, 820, 900, lambda c: pill(c, '+ de stock', 0, 0, 40, ORANGE), kind='up')

def sc_error(ctx, t, S):
    bg_sea(ctx, t, sky1='#8E96B8', sky2='#C9CEE0', sea='#33689E', sea2='#28567F', sy=1150, storm=True)
    t_e = tw('erreur', S); t_s = tw('sous-estime', S); t_m = tw('maritime', S); t_g = tw('geopolitique', S)
    big_word(ctx, t, t_e - 0.05, 'ERREUR !', 740, '#FFFFFF', 110, bg=RED, t1=t_s - 0.1)
    show(ctx, t, S, 820, 1000, lambda c: (draw_char(c, MBAYE, 0, 200, 0.55, pose='hips', t=t, mouth='smile', look=-0.4)),
         kind='fade', t1=t_s - 0.1)
    ctx.save(); ctx.translate(380 + (t - S) * 12, 1170); ship(ctx, 0.85, t * 1.8); ctx.restore()
    show(ctx, t, t_s - 0.2, 400, 700, lambda c: rain_cloud(c, 2.0, t), kind='down')
    if t > t_s:
        show(ctx, t, t_s + 0.1, 800, 740, lambda c: lightning(c, 1.0), kind='pop')
    show(ctx, t, t_m - 0.1, 760, 1480, lambda c: row_item(c, lambda c3: warning(c3, 0.7), 'Risque maritime', w=560, h=140, ls=34), kind='left')
    show(ctx, t, t_g - 0.1, 760, 1660, lambda c: row_item(c, lambda c3: globe(c3, 0.32, t), 'Géopolitique', w=560, h=140, ls=34), kind='left')

def sc_year(ctx, t, S):
    bg_sea(ctx, t, sy=1250)
    t_r = tw('resultat', S); t_a = tw('pres', S); t_d = tw('destination', S)
    big_word(ctx, t, t_r - 0.05, 'RÉSULTAT ?', 700, PURPLE, 100)
    months = ['JAN', 'FÉV', 'MAR', 'AVR', 'MAI', 'JUIN', 'JUIL', 'AOÛT', 'SEPT', 'OCT', 'NOV', 'DÉC']
    if t > t_a - 0.2:
        k = int(clamp((t - t_a + 0.2) / ((t_d - t_a + 0.4) / 12), 0, 11))
        show(ctx, t, t_a - 0.2, 300, 1000, lambda c: calendar(c, 1.25, months[k], CORAL), kind='pop')
        show(ctx, t, t_a, 780, 1000, lambda c: pill(c, 'PRÈS D\'1 AN !', 0, 0, 56, RED), kind='pop')
    p = prog(t, S, 5.5)
    ctx.save(); ctx.translate(lerp(-150, 1000, p), 1260); ship(ctx, 0.7, t); ctx.restore()
    ctx.save(); ctx.translate(lerp(-100, 1050, p), 1440); snail(ctx, 0.8, t); ctx.restore()
    if t > t_d - 0.3:
        draw_char(ctx, MBAYE, 900, FLOOR + 230, 0.7, pose='facepalm', t=t, mouth='sad', brows=-1)

def sc_catastrophe(ctx, t, S):
    bg_sky(ctx, t, ground='#C9A27A', ground2='#B58F68', sky1='#C3CADB', sky2='#ECEFF5', sun=False)
    t_c = tw('catastrophe', S)
    o = ease_out(prog(t, t_c - 0.4, 0.6))
    ctx.save(); ctx.translate(560 + shake(t, t_c, 0.6, 16), 1380); container(ctx, 1.6, CORAL, 'STOCK', open_=o); ctx.restore()
    if t > t_c - 0.2:
        for k in range(5):
            ph = clamp((t - t_c + 0.2 - k * 0.08) * 1.3)
            ctx.save(); ctx.translate(840 + ph * (60 + k * 40), 1360 + ph * 160 - math.sin(ph * math.pi) * 180)
            ctx.rotate(ph * 3); shoe(ctx, 0.5, ['#8C5A3C', '#5A3A22', '#A0522D'][k % 3]); ctx.restore()
    draw_char(ctx, MBAYE, 170, FLOOR + 40, 0.72, pose='shrug', t=t, mouth='o', brows=1.2, look=0.8)
    big_word(ctx, t, t_c, 'CATASTROPHE !', 820, '#FFFFFF', 90, bg=RED)

def sc_fashion(ctx, t, S):
    bg_soft(ctx, t, '#F4F4F7', '#E4E6EE', dots='#B7BCCD', floor='#D5D8E3', fy=1640)
    t_m = tw('mode', S); t_h = tw('habitudes', S); t_an = tw('annulees', S)
    def old(c):
        card(c, 420, 280, '#FFFFFF')
        shoe(c, 1.1, '#8C5A3C')
        if t > t_m: c.save(); c.translate(0, 70); stamp(c, 'DÉMODÉ', RED, 0.75 * ease_back(prog(t, t_m, 0.4))); c.restore()
    show(ctx, t, S + 0.1, 290, 830, old, kind='pop')
    # customers walking away
    for k, (st, x0) in enumerate(((CUST1, 640), (CUST2, 860))):
        xc, wc = walk_x(t, t_h - 0.8 + k * 0.2, 1.8, x0, x0 + 600)
        draw_char(ctx, st, xc, FLOOR + 20, 0.65, pose='idle', t=t, walk=wc, look=0.8, blink_seed=k, mouth='neutral')
    show(ctx, t, t_h - 0.4, 760, 800, lambda c: pill(c, 'Nouvelles habitudes', 0, 0, 38, PURPLE), kind='pop', t1=t_an - 0.4)
    for k in range(3):
        def tk(c, k=k):
            order_ticket(c, 1.15, k + 3)
            if t > t_an + k * 0.15: stamp(c, 'ANNULÉE', RED, 0.6)
        show(ctx, t, t_an - 0.5 + k * 0.1, 300 + k * 240, 1280, tk, kind='up')

def sc_debt(ctx, t, S):
    bg_soft(ctx, t, '#FFF3EC', '#FFE1D2', dots='#FFB59A', floor='#EFCDBA', fy=1640)
    t_s = tw('enorme stock', S); t_d = tw('dette', S); t_v = tw('aucune vente', S)
    if t > t_s - 0.3:
        p = ease_out(prog(t, t_s - 0.3, 0.8))
        rnd = random.Random(9)
        for r in range(5):
            for k in range(4 - (r // 2)):
                if r * 4 + k > p * 18: continue
                ctx.save(); ctx.translate(560 + k * 130 + (r % 2) * 50, 1580 - r * 100); package(ctx, 0.85, ['#D9A066', '#CF9358', '#E0AA70'][(r + k) % 3]); ctx.restore()
    draw_char(ctx, MBAYE, 230, FLOOR, 0.8, pose='scratch', t=t, mouth='sad', brows=-1.0, look=0.6)
    def debt(c):
        card(c, 520, 170, '#FFFFFF', r=30)
        text(c, 'DETTE', 0, -25, 34, '#6B7290', 'bold')
        text(c, '- 2 000 000 F', 0, 40, 58, RED, 'xbold')
    show(ctx, t, t_d - 0.1, W / 2, 760, debt, kind='down')
    def sales(c):
        card(c, 520, 150, '#FFFFFF', r=30)
        text(c, 'Ventes :', -90, 16, 44, NAVY, 'xbold'); text(c, '0', 150, 20, 70, RED, 'xbold')
    show(ctx, t, t_v - 0.1, W / 2, 960, sales, kind='pop')

def sc_low(ctx, t, S):
    bg_grad(ctx, '#3B4166', '#5A6087')
    ctx.rectangle(0, 1600, W, 400); col(ctx, '#2F3455'); ctx.fill()
    t_b = tw('plus bas', S); t_q = tw('quoi faire', S); t_p = tw('tout perdu', S)
    draw_char(ctx, MBAYE, 540, FLOOR + 20, 0.95, pose='sad' if t < t_q else 'scratch', t=t, mouth='sad', brows=-1.2,
              look=-0.2, tilt=-8 if t < t_q else 0)
    show(ctx, t, S + 0.1, 540, 780, lambda c: rain_cloud(c, 1.8, t), kind='down')
    def meter(c):
        card(c, 220, 420, '#FFFFFF', r=30)
        fill_rrect(c, -40, -170, 80, 340, 40, '#E3E7F2')
        hh = 340 * (1 - 0.88 * ease_out(prog(t, t_b - 0.3, 0.8)))
        fill_rrect(c, -40, 170 - hh, 80, hh, 40, RED if hh < 120 else ORANGE)
        text(c, 'Moral', 0, 205, 30, NAVY, 'bold') if False else None
    show(ctx, t, S + 0.2, 880, 1100, meter, kind='left')
    show(ctx, t, S + 0.2, 880, 1360, lambda c: pill(c, 'Moral', 0, 0, 36, '#6B7290'), kind='left')
    for k, (dx, dy) in enumerate(((-260, 900), (230, 860), (-180, 1080))):
        show(ctx, t, t_q + k * 0.15, 540 + dx, dy, lambda c: qmark(c, 0.9, YELLOW), kind='pop', t1=t_p - 0.2)
    show(ctx, t, t_p - 0.1, 540, 1000, lambda c: pill(c, 'Tout perdu ?', 0, 0, 52, RED), kind='pop')

def sc_tiktok(ctx, t, S):
    bg_night(ctx, t, floor='#2F3455')
    t_f = tw('defiler', S); t_o = tw('opportunite', S)
    h = draw_char(ctx, MBAYE, 260, FLOOR, 0.85, pose='phone', t=t, mouth='neutral' if t < t_o else 'big',
                  look=0.9, brows=0 if t < t_o else 1.0)
    ctx.save(); ctx.translate(h['r'][0] + 6, h['r'][1] - 30); phone(ctx, 0.5, '#FF6B57'); ctx.restore()
    stop = t_o - 0.1
    tt = min(t, stop)
    show(ctx, t, S + 0.2, 720, 1080, lambda c: phone_big(c, tt, t_f - 0.2, 1.0), kind='up')
    if t > t_f: show(ctx, t, t_f, 720, 680, lambda c: pill(c, 'scroll... scroll...', 0, 0, 34, '#FFFFFF', NAVY), kind='pop', t1=stop)
    show(ctx, t, t_o - 0.1, 260, 700, lambda c: bulb_sm(c, 1.5, t), kind='pop')
    if t > t_o:
        show(ctx, t, t_o, 720, 1080, lambda c: (card(c, 300, 140, '#FFFFFF', r=26), text(c, 'OPPORTUNITÉ', 0, 14, 36, GREEN, 'xbold')), kind='pop')

def sc_niger(ctx, t, S):
    bg_soft(ctx, t, '#FFF8E7', '#FFEBC2', dots='#FFCB6B', floor=None)
    t_n = tw('nigerien', S); t_a = tw('articles', S); t_p = tw('prix', S)
    glow = 0.5 + 0.5 * math.sin(t * 5)
    show(ctx, t, t_n - 0.2, 600, 900, lambda c: niger_map(c, 1.3, glow), kind='pop')
    ctx.save(); ctx.translate(430, 1720); boxes(ctx, 1.1); ctx.restore()
    draw_char(ctx, MBAYE, 200, FLOOR + 200, 0.62, pose='point', t=t, mouth='big', look=0.9, brows=0.8)
    if t > t_a:
        arrow(ctx, 430, 1580, 470, 1080, ORANGE, 14, 44, ease_out(prog(t, t_a, 0.6)))
    def price(c):
        card(c, 400, 200, '#FFFFFF', r=30)
        text(c, 'Prix', -90, 20, 52, NAVY, 'xbold')
        arrow(c, 40, 50, 40, -50, GREEN, 14, 40, 1.0)
        text(c, '+++', 130, 20, 52, GREEN, 'xbold')
    show(ctx, t, t_p - 0.1, 760, 1450, price, kind='up')
    if t > t_p:
        for k in range(3):
            show(ctx, t, t_p + 0.15 * k, 640 + k * 130, 1640, lambda c: coin(c, 0.8, t * 4), kind='pop')

def sc_calm(ctx, t, S):
    bg_soft(ctx, t, '#EEF8FF', '#DCEFFF', dots='#92C7F0', floor='#CBE2F2', fy=1620)
    t_d = tw('decide', S); t_f = tw('foncer', S); t_t = tw('baissee', S)
    # the "head down" version (ghost) crashing into a wall
    def ghost():
        x, w_ = walk_x(t, t_f - 0.3, 0.7, 600, 820)
        draw_char(ctx, MBAYE, x, FLOOR - 10, 0.6, pose='run', t=t, walk=w_, mouth='big', tilt=20, look=1)
    if t > t_f - 0.4:
        fill_rrect(ctx, 930, 1060, 90, 560, 10, '#B4674B')
        for k in range(7): line(ctx, 930, 1120 + k * 75, 1020, 1120 + k * 75, 4, '#8F4F38')
        with_alpha(ctx, 0.5, ghost)
        show(ctx, t, t_t, 760, 1100, lambda c: big_x(c, 2.0, RED, prog(t, t_t, 0.3)), kind='fade', dur=0.1)
        show(ctx, t, t_t + 0.1, 760, 820, lambda c: pill(c, 'Foncer tête baissée', 0, 0, 38, RED), kind='pop')
    draw_char(ctx, MBAYE, 250, FLOOR, 0.9, pose='stop' if t > t_f - 0.2 else 'think', t=t, mouth='smile',
              look=0.6, brows=0.3)
    show(ctx, t, t_d - 0.1, 250, 760, lambda c: pill(c, 'Cette fois...', 0, 0, 40, BLUE), kind='pop')

def sc_plan(ctx, t, S):
    bg_soft(ctx, t, '#F3F7FF', '#E3ECFF', dots='#A9C2FF', floor='#D6E0F5', fy=1640)
    draw_char(ctx, MBAYE, 200, FLOOR, 0.75, pose='holdR', t=t, mouth='smile', look=0.8)
    show(ctx, t, S + 0.2, 200, 820, lambda c: clock(c, 0.9, t), kind='pop')
    rows = [('etudier', lambda c: magnifier(c, 0.55), 'Étudier le marché'),
            ('couts', lambda c: truck(c, 0.25, t), 'Coûts de transport'),
            ('evaluer', lambda c: warning(c, 0.6), 'Évaluer les risques'),
            ('budget', lambda c: calculator(c, 0.5), 'Budget prévisionnel')]
    for i, (q, fn, lab) in enumerate(rows):
        ti = tw(q, S) - 0.1
        def f(c, fn=fn, lab=lab, ti=ti):
            row_item(c, fn, lab, w=640, h=150, ls=32, ok='check' if t > ti + 0.7 else None)
        show(ctx, t, ti, 690, 720 + i * 180, f, kind='left')

def sc_contact(ctx, t, S):
    bg_sky(ctx, t, ground='#E8D3B0', ground2='#D9C29C', sky1='#FFE0B8', sky2='#FFF6EA')
    t_t = tw('transporteurs', S); t_g = tw('grossistes', S)
    draw_char(ctx, MBAYE, 200, FLOOR, 0.78, pose='callR', t=t, mouth='open' if math.sin(t * 7) > 0 else 'smile', look=0.8)
    ctx.save(); ctx.translate(250, 1060); phone(ctx, 0.45); ctx.restore()
    for k in range(3):
        a = clamp(math.fmod(t * 1.5 + k * 0.33, 1.0))
        ctx.new_path(); ctx.arc(250, 1020, 50 + a * 90, -1.0, 0.2); ctx.set_line_width(6); col(ctx, ORANGE, 1 - a); ctx.stroke()
    if t > t_t - 0.2:
        ctx.save(); ctx.translate(760, 1000); truck(ctx, 0.75, t, TEAL, 'TRANSPORT'); ctx.restore()
    show(ctx, t, t_t - 0.2, 760, 760, lambda c: pill(c, 'Transporteurs', 0, 0, 40, TEAL), kind='pop')
    xg, wg = walk_x(t, t_g - 0.5, 1.0, 1300, 700)
    if t > t_g - 0.6:
        draw_char(ctx, GROSS, xg, FLOOR + 40, 0.66, pose='wave', t=t, walk=wg, look=-0.8, mouth='smile', blink_seed=2)
        draw_char(ctx, TRANSP, xg + 230, FLOOR + 50, 0.62, pose='idle', t=t, walk=wg, look=-0.8, mouth='smile', blink_seed=4)
    show(ctx, t, t_g, 790, 1240, lambda c: pill(c, 'Grossistes du Niger', 0, 0, 40, PURPLE), kind='pop')

def sc_deal(ctx, t, S):
    bg_soft(ctx, t, '#EFFBF4', '#D9F3E5', dots='#7FD6AE', floor='#CBEBD9', fy=1640)
    t_c = tw('contre toute', S); t_i = tw('interesses', S); t_av = tw('avance', S); t_m = tw('montant total', S)
    draw_char(ctx, MBAYE, 230, FLOOR, 0.8, pose='cheer' if t > t_av else 'idle', t=t, mouth='big', look=0.7,
              brows=1.0 if t < t_i else 0)
    draw_char(ctx, GROSS, 860, FLOOR, 0.8, pose='wave' if t > t_i else 'idle', t=t, mouth='big', look=-0.7, blink_seed=2)
    show(ctx, t, t_c - 0.1, 230, 780, lambda c: exclaim(c, 1.2, ORANGE), kind='pop', t1=t_av)
    show(ctx, t, t_i - 0.2, W / 2, 1180, lambda c: handshake(c, 1.6), kind='pop')
    show(ctx, t, t_i, 860, 780, lambda c: heart(c, 1.0), kind='pop', t1=t_av)
    def adv(c):
        card(c, 620, 300, '#FFFFFF', r=34)
        text(c, 'AVANCE', 0, -70, 40, '#6B7290', 'bold')
        text(c, '25 %', 0, 30, 110, GREEN, 'xbold')
        c.save(); c.translate(0, 105); gauge_bar(c, 500, 34, 0.25 * ease_out(prog(t, t_m - 0.3, 0.8)), GREEN); c.restore()
    show(ctx, t, t_av - 0.1, W / 2, 800, adv, kind='pop')
    if t > t_av: confetti(ctx, t, t_av, W / 2, 800, n=40, seed=6)

def sc_export(ctx, t, S):
    bg_sky(ctx, t, ground='#E8D3B0', ground2='#D9C29C', sky1='#BDE5FF', sky2='#F3FAFF')
    t_f = tw('financer', S); t_e = tw('exportation', S)
    ctx.rectangle(0, 1480, W, 140); col(ctx, '#7A7F99'); ctx.fill()
    for k in range(6): fill_rrect(ctx, (k * 220 - t * 300) % (W + 220) - 110, 1545, 110, 14, 7, '#FFFFFF')
    x = lerp(-300, 1500, prog(t, S + 0.6, 5.2))
    ctx.save(); ctx.translate(x, 1420); truck(ctx, 1.0, t, ORANGE, 'EXPORT', move=True); ctx.restore()
    def pay(c):
        card(c, 520, 160, '#FFFFFF', r=30)
        c.save(); c.translate(-180, 0); banknote(c, 0.8); c.restore()
        text(c, 'Transport payé', 50, 14, 38, '#168556', 'xbold')
    show(ctx, t, t_f - 0.1, W / 2, 760, pay, kind='down')
    show(ctx, t, t_e - 0.3, W / 2, 960, lambda c: pill(c, 'Direction : NIGER', 0, 0, 52, ORANGE), kind='pop')

def sc_newstart(ctx, t, S):
    rise = ease_out(prog(t, S, 3.0))
    bg_grad(ctx, '#FFB37A', '#FFE7C2')
    circle(ctx, W / 2, lerp(1700, 1280, rise), 210, '#FFD447')
    ctx.rectangle(0, 1500, W, 420); col(ctx, '#7CC47F'); ctx.fill()
    t_e = tw('echec', S); t_a = tw('aventure', S)
    def fail(c):
        card(c, 300, 150, '#FFFFFF', r=28); text(c, 'Échec', 0, 16, 48, '#8A90B0', 'xbold')
    show(ctx, t, t_e - 0.1, 240, 800, fail, kind='pop')
    if t > t_e + 0.3: show(ctx, t, t_e + 0.3, 240, 800, lambda c: big_x(c, 1.2, RED, prog(t, t_e + 0.3, 0.3)), kind='fade', dur=0.1)
    if t > t_a - 0.6: arrow(ctx, 410, 800, 560, 800, NAVY, 12, 36, ease_out(prog(t, t_a - 0.6, 0.4)))
    def adv(c):
        card(c, 420, 220, '#FFFFFF', r=30)
        c.save(); c.translate(-140, 0); rocket(c, 0.55); c.restore()
        text(c, 'Nouvelle', 50, -10, 44, NAVY, 'xbold'); text(c, 'aventure', 50, 45, 44, ORANGE, 'xbold')
    show(ctx, t, t_a - 0.3, 790, 800, adv, kind='pop')
    draw_char(ctx, MBAYE, 540, FLOOR, 0.95, pose='cheer', t=t, mouth='big', look=0)

def sc_dream(ctx, t, S):
    bg_soft(ctx, t, '#F3EEFF', '#E4DAFF', dots='#B49BF0', floor='#D8CCF5', fy=1640)
    t_b = tw('boutique en ligne', S); t_n = tw('nourrit', S)
    def shop(c):
        card(c, 420, 340, '#FFFFFF', r=30)
        laptop(c, 1.0, ORANGE)
        text(c, 'Boutique en ligne', 0, 135, 32, NAVY, 'xbold')
    s_ = 1.0 - 0.45 * ease_io(prog(t, t_n - 0.3, 0.8))
    show(ctx, t, t_b - 0.3, lerp(720, 860, 1 - s_ if s_ < 1 else 0), 860, shop, kind='pop', base_scale=s_)
    draw_char(ctx, MBAYE, 250, FLOOR, 0.85, pose='think', t=t, mouth='smile', look=0.8)
    if t > t_n - 0.1:
        g = ease_back(prog(t, t_n - 0.1, 0.7))
        ctx.save(); ctx.translate(560, 1180); ctx.scale(g, g)
        thought_bubble(ctx, 560, 300, '#FFFFFF', tx=-1)
        text(ctx, 'PLUS GRAND !', 0, 20, 64, PURPLE, 'xbold')
        ctx.restore()

def sc_exporter(ctx, t, S):
    bg_sky(ctx, t, ground='#A8DC8E', ground2='#93CF78', sky1='#8FD0FF', sky2='#E8F6FF', sun=True)
    t_x = tw('exportateur', S); t_i = tw('international', S)
    show(ctx, t, S, W / 2, 1000, lambda c: globe(c, 1.6, t), kind='pop')
    if t > t_i - 0.4:
        for k in range(4):
            a = t * 0.9 + k * math.pi / 2
            x = W / 2 + 330 * math.cos(a); y = 1000 + 330 * math.sin(a) * 0.6
            ctx.save(); ctx.translate(x, y)
            if k % 2 == 0: ship(ctx, 0.22, t, cargo=True)
            else: container(ctx, 0.3, [BLUE, GREEN][k // 2])
            ctx.restore()
    xm, wm = walk_x(t, S, 1.2, -150, 220)
    h = draw_char(ctx, MBAYE, xm, FLOOR + 30, 0.8, pose='holdR' if t < t_x else 'cheer', t=t, walk=wm, mouth='big', look=0.7)
    if t < t_x:
        ctx.save(); ctx.translate(h['r'][0], h['r'][1] + 40); briefcase(ctx, 0.6); ctx.restore()
    big_word(ctx, t, t_x - 0.1, 'EXPORTATEUR', 700, '#FFFFFF', 90, bg=ORANGE)
    show(ctx, t, t_i - 0.1, 800, 1480, lambda c: pill(c, "À l'international", 0, 0, 44, BLUE), kind='up')

def sc_question(ctx, t, S):
    bg_soft(ctx, t, '#FFF4E6', '#FFE2C7', dots='#FFB98A', floor='#F2CFA9', fy=1640)
    t_a = tw('abandonner', S); t_d = tw('difficiles', S)
    draw_char(ctx, MBAYE, 540, FLOOR, 0.9, pose='think', t=t, mouth='neutral', look=0)
    show(ctx, t, S + 0.1, 540, 780, lambda c: qmark(c, 1.8, PURPLE), kind='pop')
    def sign(c, txt, cc, left):
        fill_rrect(c, -12, 0, 24, 300, 6, '#8C5A3C')
        if left: poly(c, [(-190, -70), (150, -70), (150, 50), (-190, 50), (-240, -10)], cc)
        else: poly(c, [(-150, -70), (190, -70), (240, -10), (190, 50), (-150, 50)], cc)
        text(c, txt, 0, 4, 40, '#FFFFFF', 'xbold')
    show(ctx, t, t_a - 0.1, 250, 1180, lambda c: sign(c, 'Abandonner', RED, True), kind='pop')
    show(ctx, t, t_d - 0.1, 830, 1180, lambda c: sign(c, 'Continuer', GREEN, False), kind='pop')

def sc_notnec(ctx, t, S):
    bg_soft(ctx, t, '#EFFBF4', '#D9F3E5', dots='#7FD6AE', floor='#CBEBD9', fy=1640)
    big_word(ctx, t, S + 0.1, 'PAS FORCÉMENT !', 800, '#FFFFFF', 92, bg=GREEN)
    draw_char(ctx, MBAYE, 540, FLOOR, 0.95, pose='point', t=t, mouth='big', look=0.3)
    show(ctx, t, S + 0.4, 820, 1020, lambda c: (card(c, 300, 130, '#FFFFFF', r=26), text(c, 'Abandonner', 0, 14, 38, RED, 'xbold'),
                                               big_x(c, 0.9, RED, prog(t, S + 0.6, 0.3))), kind='pop')

def sc_problem(ctx, t, S):
    bg_soft(ctx, t, '#F3F7FF', '#E3ECFF', dots='#A9C2FF', floor='#D6E0F5', fy=1640)
    t_p = tw('produit', S); t_m = tw('marche', S); t_s = tw('strategie', S); t_g = tw('gerer les risques', S)
    def prod(c):
        card(c, 380, 260, '#FFFFFF', r=30)
        sneaker(c, 0.9, CORAL)
        text(c, 'Ton produit', 0, 100, 32, NAVY, 'xbold')
        c.save(); c.translate(150, -95); check(c, 0.7); c.restore()
    show(ctx, t, t_p - 0.2, 300, 860, prod, kind='pop')
    draw_char(ctx, MBAYE, 250, FLOOR + 30, 0.66, pose='point', t=t, mouth='smile', look=0.8)
    rows = [(t_m, lambda c: niger_map(c, 0.17), 'Ton marché', BLUE), (t_s, lambda c: bulb(c, 0.5, 1.0), 'Ta stratégie', PURPLE),
            (t_g, lambda c: warning(c, 0.6), 'Gestion des risques', ORANGE)]
    for i, (ti, fn, lab, cc) in enumerate(rows):
        show(ctx, t, ti - 0.15, 740, 1080 + i * 180, lambda c, fn=fn, lab=lab, cc=cc: row_item(c, fn, lab, w=560, h=150, ls=32, lc=cc), kind='left')
    if t > t_m:
        ctx.save(); ctx.translate(980, 1000 + 40 * math.sin(t * 2)); magnifier(ctx, 0.9); ctx.restore()

def sc_good(ctx, t, S):
    bg_grad(ctx, '#FFE3B8', '#FFF6E8')
    ctx.rectangle(0, 1700, W, 300); col(ctx, '#F2CFA9'); ctx.fill()
    t_d = tw('difficultes', S); t_an = tw('analyser', S); t_ad = tw("s'adapter", S); t_s = tw('saisir', S)
    steps = [(t_an, 'Analyser', BLUE), (t_ad, "S'adapter", PURPLE), (t_s, 'Saisir sa chance', GREEN)]
    for i, (ti, lab, cc) in enumerate(steps):
        x = 330 + i * 250; hh = 200 + i * 180
        g = ease_out(prog(t, ti - 0.2, 0.5))
        if g > 0:
            fill_rrect(ctx, x - 115, 1700 - hh * g, 230, hh * g + 10, 18, cc)
            if g > 0.9:
                fs = 34 if len(lab) < 10 else 28
                if ' ' in lab and len(lab) > 10:
                    a_, b_ = lab.split(' ', 1)
                    text(ctx, a_, x, 1640 - 18, fs, '#FFFFFF', 'xbold'); text(ctx, b_, x, 1640 + 20, fs, '#FFFFFF', 'xbold')
                else:
                    text(ctx, lab, x, 1640, fs, '#FFFFFF', 'xbold')
    show(ctx, t, t_d - 0.2, 300, 800, lambda c: (rain_cloud(c, 1.2, t), text(c, 'Difficultés', 0, -60, 34, '#6B7290', 'xbold')), kind='pop', t1=t_an - 0.2)
    # Mbaye climbs
    lvl = 0
    for i, (ti, _, _) in enumerate(steps):
        if t > ti + 0.3: lvl = i + 1
    xs = [130, 330, 580, 830]; ys = [1700, 1500, 1320, 1140]
    k1 = max(0, lvl - 1)
    tl = steps[lvl - 1][0] + 0.3 if lvl > 0 else 0
    p = ease_io(prog(t, tl, 0.5)) if lvl > 0 else 1
    x = lerp(xs[k1] if lvl > 0 else xs[0], xs[lvl], p); y = lerp(ys[k1] if lvl > 0 else ys[0], ys[lvl], p) - math.sin(p * math.pi) * 80
    draw_char(ctx, MBAYE, x, y, 0.62, pose='cheer' if lvl == 3 else 'run', t=t, mouth='big', look=0.6,
              walk=t * 1.5 if 0 < p < 1 else None)
    if lvl == 3:
        confetti(ctx, t, t_s + 0.4, 830, 1000, n=50, seed=8)
        show(ctx, t, t_s + 0.5, W / 2, 720, lambda c: star(c, 1.6), kind='pop')

def sc_end(ctx, t, S):
    bg_grad(ctx, '#FFE9D6', '#FFD3B0')
    ctx.rectangle(0, 1600, W, 400); col(ctx, '#F2B880'); ctx.fill()
    def l1(c2):
        font(c2, 84, 'xbold'); s = "N'ABANDONNE PAS,"
        c2.move_to(-text_w(c2, s) / 2, 0); col(c2, NAVY); c2.show_text(s)
    def l2(c2):
        font(c2, 104, 'xbold'); s = 'ADAPTE-TOI !'
        w = text_w(c2, s); fill_rrect(c2, -w / 2 - 40, -95, w + 80, 135, 30, GREEN)
        c2.move_to(-w / 2, 0); col(c2, '#FFFFFF'); c2.show_text(s)
    show(ctx, t, S + 0.05, W / 2, 520, l1, kind='pop')
    show(ctx, t, S + 0.4, W / 2, 680, l2, kind='pop')
    draw_char(ctx, MBAYE, W / 2, FLOOR + 60, 0.95, pose='cheer', t=t, mouth='big', bag=True)
    confetti(ctx, t, S + 0.5, W / 2, 900, n=60, seed=4)

# ---------------------------------------------------------- scene table
SCENES = [
    (0.0, sc_title, None),
    ('mbaye est un', sc_intro, None),
    ('apres ses etudes', sc_project, None),
    ('il lance alors', sc_brand, None),
    ('au debut tout', sc_success, None),
    ('son petit business', sc_growth, None),
    ('mais un jour', sc_bascule, None),
    ('une decision politique', sc_politics, None),
    ("les delais d'approvisionnement", sc_delays, None),
    ("les commandes s'accumulent", sc_orders, None),
    ('convaincu du potentiel', sc_loan, None),
    ('mais il commet', sc_error, None),
    ('resultat', sc_year, None),
    ("et lorsqu'elle arrive", sc_catastrophe, None),
    ('les modeles de chaussures', sc_fashion, None),
    ('mbaye se retrouve', sc_debt, None),
    ('psychologiquement', sc_low, None),
    ('mais un soir', sc_tiktok, None),
    ('le marche nigerien', sc_niger, None),
    ('cette fois-ci', sc_calm, None),
    ('il prend le temps', sc_plan, None),
    ('il entre en contact', sc_contact, None),
    ('contre toute attente', sc_deal, None),
    ('cette avance', sc_export, None),
    ('finalement', sc_newstart, None),
    ('apres cette experience', sc_dream, None),
    ('devenir un veritable', sc_exporter, None),
    ('alors faut-il', sc_question, None),
    ('pas forcement', sc_notnec, None),
    ('parfois le probleme', sc_problem, None),
    ('un bon entrepreneur', sc_good, None),
    (190.25, sc_end, None),
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
