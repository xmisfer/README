"""History Lab: three Norse myth Shorts (1080x1920). Visible world column x 656-1264, centre 960.
Usage: python3 norse_shorts.py <tts_dir> <out_root> [helmets|loki|ragnarok ...]"""
import math, random, sys
from kzlib import *
from egypt_shorts import svg, cap, tag, stack, CX, RED, VOICE, LANG, SPEED

ICE, IRON, IRON_D, SNOW = "#7fd4ff", "#6f7780", "#454c54", "#dfe9f0"
NIGHT = {"top": "#050a14", "bottom": "#16283c", "rays": False, "particleCount": 45}
DUSK = {"top": "#0a0f1e", "bottom": "#3a2a3a", "rays": False, "particleCount": 30}
FORGE = {"top": "#0c0a0a", "bottom": "#241a14", "rays": False, "particleCount": 25, "spotlight": {"x": 960, "w": 340}}
DAWN = {"top": "#3d6f8f", "bottom": "#e9c48a", "rays": True, "rayOpacity": .08, "particleCount": 10}
TOKENS_NO = {"hl": ICE, "creature": {**TOKENS["creature"], "blob": ["none", "none", "none"]}}
SAY = {"Gjermundbu": "Yermoondboo", "Veksø": "Veksuh", "Sleipnir": "Slaypneer", "Jörmungandr": "Yormungand",
       "Ragnarök": "Ragnarok", "Surtr": "Surt", "Lífthrasir": "Leefthrasseer", "Líf": "Leef", "Fimbulwinter": "Fimbul winter",
       "Svadilfari": "Svathilfari", "Doepler": "Dopler"}

# ---------------------------------------------------------------- Norse art
RUNES = ["M0,0 L0,40 M0,8 L16,0 M0,20 L16,12", "M0,40 L0,0 L16,12 L16,40", "M0,0 L0,40 M0,10 L14,20 L0,30",
         "M0,0 L0,40 M0,4 L14,14 M0,16 L14,26", "M0,40 L0,0 L14,10 L0,20 L14,40", "M0,0 L16,20 L0,40 M16,0 L0,20 L16,40",
         "M8,0 L8,40 M0,10 L16,30", "M0,0 L0,40 M16,0 L16,40 M0,12 L16,28"]
def rune_band(y, col=ICE, op=.55, seed=1):
    r = random.Random(seed); s = f'<g stroke="{col}" stroke-width="3.5" fill="none" stroke-linecap="round" opacity="{op}">'
    s += f'<line x1="600" y1="{y - 10}" x2="1320" y2="{y - 10}"/><line x1="600" y1="{y + 50}" x2="1320" y2="{y + 50}"/>'
    for x in range(640, 1300, 38): s += f'<path transform="translate({x} {y})" d="{r.choice(RUNES)}"/>'
    return svg(s + '</g>')
def bands(): return [rune_band(18), rune_band(1012, seed=2)]

def aurora(op=.4):
    s = '<defs><linearGradient id="aur" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#57e39a" stop-opacity="0"/><stop offset=".55" stop-color="#57e39a" stop-opacity=".9"/><stop offset="1" stop-color="#3fb4e0" stop-opacity="0"/></linearGradient></defs>'
    for i, (y, a) in enumerate(((140, 60), (230, 45), (320, 35))):
        d = f"M560,{y} " + " ".join(f"Q{x + 60},{y - a + (i * 13) % 30} {x + 120},{y}" for x in range(560, 1400, 120))
        s += f'<path d="{d} L1400,{y + 160} L560,{y + 160} Z" fill="url(#aur)" opacity="{op * (1 - i * .25)}"/>'
    return svg(s)

