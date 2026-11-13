"""History Lab: three Egypt myth Shorts (1080x1920). Visible world column x 656-1264, centre 960.
Usage: python3 egypt_shorts.py <tts_dir> <out_root> [cleopatra|builders|heart ...]"""
import math, random, sys
from kzlib import *

CX, GOLD, RED, SAND, SAND_D = 960, "#e8b931", "#e5383b", "#c9a46a", "#9c7444"
VOICE, LANG, SPEED = "bm_george", "en-gb", .98

# ---------------------------------------------------------------- Egypt art
def stars(n=70, seed=4, ymax=620):
    r = random.Random(seed)
    return svg("".join(f'<circle cx="{r.uniform(600, 1320):.0f}" cy="{r.uniform(10, ymax):.0f}" r="{r.uniform(1, 2.6):.1f}" fill="#f4efe0" opacity="{r.uniform(.25, .8):.2f}"/>' for _ in range(n)))

def svg(markup, **kw): return {"type": "svg", "markup": markup, **kw}

def pyramid(x, base, w, h, lit="#d9b77a", shade="#9c7444", op=1):
    apex, mid = (x, base - h), x + w * .14
    s = (f'<g opacity="{op}"><polygon fill="{lit}" points="{x - w/2},{base} {apex[0]},{apex[1]} {mid},{base}"/>'
         f'<polygon fill="{shade}" points="{mid},{base} {apex[0]},{apex[1]} {x + w/2},{base}"/>')
    for k in range(1, 9):
        y = base - h * k / 9; f = 1 - k / 9
        s += f'<line x1="{x - w/2 * f}" y1="{y}" x2="{x + w/2 * f}" y2="{y}" stroke="#000" stroke-opacity=".08" stroke-width="2"/>'
    return s + '</g>'

def ground(y=860, col=SAND, front=True):
    m = f'<rect x="-600" y="{y}" width="3120" height="1400" fill="{col}"/>'
    if front:
        m += f'<path fill="{SAND_D}" opacity=".35" d="M-600,{y + 40} C600,{y + 10} 900,{y + 70} 1300,{y + 30} C1700,{y} 2000,{y + 60} 2520,{y + 40} L2520,{y + 1400} L-600,{y + 1400} Z"/>'
    return svg(m)

def sun(x=960, y=520, r=90, col="#f2c14e"):
    return svg(f'<circle cx="{x}" cy="{y}" r="{r * 3}" fill="{col}" opacity=".07"/><circle cx="{x}" cy="{y}" r="{r * 1.7}" fill="{col}" opacity=".12"/><circle cx="{x}" cy="{y}" r="{r}" fill="{col}"/>')

def moon(x=1120, y=170, r=46):
    return svg(f'<circle cx="{x}" cy="{y}" r="{r * 2.6}" fill="#e9eef2" opacity=".06"/><circle cx="{x}" cy="{y}" r="{r}" fill="#e8e6dc"/>'
               f'<circle cx="{x - 14}" cy="{y - 10}" r="9" fill="#cfccc0"/><circle cx="{x + 16}" cy="{y + 14}" r="6" fill="#cfccc0"/>')

def heart(x, y, s=1.0, col="#b3262c"):
    return (f'<g transform="translate({x} {y}) scale({s})"><path fill="{col}" d="M0,40 C-60,0 -70,-40 -40,-58 C-18,-70 -4,-56 0,-42 C4,-56 18,-70 40,-58 C70,-40 60,0 0,40 Z"/>'
            f'<path fill="#fff" opacity=".25" d="M-38,-44 C-26,-56 -14,-50 -12,-42 C-22,-46 -30,-40 -38,-30 Z"/></g>')

def feather(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})"><path fill="#f1ede2" d="M-6,40 C-30,10 -34,-40 -10,-80 C10,-96 30,-90 30,-70 C34,-30 20,10 6,40 Z"/>'
            f'<path stroke="#b9b2a0" stroke-width="3" fill="none" d="M0,44 C2,0 6,-40 18,-80"/></g>')

