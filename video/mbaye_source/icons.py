import math
from engine import *

NAVY = '#1F2547'
GREEN = '#1FA971'
BLUE = '#3C6FE0'
CORAL = '#FF6B57'
YELLOW = '#FFC93C'
ORANGE = '#FF8A3D'
PURPLE = '#7B4FD6'
TEAL = '#2BB3C0'
CREAM = '#FFF8EC'
RED = '#E84A5F'

def card(ctx, w, h, c='#FFFFFF', r=34, sh=True):
    if sh: shadow(ctx, -w / 2, -h / 2, w, h, r)
    fill_rrect(ctx, -w / 2, -h / 2, w, h, r, c)

def icon_card(ctx, fn, label=None, w=230, h=230, c='#FFFFFF', lc=NAVY, ls=30):
    card(ctx, w, h, c)
    ctx.save(); ctx.translate(0, -18 if label else 0); fn(ctx); ctx.restore()
    if label:
        text(ctx, label, 0, h / 2 - 28, ls, lc, 'bold')

# ----------------------------------------------------------- buildings
def university(ctx, w=560):
    s = w / 560
    ctx.save(); ctx.scale(s, s)
    fill_rrect(ctx, -280, -40, 560, 300, 6, '#F4EFE6')
    poly(ctx, [(-310, -40), (0, -200), (310, -40)], '#E5DCCB')
    poly(ctx, [(-260, -55), (0, -180), (260, -55)], '#F4EFE6')
    text(ctx, 'UNIVERSITÉ', 0, -80, 38, NAVY, 'xbold')
    fill_rrect(ctx, -300, -50, 600, 22, 4, '#D9CDB6')
    for i in range(6):
        x = -225 + i * 90
        fill_rrect(ctx, x - 22, -20, 44, 250, 8, '#FFFFFF')
        line(ctx, x - 8, -10, x - 8, 220, 3, '#E7DFD0')
    fill_rrect(ctx, -330, 230, 660, 30, 4, '#D9CDB6')
    fill_rrect(ctx, -50, 110, 100, 120, 50, '#5B4B8A')
    ctx.restore()

def shop_stand(ctx, w=520, sign='ÉLISÉE ACCESSOIRES', t=0.0, items=True):
    s = w / 520
    ctx.save(); ctx.scale(s, s)
    # posts
    line(ctx, -230, -260, -230, 150, 16, '#8C5A3C'); line(ctx, 230, -260, 230, 150, 16, '#8C5A3C')
    # awning
    for i in range(8):
        c = GREEN if i % 2 == 0 else '#FFFFFF'
        x = -260 + i * 65
        poly(ctx, [(x, -300), (x + 65, -300), (x + 65, -230), (x, -230)], c)
        ctx.new_path(); ctx.arc(x + 32.5, -230, 32.5, 0, math.pi); col(ctx, c); ctx.fill()
    fill_rrect(ctx, -270, -320, 540, 30, 10, '#168556')
    # sign
    fill_rrect(ctx, -200, -400, 400, 70, 16, NAVY)
    text(ctx, sign, 0, -354, 30, '#FFFFFF', 'xbold')
    # counter
    fill_rrect(ctx, -260, 0, 520, 170, 14, '#C98B5B')
    fill_rrect(ctx, -260, 0, 520, 26, 10, '#A86E44')
    fill_rrect(ctx, -200, 60, 400, 70, 12, '#B47A4E')
    text(ctx, 'Accessoires téléphone', 0, 108, 28, '#FFF4E3', 'bold')
    if items:
        # items on counter
        ctx.save(); ctx.translate(-170, -50); phone_case(ctx, 0.55, CORAL); ctx.restore()
        ctx.save(); ctx.translate(-90, -50); phone_case(ctx, 0.55, BLUE); ctx.restore()
        ctx.save(); ctx.translate(-10, -50); phone_case(ctx, 0.55, YELLOW); ctx.restore()
        ctx.save(); ctx.translate(90, -40); earphones(ctx, 0.6); ctx.restore()
        ctx.save(); ctx.translate(185, -40); charger(ctx, 0.6); ctx.restore()
        # hanging items
        for i, c in enumerate([PURPLE, TEAL, ORANGE]):
            x = -150 + i * 150
            sw = math.sin(t * 2 + i) * 4
            line(ctx, x, -230, x + sw, -175, 3, '#8C5A3C')
            ctx.save(); ctx.translate(x + sw, -140); phone_case(ctx, 0.4, c); ctx.restore()
    ctx.restore()

def big_shop(ctx, w=600, t=0.0):
    s = w / 600
    ctx.save(); ctx.scale(s, s)
    fill_rrect(ctx, -300, -260, 600, 520, 10, '#FFFFFF')
    fill_rrect(ctx, -320, -330, 640, 90, 14, GREEN)
    text(ctx, 'ÉLISÉE ACCESSOIRES', 0, -270, 42, '#FFFFFF', 'xbold')
    for i in range(9):
        c = GREEN if i % 2 == 0 else '#E8FFF4'
        x = -300 + i * 66.6
        poly(ctx, [(x, -240), (x + 66.6, -240), (x + 66.6, -200), (x, -200)], c)
        ctx.new_path(); ctx.arc(x + 33.3, -200, 33.3, 0, math.pi); col(ctx, c); ctx.fill()
    fill_rrect(ctx, -260, -130, 330, 260, 14, '#CDEBF7')
    for r in range(3):
        fill_rrect(ctx, -250, -70 + r * 80, 310, 10, 4, '#9CC9DE')
        for k in range(5):
            cc = [CORAL, BLUE, YELLOW, PURPLE, TEAL][(k + r) % 5]
            fill_rrect(ctx, -235 + k * 58, -110 + r * 80, 34, 40, 8, cc)
    fill_rrect(ctx, 110, -110, 150, 370, 10, '#5B4B8A')
    circle(ctx, 135, 80, 10, YELLOW)
    ctx.restore()