def mountains(y=860, snow=True):
    s = f'<polygon fill="#1b2c40" points="560,{y} 700,{y - 260} 820,{y - 120} 960,{y - 330} 1110,{y - 140} 1230,{y - 280} 1380,{y}"/>'
    if snow: s += f'<polygon fill="{SNOW}" opacity=".85" points="925,{y - 285} 960,{y - 330} 995,{y - 282} 975,{y - 290} 960,{y - 272} 945,{y - 292}"/><polygon fill="{SNOW}" opacity=".8" points="1205,{y - 245} 1230,{y - 280} 1256,{y - 244} 1230,{y - 256}"/><polygon fill="{SNOW}" opacity=".8" points="678,{y - 228} 700,{y - 260} 722,{y - 228} 700,{y - 240}"/>'
    s += f'<polygon fill="#0e1824" points="560,{y} 760,{y - 150} 880,{y - 60} 1040,{y - 190} 1200,{y - 70} 1380,{y - 120} 1380,{y + 400} 560,{y + 400}"/>'
    s += f'<rect x="-600" y="{y}" width="3120" height="900" fill="#0b141e"/>'
    return svg(s)

def stars(n=60, seed=3):
    r = random.Random(seed)
    return svg("".join(f'<circle cx="{r.uniform(600, 1320):.0f}" cy="{r.uniform(10, 560):.0f}" r="{r.uniform(1, 2.4):.1f}" fill="#eef4ff" opacity="{r.uniform(.3, .8):.2f}"/>' for _ in range(n)))

def horned_helmet(x=CX, y=560, s=1.0):
    return svg(f'<g transform="translate({x} {y}) scale({s})">'
               f'<path d="M-130,-40 C-220,-60 -250,-170 -210,-260 C-200,-180 -170,-120 -110,-90" fill="#efe6cf"/>'
               f'<path d="M130,-40 C220,-60 250,-170 210,-260 C200,-180 170,-120 110,-90" fill="#efe6cf"/>'
               f'<path fill="{IRON}" d="M-150,30 C-150,-150 150,-150 150,30 Z"/><rect x="-160" y="20" width="320" height="34" rx="8" fill="{IRON_D}"/>'
               f'<path fill="#000" opacity=".2" d="M40,-118 C110,-100 150,-50 150,30 L90,30 C100,-30 80,-80 40,-118 Z"/></g>')

def spectacle_helmet(x=CX, y=560, s=1.0):
    return svg(f'<g transform="translate({x} {y}) scale({s})">'
               f'<path fill="{IRON}" d="M-150,40 C-150,-170 150,-170 150,40 Z"/><path d="M0,-130 L0,40" stroke="{IRON_D}" stroke-width="16"/>'
               f'<path d="M-150,-20 L150,-20" stroke="{IRON_D}" stroke-width="12"/>'
               f'<path fill="{IRON_D}" d="M-120,30 L120,30 L120,48 C120,110 70,120 40,96 L0,60 L-40,96 C-70,120 -120,110 -120,48 Z"/>'
               f'<ellipse cx="-58" cy="62" rx="34" ry="24" fill="#05090d"/><ellipse cx="58" cy="62" rx="34" ry="24" fill="#05090d"/>'
               f'<path fill="#000" opacity=".2" d="M40,-128 C110,-110 150,-60 150,40 L100,40 C110,-30 90,-90 40,-128 Z"/></g>')

def sleipnir(x=CX, y=600, s=1.0, col="#c9d4de"):
    g = f'<g transform="translate({x} {y}) scale({s})" fill="{col}" stroke="{col}">'
    g += '<ellipse cx="0" cy="0" rx="170" ry="62" stroke="none"/><path stroke="none" d="M110,-44 L168,-118 C182,-134 214,-136 230,-118 L282,-60 C292,-46 278,-34 264,-40 L222,-62 L186,-30 L170,14 Z"/>'
    g += '<path stroke="none" d="M176,-124 L186,-162 L200,-128 Z"/><path stroke="none" d="M112,-46 L160,-120 L150,-96 L128,-70 Z" opacity=".7"/><path fill="none" stroke-width="14" stroke-linecap="round" d="M-165,-10 C-230,10 -240,80 -220,130"/>'
    for i, lx in enumerate((70, 95, 120, 145, -150, -125, -100, -75)):
        sw = (-1) ** i * 10
        g += f'<path fill="none" stroke-width="13" stroke-linecap="round" d="M{lx},30 L{lx + sw},110 L{lx + sw * .4},180"/>'
    g += '<circle cx="214" cy="-100" r="6" fill="#05090d" stroke="none"/></g>'
    return svg(g)