def scales(tilt=0.0, cx=CX, top=430):
    """Scales of Ma'at. tilt > 0 = left pan (heart) lower."""
    L, a = 185, math.radians(tilt)
    lx, ly = cx - L * math.cos(a), top + L * math.sin(a)
    rx, ry = cx + L * math.cos(a), top - L * math.sin(a)
    gold = "#c99a3c"; s = f'<rect x="{cx - 9}" y="{top}" width="18" height="420" fill="{gold}"/><rect x="{cx - 90}" y="{top + 410}" width="180" height="22" rx="6" fill="{gold}"/>'
    s += f'<line x1="{lx}" y1="{ly}" x2="{rx}" y2="{ry}" stroke="{gold}" stroke-width="12" stroke-linecap="round"/><circle cx="{cx}" cy="{top}" r="16" fill="{gold}"/>'
    for px, py, item in ((lx, ly, heart(0, 0, .9)), (rx, ry, feather(0, -10, .9))):
        s += f'<path stroke="{gold}" stroke-width="3" fill="none" d="M{px},{py} L{px - 70},{py + 150} M{px},{py} L{px + 70},{py + 150}"/>'
        s += f'<path fill="{gold}" d="M{px - 90},{py + 150} L{px + 90},{py + 150} C{px + 70},{py + 190} {px - 70},{py + 190} {px - 90},{py + 150} Z"/>'
        s += f'<g transform="translate({px} {py + 110})">{item}</g>'
    return s

def worker(x, y, s=1.0, lean=0):
    c = "#1a120c"
    return (f'<g transform="translate({x} {y}) scale({s}) rotate({lean})" fill="{c}"><circle cx="0" cy="-150" r="18"/>'
            f'<path d="M-14,-130 L14,-130 L18,-60 L-18,-60 Z"/><path d="M-18,-62 L18,-62 L22,-30 L-22,-30 Z" fill="#e9e1cf"/>'
            f'<path stroke="{c}" stroke-width="12" stroke-linecap="round" d="M-8,-32 L-26,30 M8,-32 L22,30"/>'
            f'<path stroke="{c}" stroke-width="9" stroke-linecap="round" d="M-6,-120 L-50,-100 M6,-120 L-48,-108"/></g>')

def haul_group():
    """Stone block on a sledge, rope and four workers pulling to the right. Origin = block centre."""
    s = f'<rect x="-175" y="-60" width="350" height="120" fill="#cbb084"/><rect x="-175" y="-60" width="350" height="120" fill="none" stroke="#8a6c43" stroke-width="5"/>'
    s += f'<path fill="#6b4a2b" d="M-195,62 L190,62 L215,78 L-195,78 Z"/>'
    s += '<path stroke="#7a5a35" stroke-width="6" fill="none" d="M180,0 L620,-58"/>'
    for i, wx in enumerate((300, 400, 500, 600)):
        s += worker(wx, 70, .85, lean=-14 + (i % 2) * 3)
    return s

def skull_head(x=960, y=560):
    return svg(f'<g transform="translate({x - 960} {y - 560})"><path fill="#232a31" d="M760,520 C750,330 990,280 1100,400 L1122,470 L1176,560 L1124,576 L1134,620 L1112,642 L1122,684 C1100,722 1040,732 1000,722 L992,860 L812,860 L826,704 C772,654 764,604 760,520 Z"/>'
               f'<circle cx="1068" cy="470" r="11" fill="#e9eef2" opacity=".8"/></g>')

def brain_markup():
    s = '<path fill="#e38a9a" d="M-175,10 C-190,-80 -100,-125 -20,-118 C40,-140 140,-110 170,-50 C200,10 160,90 80,100 C30,128 -60,124 -110,96 C-160,84 -178,50 -175,10 Z"/>'
    for d in ("M-120,-40 C-80,-70 -40,-20 0,-50", "M-140,30 C-90,0 -40,50 10,20", "M20,-80 C60,-50 100,-90 130,-40", "M40,40 C80,10 110,60 150,20"):
        s += f'<path d="{d}" stroke="#b05468" stroke-width="7" fill="none" stroke-linecap="round"/>'
    return s

def bone():
    return svg('<g transform="translate(960 560) rotate(-30)"><path fill="#ece4d0" d="M-260,-30 C-300,-70 -340,-20 -300,0 C-340,20 -300,70 -260,30 L260,30 C300,70 340,20 300,0 C340,-20 300,-70 260,-30 Z"/>'
               '<path stroke="#7d6c4f" stroke-width="5" fill="none" d="M-20,-30 L-6,-6 L-26,8 L-10,30"/>'
               '<ellipse cx="-14" cy="0" rx="38" ry="40" fill="#d6c9a8" opacity=".55"/></g>')

