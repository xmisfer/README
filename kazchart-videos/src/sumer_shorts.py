"""History Lab: three Mesopotamian (Sumer / ancient Iraq) myth Shorts (1080x1920). Visible column x 656-1264.
Usage: python3 sumer_shorts.py <tts_dir> <out_root> [flood|gilgamesh|inanna ...]"""
import random, sys
from kzlib import *
from egypt_shorts import svg, cap, tag, stack, CX, RED, VOICE, LANG, SPEED

TEAL, CLAY, CLAY_D, BRICK, BRICK_D, LAPIS, GOLD = "#3fd0b8", "#b98d5f", "#8a6640", "#c49a62", "#9c7444", "#26479c", "#e0b04a"
NIGHT = {"top": "#070b18", "bottom": "#2a2a40", "rays": False, "particleCount": 20}
DESERT = {"top": "#2c5a7a", "bottom": "#dcb27a", "rays": True, "rayOpacity": .05, "particleCount": 12}
STORM = {"top": "#0d1218", "bottom": "#2b3a46", "rays": False, "particleCount": 0}
UNDER = {"top": "#0a0405", "bottom": "#2a0e10", "rays": False, "particleCount": 25, "spotlight": {"x": 960, "w": 320}}
HALL = {"top": "#0d0a08", "bottom": "#2a1d10", "rays": False, "particleCount": 25, "spotlight": {"x": 960, "w": 360}}
TOKENS_SU = {"hl": TEAL, "creature": {**TOKENS["creature"], "blob": ["none", "none", "none"]}}
SAY = {"Utnapishtim": "Oot-napishtim", "Enkidu": "Enkeedoo", "Inanna": "Inahna", "Dumuzi": "Doomoozee", "Uruk": "Oorook",
       "Enki": "Enkee", "Gilgamesh": "Gilgamesh"}

# ---------------------------------------------------------------- Mesopotamian art
def wedge(x, y, s=1.0, rot=0):
    return f'<path transform="translate({x} {y}) rotate({rot}) scale({s})" d="M0,-8 L9,0 L0,8 Z M5,-3 L30,0 L5,3 Z" fill="currentColor"/>'

def cune_band(y, col=TEAL, op=.55, seed=1):
    r = random.Random(seed); s = f'<g color="{col}" opacity="{op}"><line x1="600" y1="{y - 10}" x2="1320" y2="{y - 10}" stroke="{col}" stroke-width="3"/><line x1="600" y1="{y + 44}" x2="1320" y2="{y + 44}" stroke="{col}" stroke-width="3"/>'
    for x in range(630, 1300, 34): s += wedge(x, y + 17 + r.uniform(-6, 6), .9, r.choice((0, 0, 90, 45)))
    return svg(s + '</g>')
def bands(): return [cune_band(18), cune_band(1014, seed=2)]

def tablet(x=CX, y=540, w=480, h=620, seed=3, rot=-2):
    r = random.Random(seed)
    s = f'<g transform="translate({x} {y}) rotate({rot})" color="#5e4128"><rect x="{-w/2}" y="{-h/2}" width="{w}" height="{h}" rx="34" fill="{CLAY}"/>'
    s += f'<rect x="{-w/2 + 16}" y="{-h/2 + 16}" width="{w - 32}" height="{h - 32}" rx="24" fill="none" stroke="{CLAY_D}" stroke-width="4" opacity=".6"/>'
    for row in range(int((h - 80) / 44)):
        yy = -h/2 + 60 + row * 44
        s += f'<line x1="{-w/2 + 40}" y1="{yy + 22}" x2="{w/2 - 40}" y2="{yy + 22}" stroke="{CLAY_D}" stroke-width="2" opacity=".5"/>'
        xx = -w/2 + 44
        while xx < w/2 - 70:
            s += wedge(xx, yy + 8, .7, r.choice((0, 0, 90, 45, -45))); xx += r.uniform(26, 40)
    s += f'<path d="M{w/2 - 60},{-h/2 + 40} L{w/2 - 120},{-h/2 + 140} L{w/2 - 90},{-h/2 + 220}" stroke="{CLAY_D}" stroke-width="5" fill="none" opacity=".7"/>'
    return svg(s + '</g>')