def wall(x=CX, y=700, w=560, rows=6):
    s = ''
    for r in range(rows):
        for c in range(-1, int(w / 80) + 1):
            bx = x - w / 2 + c * 80 + (40 if r % 2 else 0)
            if bx < x - w / 2 - 20 or bx > x + w / 2 - 60: continue
            s += f'<rect x="{bx}" y="{y - (r + 1) * 46}" width="76" height="42" rx="4" fill="{"#8b939b" if (r + c) % 3 else "#737b83"}"/>'
    return svg(s)

def wolf(x=CX, y=560, s=1.0, eye=True):
    g = (f'<g transform="translate({x} {y}) scale({s})"><path fill="#2a3442" d="M-200,60 L-140,-40 L-120,-160 L-76,-62 L-40,-72 L-6,-170 L30,-60 '
         f'C80,-50 150,-30 222,0 L240,22 L202,42 L150,46 L122,84 L60,72 L0,112 L-120,140 Z"/>')
    g += '<path fill="#fff" d="M130,46 L138,62 L146,46 L156,62 L164,46 L174,60 L182,44 Z"/>'
    if eye: g += '<circle cx="40" cy="-22" r="22" fill="#f2c14e" opacity=".3"/><circle cx="40" cy="-22" r="10" fill="#f2c14e"/>'
    return svg(g + '</g>')

def world_serpent(x=CX, y=560, R=250):
    s = f'<circle cx="{x}" cy="{y}" r="{R - 70}" fill="#2a5a7a"/><path fill="#3f7a4c" d="M{x - 90},{y - 80} C{x - 40},{y - 140} {x + 60},{y - 120} {x + 70},{y - 40} C{x + 20},{y + 10} {x - 60},{y - 10} {x - 90},{y - 80} Z"/>'
    s += f'<path fill="#3f7a4c" d="M{x - 40},{y + 60} C{x + 20},{y + 40} {x + 100},{y + 70} {x + 80},{y + 140} C{x + 20},{y + 150} {x - 30},{y + 120} {x - 40},{y + 60} Z"/>'
    s += f'<circle cx="{x}" cy="{y}" r="{R}" fill="none" stroke="#2f5a3a" stroke-width="54"/>'
    s += f'<circle cx="{x}" cy="{y}" r="{R}" fill="none" stroke="#5f9a5a" stroke-width="10" stroke-dasharray="18 22" opacity=".7"/>'
    hx, hy = x + R * math.cos(-1.9), y + R * math.sin(-1.9)
    s += f'<ellipse cx="{hx}" cy="{hy}" rx="56" ry="38" fill="#2f5a3a" transform="rotate(20 {hx} {hy})"/><circle cx="{hx + 18}" cy="{hy - 10}" r="8" fill="#f2e35b"/>'
    return svg(s)

def hammer(x, y, s=1.0, rot=0):
    return svg(f'<g transform="translate({x} {y}) rotate({rot}) scale({s})"><rect x="-14" y="-10" width="28" height="200" rx="8" fill="#6b4a2b"/>'
               f'<rect x="-110" y="-110" width="220" height="110" rx="12" fill="{IRON}"/><rect x="-110" y="-60" width="220" height="12" fill="{IRON_D}"/>'
               f'<circle cx="0" cy="200" r="18" fill="{IRON_D}"/></g>')

def fire(op=1.0):
    r = random.Random(8); s = f'<defs><linearGradient id="fireg" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#ff5a1f"/><stop offset=".6" stop-color="#ff9a3c" stop-opacity=".6"/><stop offset="1" stop-color="#ffcf6a" stop-opacity="0"/></linearGradient></defs><g opacity="{op}">'
    s += '<rect x="-600" y="420" width="3120" height="900" fill="#ff5a1f" opacity=".18"/>'
    for i in range(16):
        x = 600 + i * 46 + r.uniform(-10, 10); h = r.uniform(220, 460)
        s += f'<path fill="url(#fireg)" d="M{x - 40},1000 C{x - 50},{1000 - h * .5} {x - 6},{1000 - h * .7} {x},{1000 - h} C{x + 10},{1000 - h * .6} {x + 50},{1000 - h * .5} {x + 40},1000 Z"/>'
    return svg(s + '</g>')