def tombs(y=760):
    s = ''
    for i, x in enumerate((720, 860, 1000, 1140)):
        s += f'<path fill="#6d5236" d="M{x - 52},{y + 90} L{x - 52},{y + 20} C{x - 52},{y - 34} {x + 52},{y - 34} {x + 52},{y + 20} L{x + 52},{y + 90} Z"/><rect x="{x - 14}" y="{y + 40}" width="28" height="50" fill="#2a1d12"/>'
    return s

def earth_cut(y=520):   # ground cross-section: sand on top, earth below
    return svg(f'<rect x="-600" y="{y}" width="3120" height="1400" fill="#8a6a45"/><rect x="-600" y="{y}" width="3120" height="70" fill="{SAND}"/>'
               f'<rect x="-600" y="{y + 70}" width="3120" height="1400" fill="#000" opacity=".25"/>')

# ---------------------------------------------------------------- common bits
NIGHT = {"top": "#08111f", "bottom": "#2c3a57", "rays": False, "particleCount": 22}
DUSK = {"top": "#141a33", "bottom": "#b0663a", "rays": False, "particleCount": 22}
DAY = {"top": "#2a5675", "bottom": "#d9a866", "rays": True, "rayOpacity": .05, "particleCount": 18}
HALL = {"top": "#0d0a08", "bottom": "#2a1d10", "rays": False, "particleCount": 30, "spotlight": {"x": 960, "w": 360}}

def cap(text, t0, y=None, size=48, **kw):
    e = {"type": "caption", "text": text, "x": CX, "size": size, "t0": t0, **kw}
    if y is not None: e["y"] = y
    return e
def tag(text, t0=.2, y=90): return {"type": "tag", "text": text, "x": 690, "y": y, "t0": t0}
def stack(items, y=620, w=520, size=28, gap=84, x=None):
    return {"type": "factstack", "x": x or CX - w / 2, "y": y, "w": w, "size": size, "gap": gap, "items": items}
def endcard(T, i=0):
    return [tag("History Lab", T.p(i), y=1000), cap("*follow* for more", T.p(i) + .3, y=930, size=40)]

TOKENS_EG = {"hl": GOLD, "creature": {**TOKENS["creature"], "blob": ["#cbb084", "#cbb084", "#cbb084"]}}

