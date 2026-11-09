import cairo, math, json, re, unicodedata, os

W, H = 1080, 1920
FPS = 30
HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- utils
def clamp(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x

def prog(t, t0, d):
    if d <= 0: return 1.0 if t >= t0 else 0.0
    return clamp((t - t0) / d)

def ease_out(p): return 1 - (1 - p) ** 3
def ease_in(p): return p ** 3
def ease_io(p): return 4 * p ** 3 if p < 0.5 else 1 - (-2 * p + 2) ** 3 / 2
def ease_back(p, s=1.8):
    p = p - 1
    return 1 + (s + 1) * p ** 3 + s * p ** 2
def lerp(a, b, p): return a + (b - a) * p

def hexc(h, a=1.0):
    h = h.lstrip('#')
    return (int(h[0:2], 16) / 255, int(h[2:4], 16) / 255, int(h[4:6], 16) / 255, a)

def col(ctx, h, a=1.0):
    if isinstance(h, tuple):
        ctx.set_source_rgba(*h[:3], h[3] * a if len(h) > 3 else a)
    else:
        ctx.set_source_rgba(*hexc(h, a))

def rrect(ctx, x, y, w, h, r):
    r = min(r, w / 2, h / 2)
    ctx.new_sub_path()
    ctx.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    ctx.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2)
    ctx.close_path()

def fill_rrect(ctx, x, y, w, h, r, c, a=1.0):
    rrect(ctx, x, y, w, h, r); col(ctx, c, a); ctx.fill()

def circle(ctx, x, y, r, c, a=1.0):
    ctx.new_path(); ctx.arc(x, y, r, 0, 2 * math.pi); col(ctx, c, a); ctx.fill()

def ellipse(ctx, x, y, rx, ry, c, a=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(rx, ry); ctx.new_path()
    ctx.arc(0, 0, 1, 0, 2 * math.pi); ctx.restore(); col(ctx, c, a); ctx.fill()

def line(ctx, x1, y1, x2, y2, w, c, a=1.0, cap=cairo.LINE_CAP_ROUND):
    ctx.new_path(); ctx.move_to(x1, y1); ctx.line_to(x2, y2)
    ctx.set_line_width(w); ctx.set_line_cap(cap); col(ctx, c, a); ctx.stroke()

def poly(ctx, pts, c, a=1.0):
    ctx.new_path(); ctx.move_to(*pts[0])
    for p in pts[1:]: ctx.line_to(*p)
    ctx.close_path(); col(ctx, c, a); ctx.fill()

def shadow(ctx, x, y, w, h, r, a=0.12, off=10):
    for i in range(3):
        rrect(ctx, x - i * 3, y + off - i * 2, w + i * 6, h + i * 6, r + i * 3)
        ctx.set_source_rgba(0.1, 0.12, 0.25, a / 3); ctx.fill()

def ground_shadow(ctx, x, y, rx, a=0.15):
    ellipse(ctx, x, y, rx, rx * 0.16, '#1b2040', a)

FONTS = {'reg': 'Poppins Medium', 'semi': 'Poppins SemiBold', 'bold': 'Poppins', 'xbold': 'Poppins ExtraBold'}

def font(ctx, size, kind='semi'):
    fam = FONTS[kind]
    ctx.select_font_face(fam, cairo.FONT_SLANT_NORMAL,
                         cairo.FONT_WEIGHT_BOLD if kind == 'bold' else cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(size)

def text_w(ctx, s):
    return ctx.text_extents(s).x_advance

def text(ctx, s, x, y, size, c='#1F2547', kind='semi', align='c', a=1.0):
    font(ctx, size, kind)
    w = text_w(ctx, s)
    if align == 'c': x -= w / 2
    elif align == 'r': x -= w
    ctx.move_to(x, y); col(ctx, c, a); ctx.show_text(s)
    return w

def pill(ctx, s, cx, cy, size, bg, fg='#FFFFFF', kind='bold', padx=None, pady=None):
    font(ctx, size, kind)
    w = text_w(ctx, s)
    padx = padx or size * 0.7; pady = pady or size * 0.45
    hh = size * 1.0 + pady * 2
    ww = w + padx * 2
    shadow(ctx, cx - ww / 2, cy - hh / 2, ww, hh, hh / 2, a=0.10, off=6)
    fill_rrect(ctx, cx - ww / 2, cy - hh / 2, ww, hh, hh / 2, bg)
    ctx.move_to(cx - w / 2, cy + size * 0.36); col(ctx, fg); ctx.show_text(s)
    return ww

# ------------------------------------------------- appear / group alpha
def show(ctx, t, t0, cx, cy, fn, dur=0.45, kind='pop', t1=None, out=0.3, base_scale=1.0):
    """Draw fn (origin at element centre) with an entrance animation."""
    if t < t0: return
    p = prog(t, t0, dur)
    a = ease_out(p)
    s = base_scale
    dx = dy = 0
    if kind == 'pop': s *= max(0.0, ease_back(p))
    elif kind == 'up': dy = (1 - ease_out(p)) * 60
    elif kind == 'down': dy = -(1 - ease_out(p)) * 60
    elif kind == 'left': dx = -(1 - ease_out(p)) * 140
    elif kind == 'right': dx = (1 - ease_out(p)) * 140
    elif kind == 'fade': pass
    elif kind == 'grow': s *= ease_out(p)
    if t1 is not None and t > t1:
        q = prog(t, t1, out); a *= 1 - q
        if q >= 1: return
    if a <= 0.001 or s <= 0.001: return
    ctx.save()
    if a < 0.999:
        ctx.push_group()
    ctx.translate(cx + dx, cy + dy); ctx.scale(s, s)
    fn(ctx)
    if a < 0.999:
        ctx.pop_group_to_source(); ctx.paint_with_alpha(a)
    ctx.restore()

def with_alpha(ctx, a, fn):
    if a <= 0.001: return
    if a >= 0.999: fn(); return
    ctx.push_group(); fn(); ctx.pop_group_to_source(); ctx.paint_with_alpha(a)

# ---------------------------------------------------------- words/timing
def norm(s):
    s = unicodedata.normalize('NFD', s.lower())
    s = ''.join(ch for ch in s if unicodedata.category(ch) != 'Mn')
    return re.sub(r"[^a-z0-9'\-]", '', s.replace('’', "'"))

WORDS = json.load(open(os.path.join(HERE, 'words.json'), encoding='utf-8'))
NW = [norm(w['w']) for w in WORDS]

def find_idx(query, after=0.0):
    q = [norm(x) for x in query.split()]
    for i in range(len(WORDS)):
        if WORDS[i]['s'] < after - 0.05: continue
        seg = NW[i:i + len(q)]
        if len(seg) == len(q) and all(a == b or a.split("'")[-1] == b for a, b in zip(seg, q)):
            return i
    raise KeyError(query)

def tw(query, after=0.0):
    return WORDS[find_idx(query, after)]['s']

def twe(query, after=0.0):
    i = find_idx(query, after) + len(query.split()) - 1
    return WORDS[i]['e']