def tree(x=CX, y=880, s=1.0, col="#3f7a4c"):
    g = f'<g transform="translate({x} {y}) scale({s})"><path fill="#5a3f2a" d="M-40,0 C-30,-120 -20,-220 -14,-300 L14,-300 C20,-220 30,-120 40,0 L80,20 L-80,20 Z"/>'
    for cx, cy, r in ((0, -380, 150), (-130, -320, 110), (130, -320, 110), (-70, -470, 100), (80, -460, 100)):
        g += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{col}"/>'
    return svg(g + '<circle cx="-50" cy="-400" r="40" fill="#fff" opacity=".06"/></g>')

def hills(y=860):
    return svg(f'<path fill="#5e9a5a" d="M-600,{y} C700,{y - 80} 900,{y - 20} 1100,{y - 60} C1300,{y - 100} 1500,{y - 30} 2520,{y - 40} L2520,{y + 600} L-600,{y + 600} Z"/>'
               f'<path fill="#4a8048" d="M-600,{y + 60} C800,{y + 20} 1000,{y + 80} 1300,{y + 40} C1600,{y} 1800,{y + 60} 2520,{y + 50} L2520,{y + 600} L-600,{y + 600} Z"/>')

def sun(x=CX, y=700, r=80):
    return svg(f'<circle cx="{x}" cy="{y}" r="{r * 2.8}" fill="#ffe6a8" opacity=".12"/><circle cx="{x}" cy="{y}" r="{r}" fill="#fff1c8"/>')

def endcard(t0):
    return [tag("History Lab", t0 + .3, y=990), cap("*follow* for more", t0 + .5, y=920, size=40)]

# ================================================================ 1. Horned helmets
def helmets():
    st = Story(); shot = st.shot

    @shot(["Vikings never wore horned helmets."])
    def _(T):
        return (NIGHT, {"zoomFrom": 1, "zoomTo": 1.1},
                bands() + [aurora(), horned_helmet(CX, 660, 1.0),
                 cap("vikings never wore", T.p(0), y=200, size=48),
                 cap("*horned* helmets", T.w(0, "horned"), y=275, size=58),
                 {"type": "redx", "x": CX, "y": 560, "size": 210, "width": 12, "t0": T.w(0, "helmets") + .2}])

    @shot(["The only nearly complete Viking helmet ever found was dug up in Norway, in nineteen forty-three."], chapter=True)
    def _(T):
        return (FORGE, {"zoomFrom": 1.05, "zoomTo": 1.15},
                [spectacle_helmet(CX, 560, 1.3), tag("Norway · 1943", T.w(0, "Norway")),
                 {"type": "namecard", "title": "GJERMUNDBU HELMET", "sub": "10th century · iron", "x": CX, "y": 860, "w": 500, "t0": T.w(0, "only")}])

    @shot(["No horns.", "Just a round iron cap, with a guard for the eyes."])
    def _(T):
        return (FORGE, {"zoomFrom": 1.15, "zoomTo": 1.3, "y": 600},
                [spectacle_helmet(CX, 560, 1.3),
                 cap("*no* horns", T.p(0), y=230, size=64),
                 {"type": "circle", "x": CX, "y": 640, "rx": 200, "ry": 90, "t0": T.w(1, "guard")}])

    @shot(["So where did the horns come from?", "An opera."])
    def _(T):
        return ({"mode": "black"}, {},
                [cap("where did the", T.p(0), y=440, size=48), cap("*horns* come from?", T.w(0, "horns"), y=510, size=48, t1=T.p(1) - .1),
                 {"type": "stamp", "text": "An opera", "x": CX, "y": 640, "size": 72, "t0": T.w(1, "opera")}])

    @shot(["In eighteen seventy-six, a costume designer named Carl Emil Doepler gave them horns, for Wagner's Ring cycle."], chapter=True)
    def _(T):
        return ({"mode": "paper"}, {"zoomFrom": 1, "zoomTo": 1.06},
                [{"type": "doccard", "x": CX, "y": 500, "w": 540, "h": 660, "rotate": -2, "header": "Bayreuth · 1876",
                  "title": "Der Ring des\nNibelungen", "footer": "Costumes: Carl Emil Doepler", "t0": 0},
                 {"type": "stamp", "text": "Horns added", "x": CX, "y": 890, "size": 50, "t0": T.w(0, "horns")}])

    @shot(["The twist?", "Horned helmets were real in Scandinavia.", "They were just about seventeen hundred years too early."])
    def _(T):
        return (NIGHT, {"zoomFrom": 1, "zoomTo": 1.08},
                [stars(), horned_helmet(CX, 600, .9),
                 cap("the *twist*", T.p(0), y=200, size=58, t1=T.p(1) - .1),
                 {"type": "namecard", "title": "VEKSØ HELMETS", "sub": "Denmark · c. 900 BC", "x": CX, "y": 200, "w": 420, "t0": T.w(1, "real")},
                 {"type": "bignumber", "from": 0, "to": 1700, "suffix": " yrs", "x": CX, "y": 900, "size": 100, "color": "#eef4ff", "t0": T.w(2, "seventeen") - .2, "dur": 1.1},
                 cap("*too early*", T.w(2, "early"), y=990, size=44)])

    @shot(["The Vikings got them from a costume department."], tail=2.2)
    def _(T):
        end = T.p(0) + T.d(0)
        return (NIGHT, {"zoomFrom": 1.06, "zoomTo": 1},
                bands() + [aurora(), mountains(),
                 cap("from a *costume*", T.w(0, "costume"), y=300, size=50),
                 cap("department", T.w(0, "department"), y=370, size=50)] + endcard(end))
    return st