# ================================================================ 1. Cleopatra
def cleopatra():
    st = Story(); shot = st.shot

    @shot(["Cleopatra lived closer to the Moon landing than to the building of the Great Pyramid."])
    def _(T):
        return (NIGHT, {"zoomFrom": 1, "zoomTo": 1.08, "y": 700},
                [stars(), moon(1175, 560, 40), ground(860), svg(pyramid(960, 865, 600, 380)),
                 cap("*cleopatra*", T.p(0), y=190, size=70),
                 cap("lived closer to the", T.w(0, "lived"), y=270, size=38),
                 cap("*moon landing*", T.w(0, "Moon"), y=350, size=56),
                 cap("than the pyramids", T.w(0, "building"), y=420, size=40)])

    @shot(["The Great Pyramid was finished around twenty-five sixty B.C."])
    def _(T):
        return (DAY, {"zoomFrom": 1.1, "zoomTo": 1.0, "y": 700},
                [sun(780, 560, 55), ground(860), svg(pyramid(960, 865, 600, 380)),
                 tag("Giza"),
                 cap("*2560 bc*", T.w(0, "twenty"), y=250, size=100),
                 cap("the *great pyramid*", T.w(0, "Great"), y=980, size=44)])

    @shot(["Cleopatra died in thirty B.C.", "That's more than two and a half thousand years later.",
           "The Moon landing came less than two thousand years after her."])
    def _(T):
        AX, Y0, Y1, Y2 = 720, 200, 602, 920
        dot = lambda y, c, t0: svg(f'<circle cx="{AX}" cy="{y}" r="14" fill="{c}"/>', t0=t0)
        return ({"top": "#0b1422", "bottom": "#1a2333", "rays": False, "particleCount": 15}, {},
                [svg(f'<line x1="{AX}" y1="{Y0}" x2="{AX}" y2="{Y2}" stroke="#e9eef2" stroke-opacity=".18" stroke-width="4"/>'),
                 dot(Y0, GOLD, 0), {"type": "pill", "text": "2560 BC · pyramid", "x": 760, "y": Y0 - 26, "size": 24, "t0": 0},
                 dot(Y1, "#e9eef2", T.w(0, "thirty")), {"type": "pill", "text": "30 BC · Cleopatra", "x": 760, "y": Y1 - 26, "size": 24, "t0": T.w(0, "thirty")},
                 {"type": "bracket", "x1": AX, "y1": Y0, "x2": AX, "y2": Y1, "color": GOLD, "t0": T.w(1, "two")},
                 cap("*2,530 yrs*", T.w(1, "two") + .3, y=420, size=46, x=1000),
                 dot(Y2, RED, T.w(2, "Moon")), {"type": "pill", "text": "1969 · Moon landing", "x": 760, "y": Y2 - 26, "size": 24, "t0": T.w(2, "Moon"), "tone": "red"},
                 {"type": "bracket", "x1": AX, "y1": Y1, "x2": AX, "y2": Y2, "color": "#e9eef2", "t0": T.w(2, "less")},
                 cap("1,998 yrs", T.w(2, "less") + .3, y=780, size=46, x=1000)])

    @shot(["To her, the pyramids were already ancient ruins."])
    def _(T):
        return (DUSK, {"zoomFrom": 1, "zoomTo": 1.1, "y": 760},
                [sun(960, 760, 80, "#f08a3c"), ground(860),
                 svg(pyramid(800, 865, 360, 230, "#7a5634", "#4a3220")), svg(pyramid(1120, 865, 280, 180, "#7a5634", "#4a3220")),
                 {"type": "stamp", "text": "Already ancient", "x": CX, "y": 380, "size": 50, "t0": T.w(0, "ancient")}])

    @shot(["And she wasn't Egyptian by descent.", "Her family were Greeks, from Macedonia."], chapter=True)
    def _(T):
        return ({"mode": "paper"}, {"zoomFrom": 1, "zoomTo": 1.06},
                [{"type": "namecard", "title": "CLEOPATRA VII", "sub": "Queen of Egypt · 51–30 BC", "x": CX, "y": 360, "w": 520, "t0": 0},
                 {"type": "pill", "text": "Egyptian family", "x": 780, "y": 540, "size": 28, "t0": T.w(0, "Egyptian")},
                 {"type": "redx", "x": 960, "y": 566, "size": 46, "t0": T.w(0, "descent")},
                 {"type": "pill", "text": "Greek · Macedonian", "x": 780, "y": 640, "size": 28, "check": True, "t0": T.w(1, "Greeks")},
                 {"type": "stamp", "text": "Ptolemaic dynasty", "x": CX, "y": 850, "size": 44, "color": GOLD, "t0": T.w(1, "Macedonia")}])

    @shot(["In over two hundred and fifty years, she was the first ruler of her family to even learn Egyptian."])
    def _(T):
        return (NIGHT, {"zoomFrom": 1, "zoomTo": 1.08},
                [stars(seed=9), {"type": "bignumber", "from": 0, "to": 250, "suffix": "+ yrs", "x": CX, "y": 420, "size": 120, "color": "#fff8e6", "t0": T.w(0, "two") - .2, "dur": 1.2},
                 cap("the *first* to learn", T.w(0, "first"), y=600, size=44),
                 cap("egyptian", T.w(0, "learn"), y=670, size=56)])

    @shot(["History is a lot older than you think."], tail=2.2)
    def _(T):
        return (NIGHT, {"zoomFrom": 1.08, "zoomTo": 1.0, "y": 700},
                [stars(seed=2), moon(1110, 150), ground(860), svg(pyramid(960, 865, 600, 380)),
                 cap("history is *older*", T.w(0, "older"), y=330, size=48),
                 cap("than you think", T.w(0, "think"), y=400, size=40)] + endcard(T))
    return st

