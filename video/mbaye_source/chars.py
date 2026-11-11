import math
from engine import *

# ---------------------------------------------------------------- styles
ELISEE = dict(name='Élisée', skin='#8A5534', skin_d='#6E4027', shirt='#1FA971', shirt_d='#168556',
              trim='#FFC93C', pants='#2F3A5C', shoe='#FFFFFF', shoe2='#FF7A45', hair='#1A1414',
              hair_style='flat', glasses=False, sleeves='short', collar=False, bag='#FF8A3D')
FABRICE = dict(name='Fabrice', skin='#6B3E26', skin_d='#55301c', shirt='#3C6FE0', shirt_d='#2D57B5',
               trim='#FFFFFF', pants='#B88A5A', shoe='#5A3A22', shoe2='#3E2817', hair='#120d0d',
               hair_style='round', glasses=True, sleeves='long', collar=True, bag='#E84A5F')
RECRUITER = dict(name='', skin='#7A4A2E', skin_d='#5f3822', shirt='#7B4FD6', shirt_d='#6040AE',
                 trim='#FFFFFF', pants='#2B2D42', shoe='#2B2D42', shoe2='#1b1c2b', hair='#1A1414',
                 hair_style='wrap', wrap='#FF8A3D', glasses=False, sleeves='long', collar=False, bag=None, skirt=True)
CUST1 = dict(name='', skin='#9A6340', skin_d='#7b4c30', shirt='#F25F5C', shirt_d='#cf4643', trim='#FFFFFF',
             pants='#3D405B', shoe='#3D405B', shoe2='#222222', hair='#1A1414', hair_style='flat', glasses=False,
             sleeves='short', collar=False, bag=None)
CUST2 = dict(name='', skin='#7d4b2d', skin_d='#603721', shirt='#FFB627', shirt_d='#d99a1c', trim='#FFFFFF',
             pants='#5C4D7D', shoe='#5C4D7D', shoe2='#222222', hair='#1A1414', hair_style='puffs', glasses=False,
             sleeves='short', collar=False, bag=None, skirt=True)
DAD = dict(CUST1, shirt='#5C80BC', shirt_d='#4a6aa0', hair='#555', pants='#4A4E69', sleeves='long')
MOM = dict(CUST2, shirt='#E76F51', shirt_d='#c75a3f', hair_style='wrap', wrap='#2A9D8F')

POSES = {
    'idle':   dict(la=8, le=4, ra=8, re=4),
    'wave':   dict(la=8, le=4, ra=150, re=25),
    'cheer':  dict(la=150, le=-15, ra=150, re=-15),
    'hold':   dict(la=22, le=-105, ra=22, re=-105),
    'holdR':  dict(la=8, le=4, ra=25, re=-110),
    'think':  dict(la=8, le=4, ra=40, re=-190),
    'point':  dict(la=8, le=4, ra=95, re=0),
    'pointL': dict(la=95, le=0, ra=8, re=4),
    'shrug':  dict(la=35, le=85, ra=35, re=85),
    'raiseR': dict(la=8, le=4, ra=165, re=0),
    'hips':   dict(la=40, le=-75, ra=40, re=-75),
    'scratch': dict(la=8, le=4, ra=160, re=-120),
    'present': dict(la=8, le=4, ra=65, re=-40),
    'juggle': dict(la=60, le=-60, ra=60, re=-60),
    'run':    dict(la=50, le=-80, ra=-40, re=-60),
}

def blend_pose(a, b, p):
    A = POSES[a] if isinstance(a, str) else a
    B = POSES[b] if isinstance(b, str) else b
    return {k: lerp(A[k], B[k], p) for k in A}

def pose_seq(t, seq, d=0.35):
    """seq: list of (time, posename) -> blended pose at t"""
    cur = seq[0][1]
    res = POSES[cur] if isinstance(cur, str) else cur
    for i in range(1, len(seq)):
        ti, pn = seq[i]
        if t >= ti:
            res = blend_pose(seq[i - 1][1], pn, ease_io(prog(t, ti, d)))
    return res

UA, LA = 112, 106  # upper/lower arm length

def _arm(ctx, st, side, a, e, sleeve_c, skin):
    sx, sy = side * 78, -452
    a1 = math.radians(a)
    ex, ey = sx + side * UA * math.sin(a1), sy + UA * math.cos(a1)
    a2 = math.radians(a + e)
    hx, hy = ex + side * LA * math.sin(a2), ey + LA * math.cos(a2)
    if st['sleeves'] == 'long':
        line(ctx, sx, sy, ex, ey, 40, sleeve_c); line(ctx, ex, ey, hx, hy, 36, sleeve_c)
        circle(ctx, hx, hy, 20, skin)
    else:
        line(ctx, ex, ey, hx, hy, 32, skin)
        line(ctx, sx, sy, ex, ey, 32, skin)
        line(ctx, sx, sy, sx + (ex - sx) * 0.55, sy + (ey - sy) * 0.55, 44, sleeve_c)
        circle(ctx, hx, hy, 20, skin)
    return hx, hy