def house_bg(ctx, w=300, c='#FFFFFF'):
    s = w / 300
    ctx.save(); ctx.scale(s, s)
    poly(ctx, [(-170, -40), (0, -180), (170, -40)], CORAL)
    fill_rrect(ctx, -140, -50, 280, 220, 8, c)
    fill_rrect(ctx, -40, 50, 80, 120, 10, '#8C5A3C')
    fill_rrect(ctx, -115, 0, 60, 60, 8, '#CDEBF7'); fill_rrect(ctx, 55, 0, 60, 60, 8, '#CDEBF7')
    ctx.restore()

# --------------------------------------------------------------- props
def phone(ctx, s=1.0, screen=TEAL):
    ctx.save(); ctx.scale(s, s)
    fill_rrect(ctx, -45, -85, 90, 170, 18, NAVY)
    fill_rrect(ctx, -37, -70, 74, 135, 10, screen)
    fill_rrect(ctx, -14, -80, 28, 6, 3, '#3a4170')
    ctx.restore()

def phone_case(ctx, s=1.0, c=CORAL):
    ctx.save(); ctx.scale(s, s)
    fill_rrect(ctx, -45, -80, 90, 160, 20, c)
    fill_rrect(ctx, -30, -64, 34, 44, 10, '#00000033' if False else NAVY)
    circle(ctx, -18, -50, 7, '#555c8a'); circle(ctx, -18, -32, 7, '#555c8a')
    circle(ctx, 18, 30, 16, '#FFFFFF', 0.4)
    ctx.restore()

def earphones(ctx, s=1.0):
    ctx.save(); ctx.scale(s, s)
    ctx.new_path(); ctx.move_to(-40, -40); ctx.curve_to(-40, 40, 40, 40, 40, -40)
    ctx.set_line_width(6); col(ctx, '#FFFFFF'); ctx.stroke()
    ctx.new_path(); ctx.move_to(0, 20); ctx.line_to(0, 70); ctx.set_line_width(6); ctx.stroke()
    for sx in (-40, 40):
        ellipse(ctx, sx, -50, 18, 24, '#FFFFFF'); ellipse(ctx, sx, -50, 18, 24, NAVY, 0.08)
    fill_rrect(ctx, -8, 60, 16, 26, 4, '#DADDEB')
    ctx.restore()

def charger(ctx, s=1.0):
    ctx.save(); ctx.scale(s, s)
    fill_rrect(ctx, -40, -50, 80, 70, 14, '#FFFFFF'); fill_rrect(ctx, -40, -50, 80, 70, 14, NAVY, 0.06)
    line(ctx, -14, -50, -14, -72, 8, '#B9BED3'); line(ctx, 14, -50, 14, -72, 8, '#B9BED3')
    ctx.new_path(); ctx.move_to(0, 20); ctx.curve_to(0, 60, 40, 40, 40, 80); ctx.set_line_width(7)
    col(ctx, '#FFFFFF'); ctx.stroke()
    poly(ctx, [(4, -40), (-12, -12), (2, -12), (-4, 10), (14, -20), (0, -20)], YELLOW)
    ctx.restore()

def book(ctx, s=1.0, c=BLUE, open_=False):
    ctx.save(); ctx.scale(s, s)
    if open_:
        poly(ctx, [(-90, -50), (0, -40), (0, 60), (-90, 50)], '#FFFFFF')
        poly(ctx, [(90, -50), (0, -40), (0, 60), (90, 50)], '#F3F0FF')
        for k in range(4):
            line(ctx, -75, -25 + k * 18, -15, -20 + k * 18, 4, '#C8CCE0')
            line(ctx, 15, -20 + k * 18, 75, -25 + k * 18, 4, '#C8CCE0')
        line(ctx, 0, -40, 0, 60, 4, c)
        poly(ctx, [(-95, 50), (0, 62), (95, 50), (95, 58), (0, 70), (-95, 58)], c)
    else:
        fill_rrect(ctx, -60, -80, 120, 160, 10, c)
        fill_rrect(ctx, -60, -80, 18, 160, 6, '#000000' if False else NAVY)
        fill_rrect(ctx, -30, -50, 70, 16, 6, '#FFFFFF')
        fill_rrect(ctx, 48, -74, 10, 148, 3, '#FFFFFF')
    ctx.restore()

def book_stack(ctx, s=1.0, n=4):
    ctx.save(); ctx.scale(s, s)
    cs = [BLUE, CORAL, YELLOW, GREEN, PURPLE, TEAL]
    for i in range(n):
        c = cs[i % len(cs)]
        w = 200 - (i % 2) * 20
        off = (i % 3 - 1) * 10
        fill_rrect(ctx, -w / 2 + off, 40 - i * 36, w, 34, 8, c)
        fill_rrect(ctx, w / 2 + off - 20, 46 - i * 36, 12, 22, 3, '#FFFFFF')
    ctx.restore()