# ================================================================ 2. Pyramid builders
def builders():
    st = Story(); shot = st.shot

    @shot(["Everything you were taught about who built the pyramids is probably wrong."])
    def _(T):
        return (DUSK, {"zoomFrom": 1, "zoomTo": 1.12, "y": 760},
                [sun(1000, 740, 70, "#f08a3c"), ground(860),
                 svg(pyramid(820, 865, 420, 270, "#7a5634", "#4a3220")), svg(pyramid(1130, 865, 300, 190, "#7a5634", "#4a3220")),
                 cap("who built", T.w(0, "who"), y=260, size=50),
                 cap("the *pyramids*?", T.w(0, "pyramids"), y=330, size=54),
                 {"type": "stamp", "text": "Wrong", "x": CX, "y": 520, "size": 80, "t0": T.w(0, "wrong")}])

    @shot(["It wasn't slaves."])
    def _(T):
        return ({"mode": "black"}, {},
                [cap("slaves", T.p(0) - .1, y=560, size=90),
                 {"type": "redx", "x": CX, "y": 530, "size": 150, "width": 10, "t0": T.w(0, "slaves") + .1}])

    @shot(["In nineteen ninety, a horse tripped over a buried wall near Giza."], chapter=True)
    def _(T):
        wall = svg('<g>' + ''.join(f'<rect x="{870 + (i % 4) * 46 + (23 if i // 4 % 2 else 0)}" y="{820 + (i // 4) * 26}" width="44" height="24" fill="#7a5a3a" stroke="#5a3f26" stroke-width="2"/>' for i in range(8)) + '</g>')
        return (DAY, {"zoomFrom": 1, "zoomTo": 1.25, "x": 960, "y": 830},
                [sun(1150, 300, 50), svg(pyramid(1060, 862, 320, 200, op=.55)), ground(860, front=False), wall,
                 tag("Giza · 1990"),
                 cap("a horse *tripped*", T.w(0, "horse"), y=980, size=46),
                 {"type": "circle", "x": 960, "y": 830, "rx": 150, "ry": 70, "t0": T.w(0, "wall")}])

    @shot(["Under the sand was a cemetery for the pyramid builders.", "Nearby, their town. Bakeries. Breweries. Houses."])
    def _(T):
        return (DAY, {"zoomFrom": 1, "zoomTo": 1.06},
                [earth_cut(520), svg(tombs(760)),
                 cap("the *builders'* tombs", T.w(0, "builders"), y=420, size=42),
                 stack([{"text": "Bakeries", "t0": T.w(1, "Bakeries")}, {"text": "Breweries", "t0": T.w(1, "Breweries")},
                        {"text": "Houses", "t0": T.w(1, "Houses")}], y=180, w=420)])

    @shot(["They were buried in the shadow of the king's pyramid, with bread and beer for the afterlife."])
    def _(T):
        return (DUSK, {"zoomFrom": 1, "zoomTo": 1.1, "y": 800},
                [ground(860), svg(pyramid(1050, 865, 560, 380, "#7a5634", "#4a3220")), svg(tombs(790)),
                 {"type": "pill", "text": "Buried with honour", "x": 700, "y": 200, "size": 28, "check": True, "t0": T.w(0, "buried")},
                 stack([{"text": "Bread", "t0": T.w(0, "bread")}, {"text": "Beer", "t0": T.w(0, "beer")}], y=290, w=300, x=700)])

    @shot(["Their skeletons show broken bones that were set, and healed.", "Someone was caring for them."])
    def _(T):
        return ({"mode": "black"}, {"zoomFrom": 1, "zoomTo": 1.1},
                [bone(), {"type": "circle", "x": 945, "y": 565, "rx": 90, "ry": 80, "color": "#3ecf6a", "t0": T.w(0, "healed")},
                 cap("set and *healed*", T.w(0, "healed"), y=820, size=48),
                 cap("someone *cared*", T.w(1, "caring"), y=900, size=42)])

    @shot(["The work crews even gave themselves names.", "The Friends of Khufu.", "And the Drunkards of Menkaure."], chapter=True)
    def _(T):
        return ({"mode": "paper"}, {"zoomFrom": 1, "zoomTo": 1.06},
                [cap("crew *names*", T.w(0, "names"), y=300, size=54),
                 stack([{"text": "Friends of Khufu", "t0": T.w(1, "Friends")},
                        {"text": "Drunkards of Menkaure", "t0": T.w(2, "Drunkards"), "tone": "red"}], y=440, w=560, size=26),
                 {"type": "stamp", "text": "Real graffiti", "x": CX, "y": 760, "size": 46, "color": GOLD, "t0": T.w(2, "Menkaure") + .3}])

    @shot(["Most were Egyptian farmers and craftsmen, working in shifts, fed on bread and beer."])
    def _(T):
        return (DAY, {"zoomFrom": 1, "zoomTo": 1.05, "y": 700},
                [sun(1150, 260, 50), svg(pyramid(980, 860, 520, 330, op=.7)), ground(860, front=False),
                 prop(haul_group(), 720, 800, .75, swim={"vx": 12}, bob=0),
                 stack([{"text": "Farmers", "t0": T.w(0, "farmers")}, {"text": "Craftsmen", "t0": T.w(0, "craftsmen")},
                        {"text": "Working in shifts", "t0": T.w(0, "shifts")}], y=200, w=480)])

    @shot(["The slave story came from Greek writers two thousand years later.", "And from Hollywood."], tail=2.2)
    def _(T):
        return (NIGHT, {"zoomFrom": 1, "zoomTo": 1.08, "y": 700},
                [stars(seed=6), ground(860), svg(pyramid(960, 865, 560, 360, "#5b4430", "#382818")),
                 stack([{"text": "Greek writers", "t0": T.w(0, "Greek")}, {"text": "Hollywood", "t0": T.w(1, "Hollywood"), "tone": "red"}], y=220, w=420),
                 {"type": "stamp", "text": "Myth", "x": CX, "y": 520, "size": 80, "t0": T.p(1) + T.d(1)},
                 tag("History Lab", T.p(1) + T.d(1) + .3, y=1000), cap("*follow* for more", T.p(1) + T.d(1) + .5, y=930, size=40)])
    return st