def ziggurat(x=CX, base=860, w=520, op=1):
    s = f'<g opacity="{op}">'
    for i, (ww, hh) in enumerate(((w, 120), (w * .72, 100), (w * .46, 90))):
        y0 = base - sum((120, 100, 90)[:i + 1])
        s += f'<rect x="{x - ww/2}" y="{y0}" width="{ww}" height="{hh}" fill="{BRICK if i % 2 == 0 else "#b58c56"}"/>'
        s += f'<rect x="{x - ww/2}" y="{y0}" width="{ww}" height="10" fill="{BRICK_D}" opacity=".5"/>'
    top = base - 310
    s += f'<rect x="{x - 50}" y="{top - 60}" width="100" height="60" fill="{BRICK_D}"/><rect x="{x - 14}" y="{top - 40}" width="28" height="40" fill="#3a2a1a"/>'
    s += f'<polygon points="{x - 40},{base} {x + 40},{base} {x + 22},{top} {x - 22},{top}" fill="#d9b37a"/>'
    for k in range(1, 14): s += f'<line x1="{x - 40 + k * 1.4}" y1="{base - k * 23.8}" x2="{x + 40 - k * 1.4}" y2="{base - k * 23.8}" stroke="{BRICK_D}" stroke-width="2"/>'
    return svg(s + '</g>')

def palm(x, base, s=1.0, flip=1):
    g = f'<g transform="translate({x} {base}) scale({s * flip} {s})"><path d="M0,0 C10,-80 0,-160 20,-240" stroke="#5a3f24" stroke-width="16" fill="none"/>'
    for a, l in ((-160, 120), (-120, 130), (-60, 130), (-20, 120), (-90, 110)):
        import math
        ex, ey = 20 + l * math.cos(math.radians(a)), -240 + l * math.sin(math.radians(a)) + 40
        g += f'<path d="M20,-240 Q{(20 + ex) / 2},{-280} {ex},{ey}" stroke="#3f6b3a" stroke-width="18" fill="none" stroke-linecap="round"/>'
    return g + '</g>'

def ground(y=860, col="#c9a46a"):
    return svg(f'<rect x="-600" y="{y}" width="3120" height="900" fill="{col}"/><rect x="-600" y="{y + 70}" width="3120" height="40" fill="#3a7aa0" opacity=".85"/>')

def stars(n=60, seed=3, moon=(1190, 380)):
    r = random.Random(seed); mx, my = moon or (0, 0)
    return svg("".join(f'<circle cx="{r.uniform(600, 1320):.0f}" cy="{r.uniform(10, 560):.0f}" r="{r.uniform(1, 2.4):.1f}" fill="#f4efe0" opacity="{r.uniform(.3, .8):.2f}"/>' for _ in range(n))
               + (f'<path d="M{mx},{my} a46,46 0 1,0 30,80 a36,36 0 1,1 -30,-80 Z" fill="#efe6cf"/>' if moon else ''))