def notes(ctx, s=1.0):
    ctx.save(); ctx.scale(s, s)
    fill_rrect(ctx, -60, -80, 120, 160, 12, '#FFFFFF')
    fill_rrect(ctx, -60, -80, 120, 160, 12, NAVY, 0.05)
    for k in range(5):
        line(ctx, -40, -45 + k * 25, 40 - (k % 2) * 20, -45 + k * 25, 6, '#AEB4D0')
    for k in range(4):
        circle(ctx, -40 + k * 27, -82, 7, NAVY)
    ctx.save(); ctx.translate(55, 50); ctx.rotate(-0.7); fill_rrect(ctx, -10, -60, 20, 100, 4, YELLOW)
    poly(ctx, [(-10, 40), (10, 40), (0, 60)], '#F3D6A4'); ctx.restore()
    ctx.restore()

def package(ctx, s=1.0, c='#D9A066'):
    ctx.save(); ctx.scale(s, s)
    fill_rrect(ctx, -70, -55, 140, 120, 10, c)
    poly(ctx, [(-70, -55), (70, -55), (55, -80), (-55, -80)], '#E8B97F')
    fill_rrect(ctx, -12, -80, 24, 145, 3, '#F5D9A8')
    fill_rrect(ctx, 22, 20, 36, 26, 4, '#FFFFFF')
    ctx.restore()

def person_icon(ctx, s=1.0, c=PURPLE):
    ctx.save(); ctx.scale(s, s)
    circle(ctx, 0, -35, 32, c)
    ctx.new_path(); ctx.arc(0, 60, 62, math.pi, 2 * math.pi); ctx.close_path(); col(ctx, c); ctx.fill()
    ctx.restore()

def coin(ctx, s=1.0, spin=0.0):
    ctx.save(); ctx.scale(s * max(0.15, abs(math.cos(spin))), s)
    circle(ctx, 0, 0, 40, '#F2A900'); circle(ctx, 0, 0, 31, YELLOW)
    text(ctx, 'F', 0, 14, 40, '#C98700', 'xbold')
    ctx.restore()

def banknote(ctx, s=1.0, c='#5CC48A'):
    ctx.save(); ctx.scale(s, s)
    fill_rrect(ctx, -80, -42, 160, 84, 10, c)
    fill_rrect(ctx, -68, -30, 136, 60, 8, '#FFFFFF', 0.25)
    circle(ctx, 0, 0, 22, '#FFFFFF', 0.6)
    text(ctx, 'F', 0, 12, 30, '#2E8B57', 'xbold')
    ctx.restore()

def bus(ctx, s=1.0):
    ctx.save(); ctx.scale(s, s)
    fill_rrect(ctx, -90, -60, 180, 110, 22, YELLOW)
    fill_rrect(ctx, -76, -46, 150, 44, 10, '#CDEBF7')
    line(ctx, -26, -46, -26, -2, 5, YELLOW); line(ctx, 24, -46, 24, -2, 5, YELLOW)
    fill_rrect(ctx, -90, 10, 180, 12, 4, ORANGE)
    circle(ctx, -50, 52, 20, NAVY); circle(ctx, 50, 52, 20, NAVY)
    circle(ctx, -50, 52, 8, '#B9BED3'); circle(ctx, 50, 52, 8, '#B9BED3')
    ctx.restore()

def plate(ctx, s=1.0):
    ctx.save(); ctx.scale(s, s)
    ellipse(ctx, 0, 20, 95, 40, '#FFFFFF'); ellipse(ctx, 0, 20, 95, 40, NAVY, 0.06)
    ellipse(ctx, 0, 16, 70, 28, '#FFFFFF')
    ellipse(ctx, -15, 4, 40, 20, '#F7E3A1')   # rice
    circle(ctx, 25, 0, 18, '#D9534F'); circle(ctx, 30, -10, 12, '#E56B47')
    circle(ctx, -30, -6, 8, GREEN); circle(ctx, 5, -8, 7, GREEN)
    line(ctx, 110, -30, 110, 50, 7, '#B9BED3'); line(ctx, -110, -30, -110, 50, 7, '#B9BED3')
    ctx.restore()

def supplies(ctx, s=1.0):
    ctx.save(); ctx.scale(s, s)
    ctx.save(); ctx.translate(-30, 0); notes(ctx, 0.75); ctx.restore()
    ctx.save(); ctx.translate(55, 5); ctx.rotate(0.25)
    fill_rrect(ctx, -12, -75, 24, 130, 4, CORAL); poly(ctx, [(-12, 55), (12, 55), (0, 82)], '#F3D6A4')
    poly(ctx, [(-4, 72), (4, 72), (0, 82)], NAVY); fill_rrect(ctx, -12, -85, 24, 14, 4, '#F2A2B0'); ctx.restore()
    ctx.restore()

def tshirt(ctx, s=1.0, c=PURPLE):
    ctx.save(); ctx.scale(s, s)
    poly(ctx, [(-40, -60), (-90, -30), (-70, 5), (-50, -5), (-50, 70), (50, 70), (50, -5), (70, 5),
               (90, -30), (40, -60), (20, -45), (-20, -45)], c)
    ctx.restore()

def parents(ctx, s=1.0):
    ctx.save(); ctx.scale(s, s)
    ctx.save(); ctx.translate(-40, 0); person_icon(ctx, 0.9, '#5C80BC'); ctx.restore()
    ctx.save(); ctx.translate(40, 10); person_icon(ctx, 0.8, '#E76F51'); ctx.restore()
    ctx.restore()