# ================================================================ 3. Weighing of the heart
def heart_trial():
    st = Story(); shot = st.shot

    @shot(["Ancient Egyptians believed that when you died, your heart was put on trial."])
    def _(T):
        return (HALL, {"zoomFrom": 1, "zoomTo": 1.15},
                [svg(heart(CX, 560, 2.2)),
                 cap("your heart", T.w(0, "heart"), y=300, size=56),
                 cap("put on *trial*", T.w(0, "trial"), y=380, size=56)])

    @shot(["The jackal god Anubis weighed it on a scale, against a single feather."])
    def _(T):
        return (HALL, {"zoomFrom": 1.05, "zoomTo": 1.12, "y": 600},
                [svg(scales(0)),
                 {"type": "namecard", "title": "ANUBIS", "sub": "God of the dead", "x": CX, "y": 220, "w": 360, "t0": T.w(0, "Anubis")},
                 {"type": "circle", "x": 1145, "y": 520, "rx": 80, "ry": 90, "t0": T.w(0, "feather")},
                 cap("vs a single *feather*", T.w(0, "feather"), y=980, size=40)])

    @shot(["The feather of Ma'at.", "Truth itself."])
    def _(T):
        return (HALL, {"zoomFrom": 1, "zoomTo": 1.15},
                [svg(feather(CX, 560, 2.6)),
                 {"type": "namecard", "title": "MA'AT", "sub": "Truth · order · justice", "x": CX, "y": 860, "w": 400, "t0": T.p(0)},
                 cap("*truth*", T.w(1, "Truth"), y=260, size=64)])

    @shot(["If your heart was heavier, weighed down by your wrongs,"])
    def _(T):
        return (HALL, {"zoomFrom": 1, "zoomTo": 1.1, "y": 600},
                [svg(scales(0), t1=T.w(0, "heavier")), svg(scales(16), t0=T.w(0, "heavier")),
                 cap("!heavier!", T.w(0, "heavier"), y=980, size=56)])

    @shot(["it was fed to Ammit.", "Part crocodile. Part lion. Part hippo."], thuds=[("fed", .2, 0)])
    def _(T):
        return ({"mode": "black"}, {},
                [{"type": "creature", "kind": "sharkFront", "mode": "silhouette", "threat": True, "x": CX, "y": 520, "scale": 1,
                  "approach": {"from": .25, "to": 1.6, "dur": 2.0, "t0": 0}, "bob": 2},
                 {"type": "namecard", "title": "AMMIT", "sub": "Devourer of the dead", "x": CX, "y": 220, "w": 420, "t0": T.w(0, "Ammit")},
                 stack([{"text": "Crocodile", "t0": T.w(1, "crocodile")}, {"text": "Lion", "t0": T.w(1, "lion")},
                        {"text": "Hippo", "t0": T.w(1, "hippo"), "tone": "red"}], y=760, w=360, size=28)])

    @shot(["And your soul was gone. Forever."])
    def _(T):
        return ({"mode": "black"}, {"zoomFrom": 1, "zoomTo": 1.05},
                [cap("your soul", T.w(0, "soul"), y=480, size=50),
                 {"type": "stamp", "text": "Gone forever", "x": CX, "y": 600, "size": 60, "t0": T.w(0, "Forever")}])

    @shot(["So they cheated.", "A carved scarab was placed over the heart, with a spell begging it not to testify against them."], chapter=True)
    def _(T):
        return ({"mode": "paper"}, {"zoomFrom": 1, "zoomTo": 1.06},
                [{"type": "doccard", "x": CX, "y": 520, "w": 540, "h": 700, "rotate": -2, "header": "Book of the Dead · Spell 30B",
                  "title": "O my heart,\ndo not testify\nagainst me", "footer": "Carved on a heart scarab", "t0": T.w(1, "spell") - .3},
                 cap("they *cheated*", T.w(0, "cheated"), y=500, size=60, t1=T.w(1, "spell") - .4),
                 {"type": "stamp", "text": "Cheat code", "x": CX, "y": 930, "size": 50, "color": "#3ecf6a", "t0": T.w(1, "testify")}])

    @shot(["And the brain?", "They pulled it out through the nose, with a hook, and threw it away."], chapter=True, thuds=[("threw", .3, 1)])
    def _(T):
        hook = svg('<path stroke="#c9ccd0" stroke-width="7" fill="none" stroke-linecap="round" d="M1250,640 L1150,566 L1010,470 C990,456 996,438 1014,444"/>', t0=T.w(1, "hook"))
        return (HALL, {"zoomFrom": 1, "zoomTo": 1.08},
                [skull_head(), hook,
                 prop(brain_markup(), 925, 470, .55, bob=0, moveTo={"x": 1260, "y": 610, "dur": 1.4, "t0": T.w(1, "pulled")}, t1=T.w(1, "threw") + .1),
                 cap("the *brain*?", T.p(0), y=220, size=56, t1=T.p(1) - .1),
                 cap("out through the *nose*", T.w(1, "nose"), y=220, size=40, t1=T.w(1, "threw") - .1),
                 cap("!thrown away!", T.w(1, "threw"), y=220, size=56)])

    @shot(["They kept the heart.", "And threw away the brain."], tail=2.2)
    def _(T):
        return (HALL, {"zoomFrom": 1, "zoomTo": 1.06},
                [svg(heart(CX, 420, 1.6)),
                 stack([{"text": "Heart · kept", "t0": T.w(0, "kept")}, {"text": "Brain · thrown away", "t0": T.w(1, "threw"), "tone": "red"}], y=600, w=500),
                 tag("History Lab", T.p(1) + T.d(1) + .3, y=1000), cap("*follow* for more", T.p(1) + T.d(1) + .5, y=930, size=40)])
    return st

if __name__ == "__main__":
    tts, root = sys.argv[1], sys.argv[2]
    which = sys.argv[3:] or ["cleopatra", "builders", "heart"]
    B = {"cleopatra": cleopatra, "builders": builders, "heart": heart_trial}
    for name in which:
        print("==", name)
        tokens = dict(TOKENS_EG)
        if name == "heart": tokens = {**TOKENS_EG, "creature": {**TOKENS_EG["creature"], "blob": ["#e38a9a"] * 3}}
        build(B[name](), tts, f"{root}/{name}", voice=VOICE, lang=LANG, speed=SPEED, width=1080, height=1920,
              gaps=(.32, .55, .22), lead=.3, tokens=tokens)