def draw_char(ctx, st, x, y, s=1.0, pose='idle', t=0.0, mouth='smile', look=0.0, walk=None,
              blink_seed=0.0, bag=False, grad=False, brows=0.0, tilt=0.0, flip=False, talk=False):
    """Draw character with feet at (x,y). Returns dict of hand positions (world)."""
    P = POSES[pose] if isinstance(pose, str) else pose
    ctx.save(); ctx.translate(x, y); ctx.scale(-s if flip else s, s)
    ground_shadow(ctx, 0, 0, 110)
    bob = 0.0
    ll = rl = 0.0
    if walk is not None:
        ll = math.sin(walk * 2 * math.pi) * 24; rl = -ll
        bob = abs(math.cos(walk * 2 * math.pi)) * -10
    else:
        bob = math.sin(t * 2.2 + blink_seed) * 3
    # legs
    hip_y = -232
    for side, ang in ((-1, ll), (1, rl)):
        hx0 = side * 40
        a = math.radians(ang)
        fx, fy = hx0 + math.sin(a) * 232, hip_y + math.cos(a) * 232
        if st.get('skirt'):
            line(ctx, hx0 * 0.8, hip_y + 60, fx, fy - 10, 30, st['skin'])
        else:
            line(ctx, hx0, hip_y, fx, fy - 8, 50, st['pants'], cap=1)
        # shoe
        ellipse(ctx, fx + side * 12, fy - 14, 44, 20, st['shoe'])
        ctx.new_path(); rrect(ctx, fx + side * 12 - 44, fy - 12, 88, 10, 4); col(ctx, st['shoe2']); ctx.fill()
    ctx.translate(0, bob)
    # backpack behind
    if bag and st.get('bag'):
        fill_rrect(ctx, -105, -440, 210, 220, 50, st['bag'])
    # torso
    tw_ = 170
    if st.get('skirt'):
        poly(ctx, [(-85, -470), (85, -470), (120, -150), (-120, -150)], st['shirt'])
        poly(ctx, [(-120, -150), (120, -150), (115, -170), (-115, -170)], st['shirt_d'])
    else:
        fill_rrect(ctx, -tw_ / 2, -478, tw_, 268, 50, st['shirt'])
        fill_rrect(ctx, -tw_ / 2, -250, tw_, 40, 18, st['pants'])
        line(ctx, -tw_ / 2 + 4, -232, tw_ / 2 - 4, -232, 10, st['shirt_d'], 0.0)
    if grad:
        poly(ctx, [(-95, -480), (95, -480), (118, -150), (-118, -150)], '#262B4F')
        poly(ctx, [(-30, -480), (30, -480), (0, -400)], '#FFC93C')
    # collar/trim
    if not grad:
        if st.get('collar'):
            poly(ctx, [(-34, -480), (0, -446), (-6, -426), (-44, -462)], st['trim'])
            poly(ctx, [(34, -480), (0, -446), (6, -426), (44, -462)], st['trim'])
            for k in range(3): circle(ctx, 0, -410 + k * 50, 5, st['shirt_d'])
        else:
            ctx.new_path(); ctx.arc(0, -478, 34, 0, math.pi); ctx.set_line_width(10); col(ctx, st['trim']); ctx.stroke()
    if bag and st.get('bag'):
        line(ctx, -60, -470, -55, -300, 16, st['bag']); line(ctx, 60, -470, 55, -300, 16, st['bag'])
    # neck + head
    head_y = -580
    ctx.save(); ctx.translate(0, head_y); ctx.rotate(math.radians(tilt))
    fill_rrect(ctx, -22, 50, 44, 50, 10, st['skin_d'])
    hs = st['hair_style']
    if hs == 'puffs':
        circle(ctx, -88, -60, 42, st['hair']); circle(ctx, 88, -60, 42, st['hair'])
    if hs == 'round':
        circle(ctx, 0, -18, 100, st['hair'])
    # ears
    circle(ctx, -88, 6, 18, st['skin']); circle(ctx, 88, 6, 18, st['skin'])
    ellipse(ctx, 0, 0, 90, 96, st['skin'])
    # hair
    if hs == 'flat':
        ctx.new_path(); ctx.move_to(-90, -12); ctx.curve_to(-96, -70, -70, -104, 0, -106)
        ctx.curve_to(70, -104, 96, -70, 90, -12); ctx.line_to(80, -30); ctx.curve_to(40, -52, -40, -52, -80, -30)
        ctx.close_path(); col(ctx, st['hair']); ctx.fill()
        fill_rrect(ctx, -80, -122, 160, 50, 20, st['hair'])
    elif hs == 'round':
        ctx.new_path(); ctx.move_to(-92, -6); ctx.curve_to(-70, -60, 70, -60, 92, -6)
        ctx.line_to(96, -40); ctx.curve_to(80, -110, -80, -110, -96, -40); ctx.close_path()
        col(ctx, st['hair']); ctx.fill()
    elif hs == 'puffs':
        ctx.new_path(); ctx.move_to(-90, -10); ctx.curve_to(-80, -110, 80, -110, 90, -10)
        ctx.curve_to(50, -60, -50, -60, -90, -10); col(ctx, st['hair']); ctx.fill()
    elif hs == 'wrap':
        ctx.new_path(); ctx.move_to(-94, -10); ctx.curve_to(-110, -150, 110, -150, 94, -10)
        ctx.curve_to(50, -50, -50, -50, -94, -10); col(ctx, st['wrap']); ctx.fill()
        circle(ctx, 40, -112, 34, st['wrap'])
    # face
    blink = (math.fmod(t + 1.3 + blink_seed * 1.7, 3.7) < 0.12)
    ex = 34; ey = 4
    lk = look * 9
    for sd in (-1, 1):
        if blink:
            line(ctx, sd * ex - 14, ey, sd * ex + 14, ey, 5, '#1A1414')
        else:
            ellipse(ctx, sd * ex, ey, 19, 22, '#FFFFFF')
            circle(ctx, sd * ex + lk, ey + 3, 10, '#1A1414')
            circle(ctx, sd * ex + lk + 3, ey - 1, 3.5, '#FFFFFF')
        # brows
        by = ey - 36 - brows * 8
        line(ctx, sd * ex - 15, by + (sd * brows * 4 if brows < 0 else 0), sd * ex + 15,
             by - (sd * brows * 4 if brows < 0 else 0), 7, '#1A1414')
    if st.get('glasses'):
        for sd in (-1, 1):
            ctx.new_path(); ctx.arc(sd * ex, ey, 30, 0, 2 * math.pi); ctx.set_line_width(6); col(ctx, '#1F2547'); ctx.stroke()
        line(ctx, -6, ey - 4, 6, ey - 4, 6, '#1F2547')
    # nose
    ctx.new_path(); ctx.arc(0, 30, 9, math.pi * 0.1, math.pi * 0.9); ctx.set_line_width(5); col(ctx, st['skin_d']); ctx.stroke()
    # mouth
    my = 58
    m = mouth
    if talk and m in ('smile', 'neutral'):
        m = 'open' if math.sin(t * 22) > 0.2 else m
    if m == 'smile':
        ctx.new_path(); ctx.arc(0, my - 14, 24, math.pi * 0.15, math.pi * 0.85); ctx.set_line_width(7)
        col(ctx, '#4A1F12'); ctx.stroke()
    elif m == 'big':
        ctx.new_path(); ctx.arc(0, my - 8, 26, 0, math.pi); ctx.close_path(); col(ctx, '#4A1F12'); ctx.fill()
        ctx.new_path(); ctx.arc(0, my - 8, 26, 0.35, math.pi - 0.35); ctx.clip()
        ellipse(ctx, 0, my + 16, 18, 8, '#E86A6A'); ctx.reset_clip()
    elif m == 'open':
        ellipse(ctx, 0, my, 16, 14, '#4A1F12')
    elif m == 'o':
        ellipse(ctx, 0, my, 14, 18, '#4A1F12')
    elif m == 'sad':
        ctx.new_path(); ctx.arc(0, my + 18, 22, math.pi * 1.2, math.pi * 1.8); ctx.set_line_width(7)
        col(ctx, '#4A1F12'); ctx.stroke()
    else:
        line(ctx, -16, my, 16, my, 7, '#4A1F12')
    if grad:
        poly(ctx, [(-120, -98), (0, -140), (120, -98), (0, -60)], '#262B4F')
        fill_rrect(ctx, -60, -96, 120, 40, 8, '#262B4F')
        line(ctx, 0, -100, 92, -86, 5, '#FFC93C'); line(ctx, 92, -86, 96, -40, 5, '#FFC93C')
        circle(ctx, 96, -36, 8, '#FFC93C')
    ctx.restore()
    # arms
    hands = {}
    hl = _arm(ctx, st, -1, P['la'], P['le'], st['shirt_d'] if not grad else '#262B4F', st['skin'])
    hr = _arm(ctx, st, 1, P['ra'], P['re'], st['shirt_d'] if not grad else '#262B4F', st['skin'])
    m = ctx.get_matrix()
    ctx.restore()
    hands['l'] = m.transform_point(*hl)
    hands['r'] = m.transform_point(*hr)
    if flip: hands['l'], hands['r'] = hands['r'], hands['l']
    hands['head'] = m.transform_point(0, -580 + bob)
    return hands

def name_tag(ctx, t, t0, st, x, y, s=1.0, c=None):
    c = c or st['shirt']
    show(ctx, t, t0, x, y, lambda c2: pill(c2, st['name'], 0, 0, 44 * s, c), dur=0.45)