def lamp(ctx, s=1.0):
    ctx.save(); ctx.scale(s, s)
    ellipse(ctx, 0, 90, 50, 12, NAVY)
    line(ctx, 0, 90, -30, 10, 10, NAVY); line(ctx, -30, 10, 20, -50, 10, NAVY)
    ctx.save(); ctx.translate(30, -60); ctx.rotate(0.6)
    poly(ctx, [(-40, 0), (40, 0), (22, -50), (-22, -50)], CORAL); ctx.restore()
    ctx.restore()

def clock(ctx, s=1.0, t=0.0):
    ctx.save(); ctx.scale(s, s)
    circle(ctx, 0, 0, 70, NAVY); circle(ctx, 0, 0, 60, '#FFFFFF')
    for k in range(12):
        a = k * math.pi / 6
        line(ctx, 50 * math.sin(a), -50 * math.cos(a), 56 * math.sin(a), -56 * math.cos(a), 4, NAVY)
    a1 = t * 2.0; a2 = t * 0.3
    line(ctx, 0, 0, 40 * math.sin(a1), -40 * math.cos(a1), 6, NAVY)
    line(ctx, 0, 0, 28 * math.sin(a2), -28 * math.cos(a2), 8, CORAL)
    circle(ctx, 0, 0, 7, NAVY)
    ctx.restore()

def calendar(ctx, s=1.0, label='2024', c=CORAL):
    ctx.save(); ctx.scale(s, s)
    fill_rrect(ctx, -110, -110, 220, 230, 24, '#FFFFFF')
    ctx.new_path(); rrect(ctx, -110, -110, 220, 80, 24); col(ctx, c); ctx.fill()
    fill_rrect(ctx, -110, -60, 220, 30, 0, c)
    line(ctx, -55, -130, -55, -90, 14, NAVY); line(ctx, 55, -130, 55, -90, 14, NAVY)
    text(ctx, label, 0, 60, 72, NAVY, 'xbold')
    ctx.restore()

def diploma(ctx, s=1.0):
    ctx.save(); ctx.scale(s, s)
    fill_rrect(ctx, -90, -30, 180, 60, 30, '#FFF6E0')
    ellipse(ctx, 90, 0, 14, 30, '#F1E2BC')
    fill_rrect(ctx, -12, -32, 24, 64, 2, RED)
    poly(ctx, [(-8, 30), (8, 30), (16, 70), (0, 58), (-16, 70)], RED)
    ctx.restore()

def diploma_doc(ctx, s=1.0, label='LICENCE'):
    ctx.save(); ctx.scale(s, s)
    fill_rrect(ctx, -120, -85, 240, 170, 12, '#FFF6E0')
    ctx.new_path(); rrect(ctx, -108, -73, 216, 146, 8); ctx.set_line_width(4); col(ctx, '#E5C66E'); ctx.stroke()
    text(ctx, 'DIPLÔME', 0, -30, 30, NAVY, 'xbold')
    text(ctx, label, 0, 8, 22, '#8B7A55', 'bold')
    circle(ctx, 70, 45, 22, RED); poly(ctx, [(60, 60), (66, 92), (72, 80), (80, 92), (80, 60)], RED)
    line(ctx, -80, 50, 20, 50, 4, '#C8B98F')
    ctx.restore()

def grad_cap(ctx, s=1.0):
    ctx.save(); ctx.scale(s, s)
    poly(ctx, [(-110, -10), (0, -55), (110, -10), (0, 35)], NAVY)
    ctx.new_path(); ctx.move_to(-60, 15); ctx.line_to(-60, 55); ctx.curve_to(-30, 80, 30, 80, 60, 55); ctx.line_to(60, 15)
    ctx.line_to(0, 35); ctx.close_path(); col(ctx, '#2C3366'); ctx.fill()
    line(ctx, 0, -10, 80, 10, 5, YELLOW); line(ctx, 80, 10, 80, 60, 5, YELLOW); circle(ctx, 80, 64, 9, YELLOW)
    ctx.restore()

def sparkle(ctx, s=1.0, c=YELLOW):
    ctx.save(); ctx.scale(s, s)
    ctx.new_path(); ctx.move_to(0, -40)
    for k in range(4):
        a = k * math.pi / 2
        ctx.curve_to(6 * math.cos(a + 0.8), 6 * math.sin(a + 0.8) * 1, 6 * math.cos(a + 0.8), 6 * math.sin(a + 0.8),
                     40 * math.sin(a + math.pi / 2), -40 * math.cos(a + math.pi / 2))
    ctx.close_path(); col(ctx, c); ctx.fill()
    ctx.restore()

def star(ctx, s=1.0, c=YELLOW):
    ctx.save(); ctx.scale(s, s)
    pts = []
    for k in range(10):
        r = 50 if k % 2 == 0 else 22
        a = -math.pi / 2 + k * math.pi / 5
        pts.append((r * math.cos(a), r * math.sin(a)))
    poly(ctx, pts, c); ctx.restore()

def check(ctx, s=1.0, c=GREEN):
    ctx.save(); ctx.scale(s, s)
    circle(ctx, 0, 0, 40, c)
    ctx.new_path(); ctx.move_to(-18, 0); ctx.line_to(-5, 14); ctx.line_to(20, -14)
    ctx.set_line_width(9); ctx.set_line_cap(1); ctx.set_line_join(1); col(ctx, '#FFFFFF'); ctx.stroke()
    ctx.restore()

def cross(ctx, s=1.0, c=RED):
    ctx.save(); ctx.scale(s, s)
    circle(ctx, 0, 0, 40, c)
    line(ctx, -15, -15, 15, 15, 9, '#FFFFFF'); line(ctx, 15, -15, -15, 15, 9, '#FFFFFF')
    ctx.restore()