# ================================================================ 2. Loki
def loki():
    st = Story(); shot = st.shot

    @shot(["Loki isn't Thor's brother."])
    def _(T):
        return (NIGHT, {"zoomFrom": 1, "zoomTo": 1.1},
                bands() + [aurora(), mountains(),
                 cap("loki isn't", T.p(0), y=230, size=60),
                 {"type": "pill", "text": "Thor's brother", "x": 790, "y": 300, "size": 32, "t0": T.w(0, "Thor")},
                 {"type": "redx", "x": CX, "y": 334, "size": 70, "t0": T.w(0, "brother") + .2}])

    @shot(["That's Marvel.", "In the old Norse poems, Loki is the son of giants, and Odin's blood-brother."], chapter=True)
    def _(T):
        return ({"mode": "paper"}, {"zoomFrom": 1, "zoomTo": 1.06},
                [cap("that's *marvel*", T.p(0), y=300, size=56, t1=T.p(1) - .1),
                 {"type": "doccard", "x": CX, "y": 430, "w": 520, "h": 560, "rotate": 1, "header": "Poetic Edda · c. 1270",
                  "title": "The old\nNorse poems", "footer": "Iceland", "t0": T.p(1)},
                 stack([{"text": "Son of giants", "t0": T.w(1, "giants")}, {"text": "Odin's blood-brother", "t0": T.w(1, "blood"), "tone": "red"}], y=780, w=500)])

    @shot(["But here's the strangest part.", "Odin rode an eight-legged horse called Sleipnir.", "The greatest horse of all."])
    def _(T):
        return (NIGHT, {"zoomFrom": 1, "zoomTo": 1.1},
                [stars(), aurora(.3), sleipnir(CX - 55, 600, 1.05),
                 cap("the *strangest* part", T.w(0, "strangest"), y=200, size=46, t1=T.p(1) - .1),
                 {"type": "namecard", "title": "SLEIPNIR", "sub": "Odin's horse · 8 legs", "x": CX, "y": 200, "w": 400, "t0": T.w(1, "Sleipnir")},
                 cap("the *greatest* horse", T.w(2, "greatest"), y=930, size=44)])

    @shot(["And Sleipnir's mother was Loki."], thuds=[("Loki", .2, 0)])
    def _(T):
        return ({"mode": "black"}, {"zoomFrom": 1, "zoomTo": 1.06},
                [sleipnir(CX - 55, 640, .8, col="#56606b"), cap("sleipnir's *mother*", T.w(0, "mother"), y=260, size=48),
                 {"type": "stamp", "text": "Loki", "x": CX, "y": 400, "size": 90, "t0": T.w(0, "Loki")}])

    @shot(["A giant was building the gods a wall, with a horse that worked too fast.", "So Loki turned himself into a mare, and lured the horse away."], chapter=True)
    def _(T):
        return (DUSK, {"zoomFrom": 1, "zoomTo": 1.08, "y": 640},
                [mountains(900, snow=False), wall(CX, 880, 520, 7),
                 {"type": "pill", "text": "Svadilfari · the giant's horse", "x": 680, "y": 150, "size": 24, "t0": T.w(0, "horse")},
                 cap("too *fast*", T.w(0, "fast"), y=300, size=56, t1=T.p(1) - .1),
                 cap("loki became a *mare*", T.w(1, "mare"), y=300, size=42)])

    @shot(["Months later, Loki gave birth to Sleipnir."])
    def _(T):
        return (NIGHT, {"zoomFrom": 1.1, "zoomTo": 1},
                [stars(seed=7), aurora(), sleipnir(CX - 55, 620, .55),
                 cap("loki gave *birth*", T.w(0, "birth"), y=930, size=48)])

    @shot(["Loki's other children?", "A giant wolf.", "A serpent that circles the world.", "And Hel, queen of the dead."])
    def _(T):
        return ({"mode": "black"}, {},
                [cap("loki's *children*", T.p(0), y=230, size=52),
                 stack([{"text": "Fenrir · giant wolf", "t0": T.p(1)}, {"text": "Jörmungandr · serpent", "t0": T.p(2)},
                        {"text": "Hel · queen of the dead", "t0": T.p(3), "tone": "red"}], y=380, w=560, size=27)])

    @shot(["Norse myth is a lot weirder than the movies."], tail=2.2)
    def _(T):
        end = T.p(0) + T.d(0)
        return (NIGHT, {"zoomFrom": 1.06, "zoomTo": 1},
                bands() + [aurora(), mountains(),
                 cap("a lot *weirder*", T.w(0, "weirder"), y=300, size=56),
                 cap("than the movies", T.w(0, "movies"), y=370, size=44)] + endcard(end))
    return st