def rain(op=.35, seed=4):
    r = random.Random(seed)
    return svg(f'<g stroke="#9fb6c8" stroke-width="3" opacity="{op}">' + "".join(
        f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x - 24:.0f}" y2="{y + 70:.0f}"/>' for x, y in ((r.uniform(600, 1360), r.uniform(-20, 1000)) for _ in range(90))) + '</g>')

def waves(y=760, col="#1f4a63"):
    d = f"M-600,{y} " + " ".join(f"Q{x + 40},{y - 26} {x + 80},{y}" for x in range(-600, 2520, 80))
    return svg(f'<path d="{d} L2520,{y + 900} L-600,{y + 900} Z" fill="{col}"/><path d="{d}" stroke="#9fd0e0" stroke-width="4" fill="none" opacity=".5"/>')

def cube_boat():
    s = '<rect x="-170" y="-300" width="340" height="340" fill="#6b4a2b"/>'
    s += ''.join(f'<line x1="-170" y1="{y}" x2="170" y2="{y}" stroke="#4a3220" stroke-width="5"/>' for y in range(-260, 40, 42))
    s += '<rect x="-170" y="-300" width="340" height="340" fill="none" stroke="#3a2614" stroke-width="10"/><rect x="-30" y="-120" width="60" height="80" fill="#2a1a0c"/>'
    s += '<rect x="-190" y="-318" width="380" height="24" fill="#4a3220"/>'
    return s

def bird(col="#f4f1ea"):
    return (f'<path fill="{col}" d="M-50,0 C-20,-10 20,-10 50,0 C20,8 -20,8 -50,0 Z"/><path fill="{col}" d="M-10,-4 L-40,-60 L20,-6 Z"/>'
            f'<path fill="{col}" d="M50,0 L66,-6 L62,4 Z"/>')

def king_head(x=CX, y=560, s=1.0):
    g = f'<g transform="translate({x} {y}) scale({s})">'
    g += '<path fill="#c58f5f" d="M-120,-60 C-120,-200 100,-210 120,-80 L150,-20 L130,-6 L132,30 L110,40 L-60,40 L-100,20 Z"/>'
    g += '<path fill="#1d1410" d="M-130,-110 C-110,-230 110,-240 130,-110 L120,-80 C80,-150 -60,-160 -110,-60 Z"/>'
    g += '<path fill="#1d1410" d="M-110,-40 C-170,10 -150,120 -100,150 L-110,-10 Z"/>'
    g += '<path fill="#1d1410" d="M-40,10 L120,20 L100,250 L-20,250 Z"/>'
    for row in range(5):
        for k in range(5):
            g += f'<circle cx="{-4 + k * 24}" cy="{50 + row * 42}" r="9" fill="none" stroke="#5a4030" stroke-width="3"/>'
    g += '<path fill="#fff" d="M50,-70 C66,-82 92,-80 104,-70 C90,-60 64,-60 50,-70 Z"/><circle cx="80" cy="-70" r="8" fill="#1d1410"/>'
    g += f'<path fill="{GOLD}" d="M-120,-150 C-90,-215 90,-225 124,-150 L118,-128 C80,-180 -80,-180 -114,-128 Z"/>'
    return svg(g + '</g>')

def figure(col="#1d1410"):
    return (f'<circle cx="0" cy="-150" r="22" fill="{col}"/><path fill="{col}" d="M-28,-124 L28,-124 L36,40 L-36,40 Z"/>'
            f'<path stroke="{col}" stroke-width="12" stroke-linecap="round" d="M-14,40 L-16,110 M14,40 L16,110"/>'
            f'<rect x="-34" y="110" width="30" height="24" rx="6" fill="#6f6a62"/><rect x="4" y="110" width="30" height="24" rx="6" fill="#6f6a62"/>')

def plant(x, y, s=1.0, glow=True):
    g = f'<g transform="translate({x} {y}) scale({s})">'
    if glow: g += f'<circle cx="0" cy="-120" r="140" fill="{TEAL}" opacity=".18"/>'
    g += '<path d="M0,0 C-10,-60 10,-120 0,-200" stroke="#2f6a4a" stroke-width="12" fill="none"/>'
    for i, yy in enumerate(range(-30, -200, -30)):
        d = 1 if i % 2 else -1
        g += f'<path d="M0,{yy} L{d * 34},{yy - 16} L{d * 6},{yy - 8} Z" fill="#2f6a4a"/>'
    for fx, fy in ((0, -210), (-40, -150), (40, -120)):
        g += f'<circle cx="{fx}" cy="{fy}" r="18" fill="{TEAL}"/><circle cx="{fx}" cy="{fy}" r="7" fill="#e9fff9"/>'
    return g + '</g>'

def snake_markup(col="#6b7a3a"):
    return (f'<path d="M-220,0 C-180,-40 -140,40 -100,0 C-60,-40 -20,40 20,0 C50,-28 80,-24 110,-10" stroke="{col}" stroke-width="26" fill="none" stroke-linecap="round"/>'
            f'<ellipse cx="128" cy="-12" rx="34" ry="22" fill="{col}"/><circle cx="138" cy="-20" r="5" fill="#f2e35b"/><path d="M160,-10 l18,-5 M160,-10 l18,5" stroke="{RED}" stroke-width="3"/>')

def city_walls(y=860):
    s = f'<rect x="560" y="{y - 220}" width="800" height="220" fill="{BRICK}"/>'
    s += ''.join(f'<rect x="{x}" y="{y - 250}" width="30" height="30" fill="{BRICK}"/>' for x in range(570, 1360, 50))
    for tx in (680, 960, 1240):
        s += f'<rect x="{tx - 50}" y="{y - 320}" width="100" height="320" fill="#b58c56"/>' + ''.join(f'<rect x="{tx - 50 + k * 34}" y="{y - 348}" width="24" height="28" fill="#b58c56"/>' for k in range(3))
    s += f'<path d="M920,{y} L920,{y - 110} A40,40 0 0 1 1000,{y - 110} L1000,{y} Z" fill="#3a2a1a"/>'
    return svg(s)

def gate(x=CX, y=880, s=1.0):
    return svg(f'<g transform="translate({x} {y}) scale({s})"><rect x="-230" y="-520" width="460" height="520" fill="{LAPIS}"/>'
               + ''.join(f'<circle cx="{-200 + k * 40}" cy="-490" r="9" fill="{GOLD}"/>' for k in range(11)) +
               f'<path d="M-130,0 L-130,-300 A130,130 0 0 1 130,-300 L130,0 Z" fill="#05030a"/>'
               f'<path d="M-150,0 L-150,-300 A150,150 0 0 1 150,-300 L150,0" stroke="{GOLD}" stroke-width="10" fill="none"/></g>')

def hook():
    return svg(f'<line x1="960" y1="-20" x2="960" y2="420" stroke="#8a8f94" stroke-width="10"/>'
               f'<path d="M960,420 C960,520 1060,520 1060,440 L1040,450" stroke="#8a8f94" stroke-width="16" fill="none" stroke-linecap="round"/>'
               f'<circle cx="960" cy="560" r="220" fill="{RED}" opacity=".08"/>')

def eye(x=CX, y=520, s=1.0):
    return svg(f'<g transform="translate({x} {y}) scale({s})"><path fill="#e9e1cf" d="M-220,0 C-120,-130 120,-130 220,0 C120,130 -120,130 -220,0 Z"/>'
               f'<circle r="86" fill="{RED}"/><circle r="40" fill="#120607"/><circle cx="-24" cy="-26" r="14" fill="#fff" opacity=".8"/>'
               f'<path d="M-220,0 C-120,-130 120,-130 220,0" stroke="#120607" stroke-width="16" fill="none"/></g>')

def throne(x=CX, y=820):
    return svg(f'<g transform="translate({x} {y})"><rect x="-150" y="-420" width="300" height="420" rx="10" fill="{GOLD}"/><rect x="-170" y="-170" width="340" height="60" fill="#b8892f"/>'
               f'<rect x="-150" y="-110" width="40" height="110" fill="#b8892f"/><rect x="110" y="-110" width="40" height="110" fill="#b8892f"/>'
               f'<circle cx="0" cy="-300" r="36" fill="#c58f5f"/><path d="M-36,-330 C-30,-370 30,-370 36,-330 Z" fill="#1d1410"/>'
               f'<path fill="{LAPIS}" d="M-70,-262 L70,-262 L90,-110 L-90,-110 Z"/><path fill="{GOLD}" d="M-70,-262 L70,-262 L62,-236 L-62,-236 Z" opacity=".8"/>'
               f'<path stroke="{LAPIS}" stroke-width="30" d="M-50,-110 L-50,-10 M50,-110 L50,-10"/></g>')

def endcard(t0):
    return [tag("History Lab", t0 + .3, y=990), cap("*follow* for more", t0 + .5, y=920, size=40)]

# ================================================================ 1. The flood
def flood():
    st = Story(); shot = st.shot

    @shot(["Centuries before the story of Noah was written down, ancient Iraq already had a flood hero."])
    def _(T):
        return (STORM, {"zoomFrom": 1, "zoomTo": 1.1},
                bands() + [rain(), waves(820), prop(cube_boat(), CX, 800, .8, bob=10),
                 cap("before noah", 0, y=200, size=58),
                 cap("there was a *flood hero*", T.w(0, "flood"), y=275, size=40)])

    @shot(["His name was Utnapishtim.", "His story is told in the Epic of Gilgamesh."], chapter=True)
    def _(T):
        return (HALL, {"zoomFrom": 1, "zoomTo": 1.06},
                [tablet(CX, 560, 460, 600), {"type": "namecard", "title": "UTNAPISHTIM", "sub": "The flood hero", "x": CX, "y": 190, "w": 420, "t0": T.w(0, "Utnapishtim")},
                 {"type": "pill", "text": "Epic of Gilgamesh · tablet XI", "x": 690, "y": 900, "size": 24, "t0": T.w(1, "Epic")}])

    @shot(["The gods decided to wipe out humanity.", "But one god warned him, in secret."])
    def _(T):
        return (NIGHT, {"zoomFrom": 1, "zoomTo": 1.1, "y": 700},
                [stars(), ground(860), ziggurat(CX, 862, 460), svg(palm(700, 862, .9) + palm(1220, 862, .8, -1)),
                 cap("wipe out *humanity*", T.w(0, "humanity"), y=200, size=46, t1=T.p(1) - .1),
                 cap("warned *in secret*", T.w(1, "secret"), y=200, size=48)])

    @shot(["Tear down your house.", "Build a boat."])
    def _(T):
        return ({"mode": "black"}, {},
                [cap("tear down your house", T.p(0), y=470, size=42), cap("*build a boat*", T.p(1), y=550, size=60)])

    @shot(["And the boat was a giant cube.", "About sixty metres on every side."])
    def _(T):
        return (STORM, {"zoomFrom": 1, "zoomTo": 1.08},
                [waves(860), prop(cube_boat(), CX, 860, 1.1, bob=6),
                 {"type": "bracket", "x1": 760, "y1": 920, "x2": 1160, "y2": 920, "color": TEAL, "label": "~60 M", "t0": T.w(1, "sixty")},
                 cap("a giant *cube*", T.w(0, "cube"), y=220, size=60)])

    @shot(["The storm raged for six days and seven nights.", "Even the gods were terrified, cowering like dogs."], thuds=[("storm", .1, 0)])
    def _(T):
        return (STORM, {"zoomFrom": 1, "zoomTo": 1.12},
                [rain(.55), waves(760), prop(cube_boat(), CX, 760, .7, bob=26, rotate=6),
                 svg('<polygon points="1100,0 1060,180 1110,180 1050,380 1170,140 1120,140 1170,0" fill="#fff6c8" opacity=".9"/>', t0=T.w(0, "storm"), t1=T.w(0, "storm") + .4),
                 cap("6 days · 7 nights", T.w(0, "six"), y=200, size=46, t1=T.p(1) - .1),
                 cap("gods *cowering*", T.w(1, "cowering"), y=200, size=56)])

    @shot(["When the boat landed on a mountain, he sent out a dove, then a swallow, then a raven.", "The raven never came back."])
    def _(T):
        return (DESERT, {"zoomFrom": 1, "zoomTo": 1.06},
                [svg('<polygon points="560,900 860,560 960,620 1100,500 1380,900" fill="#6f7d5a"/>'), waves(900, "#2f6a85"),
                 prop(cube_boat(), 900, 640, .6, bob=0),
                 prop(bird(), 900, 500, .9, bob=6, t0=T.w(0, "dove"), swim={"vx": 60, "vy": -40}),
                 prop(bird("#2b3a6b"), 900, 500, .8, bob=6, t0=T.w(0, "swallow"), swim={"vx": -40, "vy": -50}),
                 prop(bird("#0b0b0b"), 900, 500, 1.0, bob=6, t0=T.w(0, "raven"), swim={"vx": 130, "vy": -60}),
                 stack([{"text": "Dove · came back", "t0": T.w(0, "dove")}, {"text": "Swallow · came back", "t0": T.w(0, "swallow")},
                        {"text": "Raven · never returned", "t0": T.w(1, "never"), "tone": "red"}], y=760, w=520, size=26, gap=72)])

    @shot(["In eighteen seventy-two, the man who first translated it got so excited, he reportedly started taking off his clothes."], chapter=True)
    def _(T):
        return (HALL, {"zoomFrom": 1, "zoomTo": 1.08},
                [tablet(CX, 520, 420, 540, seed=8, rot=3), tag("London · 1872"),
                 {"type": "namecard", "title": "GEORGE SMITH", "sub": "Assyriologist", "x": CX, "y": 880, "w": 400, "t0": T.w(0, "man")},
                 {"type": "stamp", "text": "Too excited", "x": CX, "y": 420, "size": 56, "t0": T.w(0, "clothes")}])

    @shot(["Some stories are much older than you think."], tail=2.2)
    def _(T):
        end = T.p(0) + T.d(0)
        return (NIGHT, {"zoomFrom": 1.06, "zoomTo": 1, "y": 700},
                bands() + [stars(seed=9), ground(860), ziggurat(CX, 862, 460),
                 cap("much *older*", T.w(0, "older"), y=250, size=60), cap("than you think", T.w(0, "think"), y=320, size=44)] + endcard(end))
    return st

# ================================================================ 2. Gilgamesh
def gilgamesh():
    st = Story(); shot = st.shot

    @shot(["The world's oldest epic is about a king who was terrified of dying."])
    def _(T):
        return (HALL, {"zoomFrom": 1, "zoomTo": 1.1},
                bands() + [king_head(CX, 620, 1.3),
                 cap("a king afraid", 0, y=200, size=54), cap("of *dying*", T.w(0, "dying"), y=275, size=60)])

    @shot(["Gilgamesh, king of Uruk.", "Two thirds god. One third man."], chapter=True)
    def _(T):
        return (DESERT, {"zoomFrom": 1, "zoomTo": 1.06, "y": 700},
                [city_walls(880), svg('<rect x="-600" y="880" width="3120" height="400" fill="#c9a46a"/>'),
                 {"type": "namecard", "title": "GILGAMESH", "sub": "King of Uruk · c. 2700 BC", "x": CX, "y": 200, "w": 440, "t0": T.p(0)},
                 stack([{"text": "2/3 god", "t0": T.w(1, "god")}, {"text": "1/3 man", "t0": T.w(1, "man")}], y=330, w=300, x=810, size=30)])

    @shot(["When his best friend Enkidu died,", "Gilgamesh saw his own death coming."])
    def _(T):
        return (NIGHT, {"zoomFrom": 1, "zoomTo": 1.1},
                [stars(seed=5), king_head(CX, 600, 1.1),
                 {"type": "pill", "text": "Enkidu · his best friend", "x": 720, "y": 900, "size": 26, "t0": T.w(0, "Enkidu"), "tone": "red"},
                 cap("his own *death*", T.w(1, "death"), y=200, size=56)])

    @shot(["He learned of a plant, at the bottom of the sea, that could make an old man young again."], chapter=True)
    def _(T):
        return ({"depth": .85, "seabed": "dark", "seabedY": 900}, {"zoomFrom": 1, "zoomTo": 1.15, "y": 760},
                [svg(plant(CX, 900, 1.3)),
                 cap("make you *young*", T.w(0, "young"), y=220, size=54), cap("again", T.w(0, "again"), y=290, size=48)])

    @shot(["He tied stones to his feet, sank to the seabed, and pulled it up."])
    def _(T):
        return ({"depth": .8, "seabed": "dark", "seabedY": 900}, {"zoomFrom": 1, "zoomTo": 1.08},
                [svg(plant(1110, 900, .9), t1=T.w(0, "pulled")),
                 prop(figure(), 920, 180, .9, bob=0, moveTo={"x": 920, "y": 720, "dur": 2.4, "t0": T.w(0, "sank") - .4}),
                 svg(plant(1010, 640, .6, glow=True), t0=T.w(0, "pulled")),
                 cap("stones tied to his *feet*", T.w(0, "feet"), y=990, size=40)])

    @shot(["On the way home, he stopped to bathe in a pool.", "A snake smelled the plant, crept out, and ate it."], thuds=[("ate", .2, 1)])
    def _(T):
        return (DESERT, {"zoomFrom": 1, "zoomTo": 1.1, "y": 760},
                [svg('<rect x="-600" y="760" width="3120" height="600" fill="#c9a46a"/><ellipse cx="1040" cy="880" rx="260" ry="70" fill="#3a7aa0"/>'),
                 svg(plant(760, 840, .6), t1=T.w(1, "ate")),
                 prop(snake_markup(), 1400, 830, .9, bob=0, flip=True, t0=T.w(1, "snake") - .2, moveTo={"x": 860, "y": 830, "dur": 1.4, "t0": T.w(1, "snake")}),
                 cap("he stopped to *bathe*", T.w(0, "bathe"), y=220, size=46, t1=T.p(1) - .1),
                 {"type": "stamp", "text": "Stolen", "x": CX, "y": 400, "size": 70, "t0": T.w(1, "ate") + .2}])

    @shot(["Then it shed its skin.", "An ancient answer to why snakes shed their skin."])
    def _(T):
        return (DESERT, {"zoomFrom": 1.05, "zoomTo": 1.15, "y": 760},
                [svg('<rect x="-600" y="760" width="3120" height="600" fill="#c9a46a"/>'),
                 prop(snake_markup("#d9cfa8"), 860, 830, .9, bob=0, flip=True, opacity=.6),
                 prop(snake_markup(), 860, 830, .9, bob=0, flip=True, swim={"vx": -70}),
                 cap("it *shed its skin*", T.w(0, "shed"), y=220, size=50, t1=T.p(1) - .1),
                 cap("why snakes *renew*", T.w(1, "why"), y=220, size=46)])

    @shot(["Gilgamesh wept.", "Then he went home, and looked at the great walls of his city."], chapter=True)
    def _(T):
        return (DESERT, {"zoomFrom": 1.1, "zoomTo": 1, "y": 700},
                [city_walls(880), svg('<rect x="-600" y="880" width="3120" height="400" fill="#c9a46a"/>'),
                 cap("gilgamesh *wept*", T.p(0), y=200, size=54, t1=T.p(1) - .1),
                 cap("his *walls* would last", T.w(1, "walls"), y=200, size=46)])

    @shot(["Four thousand years later, we still know his name."], tail=2.2)
    def _(T):
        end = T.p(0) + T.d(0)
        return (HALL, {"zoomFrom": 1.06, "zoomTo": 1},
                bands() + [tablet(CX, 660, 380, 440, seed=12),
                 {"type": "bignumber", "from": 0, "to": 4000, "suffix": " yrs", "x": CX, "y": 250, "size": 96, "color": "#f4efe0", "t0": T.p(0), "dur": 1.2},
                 cap("we still know his *name*", T.w(0, "name"), y=330, size=40)] + endcard(end))
    return st

# ================================================================ 3. Inanna
def inanna():
    st = Story(); shot = st.shot

    @shot(["A goddess went to the underworld, and sent her husband to take her place."])
    def _(T):
        return (UNDER, {"zoomFrom": 1, "zoomTo": 1.1},
                bands() + [gate(CX, 900, 1.0),
                 cap("she sent her", 0, y=200, size=54), cap("*husband* instead", T.w(0, "husband"), y=275, size=54)])

    @shot(["Inanna, queen of heaven, went to visit her sister, the queen of the dead."], chapter=True)
    def _(T):
        return (NIGHT, {"zoomFrom": 1, "zoomTo": 1.08},
                [stars(seed=7, moon=(1170, 600)), svg('<polygon points="960,380 985,450 1060,450 1000,495 1022,566 960,522 898,566 920,495 860,450 935,450" fill="#e0b04a"/>'),
                 {"type": "namecard", "title": "INANNA", "sub": "Queen of heaven", "x": CX, "y": 200, "w": 380, "t0": T.p(0)},
                 {"type": "namecard", "title": "ERESHKIGAL", "sub": "Queen of the dead", "x": CX, "y": 760, "w": 420, "t0": T.w(0, "sister")}])

    @shot(["At each of the seven gates, she had to give something up.", "Her crown. Her jewels. Her robe."])
    def _(T):
        return (UNDER, {"zoomFrom": 1, "zoomTo": 1.25, "y": 620},
                [gate(CX, 900, 1.0),
                 {"type": "bignumber", "from": 1, "to": 7, "prefix": "GATE ", "x": CX, "y": 220, "size": 80, "color": "#f4efe0", "t0": T.w(0, "seven"), "dur": T.dur - T.w(0, "seven") - .4},
                 stack([{"text": "Crown", "t0": T.w(1, "crown")}, {"text": "Jewels", "t0": T.w(1, "jewels")}, {"text": "Robe", "t0": T.w(1, "robe"), "tone": "red"}], y=300, w=300, x=810, size=28, gap=70)])

    @shot(["At the last gate, she stood naked before the judges of the dead."])
    def _(T):
        return (UNDER, {"zoomFrom": 1, "zoomTo": 1.08},
                [gate(CX, 1000, 1.2), cap("*judged*", T.w(0, "judges"), y=220, size=72)])

    @shot(["Her sister killed her with a look, and hung her body on a hook."], thuds=[("hook", .1, 0)])
    def _(T):
        return ({"mode": "black"}, {"zoomFrom": 1, "zoomTo": 1.08},
                [eye(CX, 520, 1.1) | {"t1": T.w(0, "hung") - .1},
                 hook() | {"t0": T.w(0, "hung")},
                 cap("killed with a *look*", T.w(0, "look"), y=900, size=46, t1=T.w(0, "hung") - .1),
                 cap("!hung on a hook!", T.w(0, "hook"), y=900, size=50)])

    @shot(["Then the god Enki made two tiny creatures from the dirt under his fingernails, to bring her back."], chapter=True)
    def _(T):
        fig = lambda x: f'<g transform="translate({x} 620) scale(.45)"><circle cx="0" cy="-150" r="60" fill="{TEAL}" opacity=".25"/>{figure("#3fd0b8")}</g>'
        return (HALL, {"zoomFrom": 1, "zoomTo": 1.12},
                [{"type": "namecard", "title": "ENKI", "sub": "God of wisdom", "x": CX, "y": 200, "w": 360, "t0": T.w(0, "Enki")},
                 svg(fig(880) + fig(1040), t0=T.w(0, "tiny")),
                 cap("from fingernail *dirt*", T.w(0, "dirt"), y=900, size=44)])

    @shot(["But someone had to take her place.", "She found her husband Dumuzi on his throne, in fine clothes, not mourning her at all."])
    def _(T):
        return (HALL, {"zoomFrom": 1, "zoomTo": 1.1},
                [throne(CX, 860) | {"t0": T.w(1, "Dumuzi") - .3},
                 cap("someone had to *replace* her", T.p(0), y=200, size=36, t1=T.p(1) - .1),
                 {"type": "namecard", "title": "DUMUZI", "sub": "Her husband", "x": CX, "y": 200, "w": 360, "t0": T.w(1, "Dumuzi")},
                 {"type": "pill", "text": "Not mourning", "x": 800, "y": 930, "size": 28, "tone": "red", "t0": T.w(1, "mourning")}])

    @shot(["So she chose him."], thuds=[("chose", .2, 0)])
    def _(T):
        return ({"mode": "black"}, {},
                [throne(CX, 820), {"type": "stamp", "text": "Him", "x": CX, "y": 300, "size": 100, "t0": T.w(0, "chose") + .1}])

    @shot(["In the end, Dumuzi and his sister split the sentence.", "Half a year each, below the earth."], tail=2.2)
    def _(T):
        end = T.p(1) + T.d(1)
        return (NIGHT, {"zoomFrom": 1, "zoomTo": 1.04},
                bands() + [stars(seed=11, moon=None),
                 {"type": "meter", "title": "Time in the underworld", "x": 710, "y": 520, "w": 500, "value": .5, "number": 6, "unit": "months", "sub": "each, every year", "t0": T.p(1) - .2, "dur": 1.0},
                 cap("they *split* it", T.w(0, "split"), y=200, size=52)] + endcard(end))
    return st

if __name__ == "__main__":
    tts, root = sys.argv[1], sys.argv[2]
    which = sys.argv[3:] or ["flood", "gilgamesh", "inanna"]
    B = {"flood": flood, "gilgamesh": gilgamesh, "inanna": inanna}
    for name in which:
        print("==", name)
        build(B[name](), tts, f"{root}/{name}", voice=VOICE, lang=LANG, speed=SPEED, width=1080, height=1920,
              gaps=(.32, .55, .22), lead=.3, tokens=TOKENS_SU, say=SAY)