def big_x(ctx, s=1.0, c=RED, p=1.0):
    ctx.save(); ctx.scale(s, s)
    p1 = clamp(p * 2); p2 = clamp(p * 2 - 1)
    if p1 > 0: line(ctx, -100, -100, -100 + 200 * p1, -100 + 200 * p1, 34, c)
    if p2 > 0: line(ctx, 100, -100, 100 - 200 * p2, -100 + 200 * p2, 34, c)
    ctx.restore()

def qmark(ctx, s=1.0, c=PURPLE):
    ctx.save(); ctx.scale(s, s)
    circle(ctx, 0, 0, 55, c)
    text(ctx, '?', 0, 30, 84, '#FFFFFF', 'xbold')
    ctx.restore()

def exclaim(ctx, s=1.0, c=CORAL):
    ctx.save(); ctx.scale(s, s)
    circle(ctx, 0, 0, 55, c)
    text(ctx, '!', 0, 30, 84, '#FFFFFF', 'xbold')
    ctx.restore()

def bulb(ctx, s=1.0, glow=1.0):
    ctx.save(); ctx.scale(s, s)
    if glow > 0:
        for k in range(8):
            a = k * math.pi / 4
            line(ctx, 85 * math.cos(a), -20 + 85 * math.sin(a), 110 * math.cos(a), -20 + 110 * math.sin(a), 9, YELLOW, glow)
        circle(ctx, 0, -20, 75, YELLOW, 0.25 * glow)
    circle(ctx, 0, -20, 58, YELLOW)
    fill_rrect(ctx, -26, 30, 52, 44, 10, '#9AA0BF')
    line(ctx, -24, 46, 24, 46, 5, '#7A809F'); line(ctx, -24, 60, 24, 60, 5, '#7A809F')
    ctx.new_path(); ctx.move_to(-16, 20); ctx.line_to(-8, -20); ctx.line_to(0, 0); ctx.line_to(8, -20); ctx.line_to(16, 20)
    ctx.set_line_width(5); col(ctx, ORANGE); ctx.stroke()
    ctx.restore()

def warning(ctx, s=1.0):
    ctx.save(); ctx.scale(s, s)
    ctx.new_path(); ctx.move_to(0, -100); ctx.line_to(110, 85); ctx.line_to(-110, 85); ctx.close_path()
    ctx.set_line_join(1); ctx.set_line_width(30); col(ctx, YELLOW); ctx.stroke_preserve(); ctx.fill()
    fill_rrect(ctx, -11, -45, 22, 80, 11, NAVY); circle(ctx, 0, 62, 13, NAVY)
    ctx.restore()

def handshake(ctx, s=1.0):
    ctx.save(); ctx.scale(s, s)
    line(ctx, -110, 20, -30, -5, 42, GREEN); line(ctx, 110, 20, 30, -5, 42, PURPLE)
    ellipse(ctx, 0, -5, 48, 30, '#8A5534')
    for k in range(3): line(ctx, -20 + k * 18, -28, -16 + k * 18, 10, 4, '#6E4027')
    ctx.restore()

def boxes(ctx, s=1.0):
    ctx.save(); ctx.scale(s, s)
    ctx.save(); ctx.translate(-50, 30); package(ctx, 0.6); ctx.restore()
    ctx.save(); ctx.translate(50, 30); package(ctx, 0.6, '#CF9358'); ctx.restore()
    ctx.save(); ctx.translate(0, -40); package(ctx, 0.6, '#E0AA70'); ctx.restore()
    ctx.restore()

def heart(ctx, s=1.0, c=RED):
    ctx.save(); ctx.scale(s, s)
    ctx.new_path(); ctx.move_to(0, 50)
    ctx.curve_to(-90, -10, -50, -80, 0, -35); ctx.curve_to(50, -80, 90, -10, 0, 50)
    col(ctx, c); ctx.fill(); ctx.restore()

def receipt(ctx, s=1.0):
    ctx.save(); ctx.scale(s, s)
    pts = [(-55, -80), (55, -80), (55, 80)]
    for k in range(6): pts.append((55 - k * 22 - 11, 70 if k % 2 == 0 else 80))
    pts.append((-55, 80))
    poly(ctx, pts, '#FFFFFF'); poly(ctx, pts, NAVY, 0.05)
    for k in range(4): line(ctx, -35, -50 + k * 26, 35 - (k % 2) * 25, -50 + k * 26, 6, '#AEB4D0')
    text(ctx, '-', 30, 58, 40, RED, 'xbold')
    ctx.restore()

def calculator(ctx, s=1.0):
    ctx.save(); ctx.scale(s, s)
    fill_rrect(ctx, -60, -85, 120, 170, 16, NAVY)
    fill_rrect(ctx, -46, -70, 92, 40, 8, '#BFF0D4')
    text(ctx, '+250', 36, -38, 26, '#168556', 'xbold', align='r')
    for r in range(3):
        for c in range(3):
            cc = CORAL if (r == 2 and c == 2) else '#4A5180'
            fill_rrect(ctx, -46 + c * 33, -16 + r * 32, 26, 24, 6, cc)
    ctx.restore()