# ================================================================ 3. Ragnarok
def ragnarok():
    st = Story(); shot = st.shot

    @shot(["In Norse mythology, the gods lose."])
    def _(T):
        return (DUSK, {"zoomFrom": 1, "zoomTo": 1.12, "y": 700},
                bands() + [mountains(), fire(.55),
                 cap("in norse myth", T.p(0), y=230, size=52),
                 cap("the gods !lose!", T.w(0, "lose"), y=310, size=64)])

    @shot(["It's called Ragnarök.", "The final battle."], chapter=True)
    def _(T):
        return (NIGHT, {"zoomFrom": 1, "zoomTo": 1.08},
                [stars(), aurora(.3), mountains(),
                 {"type": "namecard", "title": "RAGNARÖK", "sub": "The fate of the gods", "x": CX, "y": 300, "w": 420, "t0": T.w(0, "Ragnar")},
                 cap("the *final* battle", T.w(1, "final"), y=460, size=48)])

    @shot(["First comes Fimbulwinter.", "Three winters in a row, with no summer in between."])
    def _(T):
        return ({**NIGHT, "particleCount": 120}, {"zoomFrom": 1, "zoomTo": 1.08},
                [mountains(), svg(f'<rect x="-600" y="830" width="3120" height="400" fill="{SNOW}"/>'),
                 {"type": "namecard", "title": "FIMBULWINTER", "sub": "The great winter", "x": CX, "y": 250, "w": 440, "t0": T.p(0)},
                 {"type": "bignumber", "from": 1, "to": 3, "suffix": " winters", "x": CX, "y": 470, "size": 90, "color": "#eef4ff", "t0": T.w(1, "Three"), "dur": .9},
                 cap("*no* summer", T.w(1, "summer"), y=560, size=46)])

    @shot(["Then the giant wolf Fenrir breaks free,", "and swallows Odin whole."], thuds=[("swallows", .2, 1)])
    def _(T):
        return (FORGE, {"zoomFrom": 1, "zoomTo": 1.15, "x": 960},
                [wolf(930, 580, 1.2),
                 {"type": "namecard", "title": "FENRIR", "sub": "Son of Loki", "x": CX, "y": 220, "w": 340, "t0": T.w(0, "Fenrir")},
                 cap("!odin! is swallowed", T.w(1, "Odin"), y=930, size=44)])

    @shot(["Thor kills the world serpent,", "walks nine steps,", "and drops dead from its venom."], thuds=[("kills", .2, 0)])
    def _(T):
        return (NIGHT, {"zoomFrom": 1, "zoomTo": 1.08},
                [world_serpent(CX, 520), hammer(1080, 200, .45, 30, ) | {"t0": T.w(0, "kills") - .2},
                 {"type": "bignumber", "from": 1, "to": 9, "suffix": " steps", "x": CX, "y": 900, "size": 80, "color": "#eef4ff", "t0": T.w(1, "nine") - .2, "dur": 1.0, "t1": T.p(2)},
                 cap("thor is !dead!", T.w(2, "dead"), y=900, size=56)])

    @shot(["Loki and Heimdall kill each other.", "And the fire giant Surtr sets the whole world ablaze."])
    def _(T):
        return (DUSK, {"zoomFrom": 1, "zoomTo": 1.12, "y": 760},
                [mountains(), fire() | {"t0": T.w(1, "fire") - .2},
                 stack([{"text": "Loki", "t0": T.w(0, "Loki")}, {"text": "Heimdall", "t0": T.w(0, "Heimdall")}], y=180, w=320, size=28) | {"t1": T.p(1)},
                 {"type": "namecard", "title": "SURTR", "sub": "The fire giant", "x": CX, "y": 250, "w": 340, "t0": T.w(1, "Surtr")},
                 cap("the world !burns!", T.w(1, "ablaze"), y=420, size=52)])

    @shot(["But it doesn't end there.", "The earth rises again from the sea, green and new."], chapter=True)
    def _(T):
        return (DAWN, {"zoomFrom": 1.08, "zoomTo": 1, "y": 700},
                [sun(CX, 760, 70), hills(860),
                 cap("it doesn't *end*", T.w(0, "end"), y=250, size=52, t1=T.p(1) - .1),
                 cap("the earth *rises*", T.w(1, "rises"), y=250, size=52)])

    @shot(["Two humans survive, hidden in the woods.", "Líf and Lífthrasir."])
    def _(T):
        return (DAWN, {"zoomFrom": 1, "zoomTo": 1.1, "y": 620},
                [sun(1150, 520, 50), hills(880), tree(CX, 900, 1.1),
                 svg('<g fill="#2a1d15"><circle cx="905" cy="790" r="16"/><rect x="893" y="806" width="24" height="64" rx="10"/><circle cx="1015" cy="794" r="15"/><rect x="1004" y="809" width="22" height="61" rx="10"/></g>', t0=T.w(0, "humans")),
                 cap("two humans *survive*", T.w(0, "survive"), y=170, size=42),
                 {"type": "pill", "text": "Líf & Lífthrasir", "x": 780, "y": 960, "size": 28, "t0": T.p(1)}])

    @shot(["The end of the world is a new beginning."], tail=2.2)
    def _(T):
        end = T.p(0) + T.d(0)
        return (DAWN, {"zoomFrom": 1, "zoomTo": 1.06},
                bands() + [sun(CX, 700, 80), hills(860),
                 cap("the end is a", T.w(0, "end"), y=280, size=48),
                 cap("*new beginning*", T.w(0, "beginning"), y=350, size=52)] + endcard(end))
    return st

if __name__ == "__main__":
    tts, root = sys.argv[1], sys.argv[2]
    which = sys.argv[3:] or ["helmets", "loki", "ragnarok"]
    B = {"helmets": helmets, "loki": loki, "ragnarok": ragnarok}
    for name in which:
        print("==", name)
        build(B[name](), tts, f"{root}/{name}", voice=VOICE, lang=LANG, speed=SPEED, width=1080, height=1920,
              gaps=(.32, .55, .22), lead=.3, tokens=TOKENS_NO, say=SAY)