def scale_balance(ctx, s=1.0, tilt=0.0):
    ctx.save(); ctx.scale(s, s)
    poly(ctx, [(-50, 150), (50, 150), (10, 120), (-10, 120)], NAVY)
    line(ctx, 0, 125, 0, -60, 12, NAVY)
    ctx.save(); ctx.translate(0, -60); ctx.rotate(tilt)
    line(ctx, -170, 0, 170, 0, 12, NAVY)
    ctx.restore()
    for sd in (-1, 1):
        px = sd * 170 * math.cos(tilt); py = -60 + sd * 170 * math.sin(tilt)
        line(ctx, px, py, px - 50, py + 90, 4, NAVY); line(ctx, px, py, px + 50, py + 90, 4, NAVY)
        ctx.new_path(); ctx.arc(px, py + 90, 60, 0, math.pi); ctx.close_path(); col(ctx, YELLOW); ctx.fill()
    circle(ctx, 0, -60, 14, CORAL)
    ctx.restore()

def job_card(ctx, s=1.0):
    ctx.save(); ctx.scale(s, s)
    card(ctx, 420, 300, '#FFFFFF')
    fill_rrect(ctx, -210, -150, 420, 70, 34, PURPLE); fill_rrect(ctx, -210, -110, 420, 30, 0, PURPLE)
    text(ctx, 'OFFRE D\'EMPLOI', 0, -102, 32, '#FFFFFF', 'xbold')
    ctx.restore()

def cv(ctx, s=1.0, st=None):
    ctx.save(); ctx.scale(s, s)
    card(ctx, 300, 380, '#FFFFFF', r=22)
    circle(ctx, -80, -120, 40, '#E9F7F0')
    if st:
        circle(ctx, -80, -126, 22, st['skin']); ctx.new_path(); ctx.arc(-80, -100, 30, math.pi, 0); col(ctx, st['shirt']); ctx.fill()
    text(ctx, 'CV', 60, -105, 54, NAVY, 'xbold')
    ctx.restore()

def desk(ctx, w=520):
    s = w / 520
    ctx.save(); ctx.scale(s, s)
    fill_rrect(ctx, -260, -20, 520, 34, 10, '#B97A4E')
    fill_rrect(ctx, -235, 10, 30, 220, 6, '#9B6440'); fill_rrect(ctx, 205, 10, 30, 220, 6, '#9B6440')
    fill_rrect(ctx, 80, 14, 140, 120, 10, '#A86E44')
    fill_rrect(ctx, 130, 60, 40, 10, 5, '#E3B78C')
    ctx.restore()

def hourglass(ctx, s=1.0, p=0.5):
    ctx.save(); ctx.scale(s, s)
    fill_rrect(ctx, -80, -120, 160, 20, 8, '#8C5A3C'); fill_rrect(ctx, -80, 100, 160, 20, 8, '#8C5A3C')
    poly(ctx, [(-60, -100), (60, -100), (8, 0), (60, 100), (-60, 100), (-8, 0)], '#DFF3FA')
    top = 1 - p
    if top > 0:
        poly(ctx, [(-50 * top, -100 * top + 0 * 1 + (-100 + 100 * top) * 0), (50 * top, -100 * top), (6, -4), (-6, -4)], '#F2B33D')
    poly(ctx, [(-56, 98), (56, 98), (56 * (1 - p * 0.0), 98 - 60 * p), (0, 98 - 85 * p), (-56, 98 - 60 * p)], '#F2B33D')
    line(ctx, 0, 0, 0, 96 - 80 * p, 4, '#F2B33D')
    ctx.restore()

def piggy(ctx, s=1.0):
    ctx.save(); ctx.scale(s, s)
    ellipse(ctx, 0, 0, 120, 90, '#F7A1B5')
    circle(ctx, 115, -5, 30, '#F49AAF'); ellipse(ctx, 132, -5, 14, 20, '#E8879E')
    circle(ctx, 128, -12, 4, NAVY); circle(ctx, 128, 2, 4, NAVY)
    circle(ctx, 70, -35, 9, NAVY)
    poly(ctx, [(30, -80), (60, -110), (70, -70)], '#F49AAF')
    for x in (-70, -25, 25, 65): fill_rrect(ctx, x - 14, 60, 28, 50, 10, '#F49AAF')
    fill_rrect(ctx, -30, -88, 60, 12, 6, '#C25E7A')
    ctx.new_path(); ctx.move_to(-118, -10); ctx.curve_to(-150, -40, -160, 10, -135, 0)
    ctx.set_line_width(8); col(ctx, '#F49AAF'); ctx.stroke()
    ctx.restore()

def plant(ctx, s=1.0, g=1.0):
    """g in 0..1 growth: sprout -> tree"""
    ctx.save(); ctx.scale(s, s)
    poly(ctx, [(-70, 0), (70, 0), (50, 110), (-50, 110)], '#C9673E')
    fill_rrect(ctx, -80, -10, 160, 24, 8, '#DB7A4F')
    h = 40 + 300 * g
    line(ctx, 0, 0, 0, -h, 10 + 22 * g, '#7A4E2D', cap=0)
    if g < 0.35:
        ellipse(ctx, -24, -h + 10, 26, 13, GREEN); ellipse(ctx, 24, -h + 4, 26, 13, '#33C487')
    else:
        r = 60 + 120 * (g - 0.35) / 0.65
        circle(ctx, 0, -h - r * 0.4, r, '#1FA971'); circle(ctx, -r * 0.6, -h, r * 0.7, '#22B377')
        circle(ctx, r * 0.6, -h, r * 0.7, '#1C9A66')
        if g > 0.8:
            for (dx, dy) in ((-40, -30), (30, -70), (50, 10), (-60, -90)):
                circle(ctx, dx * r / 150, -h - r * 0.4 + dy * r / 150, 12, YELLOW)
    ctx.restore()

def door(ctx, s=1.0, p=0.0):
    ctx.save(); ctx.scale(s, s)
    fill_rrect(ctx, -110, -200, 220, 400, 10, '#5B4B8A')
    # light behind
    fill_rrect(ctx, -95, -185, 190, 385, 6, '#FFF3C4')
    for k in range(5):
        circle(ctx, 0, 0, 40 + k * 30, YELLOW, 0.12 * p)
    w = 190 * (1 - 0.85 * p)
    poly(ctx, [(-95, -185), (-95 + w, -185 + 25 * p), (-95 + w, 200 - 15 * p), (-95, 200)], '#8C5A3C')
    circle(ctx, -95 + w - 20, 20, 9 * (1 - p * 0.6), YELLOW)
    ctx.restore()

def timetable(ctx, s=1.0, t=0.0, t_bus=999):
    ctx.save(); ctx.scale(s, s)
    card(ctx, 560, 440, '#FFFFFF', r=26)
    fill_rrect(ctx, -280, -220, 560, 70, 26, NAVY); fill_rrect(ctx, -280, -180, 560, 30, 0, NAVY)
    text(ctx, 'EMPLOI DU TEMPS', 0, -172, 32, '#FFFFFF', 'xbold')
    days = ['LUN', 'MAR', 'MER', 'JEU', 'VEN']
    for i, d in enumerate(days):
        text(ctx, d, -200 + i * 100, -112, 24, '#8A90B0', 'bold')
    cells = [(0, 0, 'C'), (1, 0, 'C'), (2, 0, 'C'), (3, 0, 'C'), (4, 0, 'C'),
             (0, 1, 'C'), (1, 1, 'B'), (2, 1, 'C'), (3, 1, 'B'), (4, 1, 'C'),
             (0, 2, 'R'), (1, 2, 'R'), (2, 2, 'B'), (3, 2, 'R'), (4, 2, 'B')]
    for (i, r, k) in cells:
        x = -240 + i * 100; y = -90 + r * 95
        if k == 'B':
            a = ease_out(prog(t, t_bus + i * 0.08, 0.4))
            if a > 0: fill_rrect(ctx, x, y, 80, 80, 14, GREEN, a)
        else:
            fill_rrect(ctx, x, y, 80, 80, 14, BLUE if k == 'C' else '#9DB7F5')
    ctx.restore()

def wallet(ctx, s=1.0):
    ctx.save(); ctx.scale(s, s)
    ctx.save(); ctx.translate(10, -50); ctx.rotate(-0.2); banknote(ctx, 0.8); ctx.restore()
    fill_rrect(ctx, -100, -50, 200, 130, 20, '#8C5A3C')
    fill_rrect(ctx, 30, -10, 80, 50, 14, '#A86E44'); circle(ctx, 60, 15, 9, YELLOW)
    ctx.restore()

def gauge(ctx, s=1.0, v=0.5, label=''):
    ctx.save(); ctx.scale(s, s)
    ctx.new_path(); ctx.arc(0, 0, 110, math.pi, 2 * math.pi); ctx.set_line_width(34); col(ctx, '#E3E6F2'); ctx.stroke()
    ctx.new_path(); ctx.arc(0, 0, 110, math.pi, math.pi + math.pi * v); col(ctx, CORAL if v > 0.5 else GREEN); ctx.stroke()
    a = math.pi + math.pi * v
    line(ctx, 0, 0, 80 * math.cos(a), 80 * math.sin(a), 10, NAVY); circle(ctx, 0, 0, 16, NAVY)
    if label: text(ctx, label, 0, 60, 30, NAVY, 'bold')
    ctx.restore()

def stairs(ctx, s=1.0, n=4, labels=None):
    ctx.save(); ctx.scale(s, s)
    cs = ['#B9E8D2', '#7FD6AE', '#3EC189', GREEN, '#168556']
    for i in range(n):
        fill_rrect(ctx, -300 + i * 150, -i * 110, 150, 120 + i * 110, 8, cs[i % len(cs)])
        if labels:
            text(ctx, labels[i], -225 + i * 150, -i * 110 + 50, 24, '#FFFFFF' if i > 1 else '#16634A', 'bold')
    ctx.restore()

def briefcase(ctx, s=1.0, c='#8C5A3C'):
    ctx.save(); ctx.scale(s, s)
    ctx.new_path(); rrect(ctx, -30, -80, 60, 40, 12); ctx.set_line_width(12); col(ctx, '#6B4229'); ctx.stroke()
    fill_rrect(ctx, -90, -55, 180, 120, 16, c)
    fill_rrect(ctx, -90, -10, 180, 12, 0, '#6B4229'); fill_rrect(ctx, -14, -18, 28, 26, 6, YELLOW)
    ctx.restore()

def magnifier(ctx, s=1.0):
    ctx.save(); ctx.scale(s, s)
    line(ctx, 40, 40, 100, 100, 26, NAVY)
    circle(ctx, 0, 0, 70, NAVY); circle(ctx, 0, 0, 54, '#DFF3FA')
    ctx.new_path(); ctx.arc(0, 0, 38, math.pi * 1.1, math.pi * 1.5); ctx.set_line_width(8); col(ctx, '#FFFFFF'); ctx.stroke()
    ctx.restore()

def bricks_house(ctx, s=1.0, p=1.0):
    """house built brick by brick; p 0..1"""
    ctx.save(); ctx.scale(s, s)
    rows = 6; per = 4
    total = rows * per + 1
    k = int(p * total + 0.0001)
    n = 0
    for r in range(rows):
        for c in range(per):
            if n >= k: break
            off = 30 if r % 2 else 0
            x = -150 + c * 75 + off - (0 if r % 2 == 0 else 15)
            if r % 2 and c == per - 1: w = 45
            else: w = 70
            fill_rrect(ctx, x - (15 if (r % 2 and c == 0) else 0), -r * 42, w, 38, 6, '#E07A5F' if (r + c) % 2 else '#D46A4F')
            n += 1
    if k >= total:
        poly(ctx, [(-185, -rows * 42 + 34), (0, -rows * 42 - 120), (185, -rows * 42 + 34)], NAVY)
    ctx.restore()

def rocket(ctx, s=1.0):
    ctx.save(); ctx.scale(s, s)
    poly(ctx, [(-40, 40), (-80, 90), (-40, 80)], CORAL); poly(ctx, [(40, 40), (80, 90), (40, 80)], CORAL)
    ctx.new_path(); ctx.move_to(0, -120); ctx.curve_to(60, -60, 50, 40, 40, 80); ctx.line_to(-40, 80)
    ctx.curve_to(-50, 40, -60, -60, 0, -120); col(ctx, '#FFFFFF'); ctx.fill()
    circle(ctx, 0, -30, 22, BLUE); circle(ctx, 0, -30, 14, '#CDEBF7')
    poly(ctx, [(-25, 85), (25, 85), (0, 140)], ORANGE)
    ctx.restore()

def arrow(ctx, x1, y1, x2, y2, c=NAVY, w=12, head=34, p=1.0):
    x2p = x1 + (x2 - x1) * p; y2p = y1 + (y2 - y1) * p
    if p <= 0.02: return
    ang = math.atan2(y2p - y1, x2p - x1)
    bx = x2p - head * 0.7 * math.cos(ang); by = y2p - head * 0.7 * math.sin(ang)
    line(ctx, x1, y1, bx, by, w, c)
    poly(ctx, [(x2p, y2p), (x2p - head * math.cos(ang - 0.5), y2p - head * math.sin(ang - 0.5)),
               (x2p - head * math.cos(ang + 0.5), y2p - head * math.sin(ang + 0.5))], c)

def speech_bubble(ctx, w, h, c='#FFFFFF', tail='bl'):
    shadow(ctx, -w / 2, -h / 2, w, h, 40, a=0.08)
    fill_rrect(ctx, -w / 2, -h / 2, w, h, 40, c)
    if tail == 'bl':
        poly(ctx, [(-w / 2 + 50, h / 2 - 5), (-w / 2 + 110, h / 2 - 5), (-w / 2 + 30, h / 2 + 50)], c)
    elif tail == 'br':
        poly(ctx, [(w / 2 - 50, h / 2 - 5), (w / 2 - 110, h / 2 - 5), (w / 2 - 30, h / 2 + 50)], c)

def thought_bubble(ctx, w, h, c='#FFFFFF', tx=-1):
    shadow(ctx, -w / 2, -h / 2, w, h, h / 2, a=0.08)
    fill_rrect(ctx, -w / 2, -h / 2, w, h, h / 2, c)
    circle(ctx, tx * w * 0.25, h / 2 + 30, 22, c); circle(ctx, tx * w * 0.32, h / 2 + 75, 13, c)

def number_badge(ctx, n, c=CORAL, r=56):
    circle(ctx, 0, 0, r, c)
    text(ctx, str(n), 0, r * 0.36, r * 1.05, '#FFFFFF', 'xbold')

def cloud(ctx, s=1.0, c='#FFFFFF', a=1.0):
    ctx.save(); ctx.scale(s, s)
    for (x, y, r) in ((-60, 10, 40), (-15, -15, 55), (40, 0, 45), (75, 15, 32)):
        circle(ctx, x, y, r, c, a)
    fill_rrect(ctx, -100, 10, 210, 42, 21, c, a)
    ctx.restore()

def rain_cloud(ctx, s=1.0, t=0.0):
    ctx.save(); ctx.scale(s, s)
    for k in range(6):
        ph = math.fmod(t * 1.6 + k * 0.37, 1.0)
        x = -70 + k * 28; y = 40 + ph * 120
        line(ctx, x, y, x - 6, y + 22, 6, '#6FA8DC', 1 - ph)
    cloud(ctx, 1.0, '#8E96B8')
    ctx.restore()

def sweat(ctx, s=1.0):
    ctx.save(); ctx.scale(s, s)
    ctx.new_path(); ctx.move_to(0, -24); ctx.curve_to(18, 0, 16, 20, 0, 20); ctx.curve_to(-16, 20, -18, 0, 0, -24)
    col(ctx, '#6FC3F0'); ctx.fill(); ctx.restore()

def confetti(ctx, t, t0, x0, y0, n=40, seed=1, spread=480):
    if t < t0: return
    import random
    rnd = random.Random(seed)
    dt = t - t0
    cs = [CORAL, YELLOW, GREEN, BLUE, PURPLE, TEAL]
    for i in range(n):
        vx = rnd.uniform(-1, 1) * spread; vy = rnd.uniform(-1100, -500)
        x = x0 + vx * dt; y = y0 + vy * dt + 900 * dt * dt
        if y > 2000: continue
        ctx.save(); ctx.translate(x, y); ctx.rotate(dt * rnd.uniform(-8, 8))
        fill_rrect(ctx, -9, -5, 18, 10, 3, cs[i % 6], clamp(2.8 - dt)); ctx.restore()
