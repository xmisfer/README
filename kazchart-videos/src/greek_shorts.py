"""History Lab: three Greek myth Shorts (1080x1920). Visible world column x 656-1264, centre 960.
Usage: python3 greek_shorts.py <tts_dir> <out_root> [medusa|pandora|achilles ...]"""
import random, sys
from kzlib import *
from egypt_shorts import svg, cap, tag, stack, CX, RED, VOICE, LANG, SPEED

ORANGE, MARBLE, MARBLE_D, BRONZE, CLAY = "#ef8a3e", "#e9e4d8", "#b9b2a2", "#b58a3c", "#b85c2c"
NIGHT = {"top": "#0b1324", "bottom": "#23304a", "rays": False, "particleCount": 20}
AEGEAN = {"top": "#1f5f8b", "bottom": "#9cc9df", "rays": True, "rayOpacity": .06, "particleCount": 12}
DARK = {"top": "#0c0a0e", "bottom": "#1c1620", "rays": False, "particleCount": 25, "spotlight": {"x": 960, "w": 360}}
STYX = {"top": "#05080b", "bottom": "#0e1c22", "rays": False, "particleCount": 30}
TOKENS_GR = {"hl": ORANGE, "creature": {**TOKENS["creature"], "blob": ["none", "none", "none"]}}  # props draw their own art

# ---------------------------------------------------------------- Greek art
def meander(y, col=ORANGE, x0=600, x1=1320, u=36, op=.8):
    d = ""
    for x in range(x0, x1, u):
        d += f"M{x},{y + u * .8} L{x},{y} L{x + u * .8},{y} L{x + u * .8},{y + u * .6} L{x + u * .3},{y + u * .6} L{x + u * .3},{y + u * .3} L{x + u * .55},{y + u * .3} "
    return svg(f'<line x1="{x0}" y1="{y - 8}" x2="{x1}" y2="{y - 8}" stroke="{col}" stroke-width="3" opacity="{op}"/>'
               f'<path d="{d}" fill="none" stroke="{col}" stroke-width="4" opacity="{op}"/>'
               f'<line x1="{x0}" y1="{y + u}" x2="{x1}" y2="{y + u}" stroke="{col}" stroke-width="3" opacity="{op}"/>')

def bands(): return [meander(24), meander(1022)]

def temple(x=CX, base=900, w=540, op=1):
    h, n = w * .62, 6
    s = f'<g opacity="{op}">'
    for i in range(3):
        s += f'<rect x="{x - w/2 - 30 + i * 10}" y="{base - 18 * (i + 1)}" width="{w + 60 - i * 20}" height="18" fill="{MARBLE if i % 2 else MARBLE_D}"/>'
    top = base - 54 - h
    for i in range(n):
        cx = x - w/2 + 30 + i * (w - 60) / (n - 1)
        s += f'<rect x="{cx - 20}" y="{top + 60}" width="40" height="{h - 60}" fill="{MARBLE}"/>'
        s += ''.join(f'<line x1="{cx + k}" y1="{top + 66}" x2="{cx + k}" y2="{base - 58}" stroke="{MARBLE_D}" stroke-width="2"/>' for k in (-10, 0, 10))
        s += f'<rect x="{cx - 28}" y="{top + 50}" width="56" height="14" fill="{MARBLE_D}"/>'
    s += f'<rect x="{x - w/2 - 10}" y="{top + 10}" width="{w + 20}" height="42" fill="{MARBLE}"/><rect x="{x - w/2 - 10}" y="{top + 30}" width="{w + 20}" height="6" fill="{MARBLE_D}"/>'
    s += f'<polygon points="{x - w/2 - 20},{top + 12} {x},{top - 90} {x + w/2 + 20},{top + 12}" fill="{MARBLE}"/><polygon points="{x - w/2 + 30},{top + 2} {x},{top - 66} {x + w/2 - 30},{top + 2}" fill="{MARBLE_D}" opacity=".5"/>'
    return svg(s + '</g>')

def face(x=CX, y=520, s=1.0, snakes=False, glow=False):
    skin = "#8fa37e" if snakes else "#e2c2a0"
    g = f'<g transform="translate({x} {y}) scale({s})">'
    if snakes:
        r = random.Random(5)
        for i in range(11):
            a = -160 + i * 32; sx, sy = a * .55, -120 + abs(a) * .3
            ex, ey = sx * 1.9 + r.uniform(-20, 20), sy - 120 - r.uniform(0, 50)
            g += f'<path d="M{sx * .5},{sy + 40} C{sx},{sy - 40} {ex - 40},{ey + 60} {ex},{ey}" stroke="#4f6b3a" stroke-width="22" fill="none" stroke-linecap="round"/>'
            g += f'<ellipse cx="{ex}" cy="{ey}" rx="20" ry="13" fill="#4f6b3a"/><circle cx="{ex + 6}" cy="{ey - 3}" r="3.5" fill="#f2e35b"/>'
            g += f'<path d="M{ex + 18},{ey} l14,-4 M{ex + 18},{ey} l14,4" stroke="{RED}" stroke-width="2"/>'
    else:
        g += '<path fill="#4a2e1d" d="M-150,-40 C-170,-200 170,-200 150,-40 C170,120 160,240 120,300 L-120,300 C-160,240 -170,120 -150,-40 Z"/>'
    g += f'<ellipse cx="0" cy="0" rx="110" ry="140" fill="{skin}"/><rect x="-36" y="120" width="72" height="90" fill="{skin}"/>'
    if not snakes: g += '<path fill="#4a2e1d" d="M-112,-30 C-100,-150 100,-150 112,-30 C70,-90 -70,-90 -112,-30 Z"/>'
    ec = "#f2e35b" if glow else "#2a1d15"
    for ex in (-42, 42):
        if glow: g += f'<circle cx="{ex}" cy="-10" r="26" fill="#f2e35b" opacity=".25"/>'
        g += f'<ellipse cx="{ex}" cy="-10" rx="16" ry="9" fill="{ec}"/>'
    g += f'<path d="M-24,70 Q0,{60 if snakes else 84} 24,70" stroke="#5a2d22" stroke-width="5" fill="none"/>'
    return g + '</g>'

def statue(x, y, s=1.0, pose=0):
    c, d = "#8a8f94", "#6c7176"
    arm = ("M-14,-120 L-60,-60", "M14,-120 L60,-170")[pose % 2]
    return (f'<g transform="translate({x} {y}) scale({s})" fill="{c}"><circle cx="0" cy="-170" r="24"/><path d="M-26,-140 L26,-140 L22,-20 L-22,-20 Z"/>'
            f'<path stroke="{c}" stroke-width="16" stroke-linecap="round" fill="none" d="M-8,-22 L-20,80 M8,-22 L22,80 M-14,-120 L-50,-80 {arm}"/>'
            f'<rect x="-50" y="80" width="100" height="22" fill="{d}"/></g>')

def wing(x=CX, y=520, s=1.0):
    g = f'<g transform="translate({x - 230 * s} {y}) scale({s})">'
    g += ('<path fill="#f4f1ea" d="M0,0 C80,-140 270,-220 470,-190 C430,-150 390,-128 340,-116 C392,-96 412,-72 412,-48 '
          'C360,-46 310,-50 268,-56 C300,-34 310,-10 300,14 C250,4 208,-6 168,-16 C178,6 176,28 156,48 C112,28 62,14 0,0 Z"/>')
    g += '<path fill="#dcd6c8" d="M30,-14 C110,-120 260,-170 410,-170 C300,-140 200,-100 120,-40 C90,-30 60,-20 30,-14 Z"/>'
    return g + '</g>'

def shield(x=CX, y=540, r=230):
    s = f'<circle cx="{x}" cy="{y}" r="{r}" fill="{BRONZE}"/><circle cx="{x}" cy="{y}" r="{r - 22}" fill="#c99c4a"/><circle cx="{x}" cy="{y}" r="{r - 22}" fill="none" stroke="#7a5a24" stroke-width="4"/>'
    return svg(s + face(x, y + 10, .55, snakes=True, glow=True))

def jar(x=CX, y=600, s=1.0):
    g = f'<g transform="translate({x} {y}) scale({s})">'
    g += f'<path fill="{CLAY}" d="M-150,-200 C-250,-110 -250,170 -120,270 L120,270 C250,170 250,-110 150,-200 Z"/>'
    g += f'<rect x="-120" y="-250" width="240" height="56" fill="{CLAY}"/><rect x="-140" y="-262" width="280" height="22" rx="8" fill="#8e4320"/>'
    g += '<rect x="-200" y="-90" width="400" height="16" fill="#1a1210" opacity=".85"/><rect x="-196" y="150" width="392" height="14" fill="#1a1210" opacity=".85"/>'
    g += '<path fill="#000" opacity=".18" d="M60,-200 C200,-110 210,150 100,270 L120,270 C250,170 250,-110 150,-200 Z"/>'
    return g + '</g>'

def lid():
    return '<rect x="-150" y="-26" width="300" height="40" rx="10" fill="#8e4320"/><rect x="-26" y="-56" width="52" height="34" rx="10" fill="#6e3318"/>'

def wisp():
    return ('<path fill="#1a1420" opacity=".92" d="M-60,40 C-90,-20 -40,-80 0,-120 C40,-80 90,-20 60,40 C40,70 20,100 0,150 C-20,100 -40,70 -60,40 Z"/>'
            '<circle cx="-20" cy="-20" r="9" fill="#ff4a3a"/><circle cx="20" cy="-20" r="9" fill="#ff4a3a"/>')

def helmet(x=CX, y=520, s=1.0):
    return svg(f'<g transform="translate({x} {y}) scale({s})">'
               f'<path d="M-130,-190 C-90,-300 110,-300 150,-180" stroke="{RED}" stroke-width="36" fill="none" stroke-linecap="round"/>'
               f'<path fill="{BRONZE}" d="M-150,-90 C-150,-230 150,-230 160,-80 L160,40 L120,140 L60,140 L64,40 L36,10 L36,-30 L6,-30 L6,50 L-16,140 L-150,140 Z"/>'
               f'<path fill="#000" opacity=".2" d="M60,-200 C130,-170 160,-130 160,-80 L160,40 L120,140 L90,140 C120,60 130,-60 60,-200 Z"/>'
               f'<path d="M-150,40 L-20,40" stroke="#7a5a24" stroke-width="5"/></g>')

FOOT = "M820,470 L940,470 L962,600 L1062,688 L1210,738 C1242,758 1232,792 1180,792 L880,792 C818,792 768,770 778,720 L800,600 Z"
def foot(glow=False):
    s = f'<path fill="#d9a77c" d="{FOOT}"/>'
    if glow: s += f'<path fill="none" stroke="#7fe3f0" stroke-width="10" opacity=".7" d="M820,470 L800,600 L790,690 M940,470 L962,600 L1062,688 L1210,738 C1242,758 1232,792 1180,792 L880,792"/>'
    return svg(s)

def arrow():
    return ('<line x1="-340" y1="0" x2="120" y2="0" stroke="#e9e1cf" stroke-width="8"/><polygon points="160,0 112,-18 112,18" fill="#c9ccd0"/>'
            '<path fill="' + RED + '" d="M-340,0 L-300,-26 L-270,-26 L-310,0 L-270,26 L-300,26 Z"/>')

def endcard(t0):
    return [tag("History Lab", t0 + .3, y=990), cap("*follow* for more", t0 + .5, y=920, size=40)]

# ================================================================ 1. Medusa
def medusa():
    st = Story(); shot = st.shot

    @shot(["Medusa wasn't born a monster."])
    def _(T):
        return (DARK, {"zoomFrom": 1, "zoomTo": 1.12, "y": 560},
                bands() + [svg(face(CX, 700, 1.0, snakes=True, glow=True)),
                 cap("medusa wasn't", T.w(0, "Medusa"), y=200, size=54),
                 cap("born a *monster*", T.w(0, "monster"), y=275, size=54)])

    @shot(["In the Roman poet Ovid's version, she was a beautiful young woman, famous for her hair."], chapter=True)
    def _(T):
        return (AEGEAN, {"zoomFrom": 1.05, "zoomTo": 1.15, "y": 520},
                [svg(face(CX, 560, 1.15)), tag("Ovid · 8 AD"),
                 cap("a *beautiful* woman", T.w(0, "beautiful"), y=950, size=44)])

    @shot(["Then the sea god Poseidon attacked her, inside Athena's temple."])
    def _(T):
        return (NIGHT, {"zoomFrom": 1, "zoomTo": 1.12, "y": 700},
                [temple(), {"type": "pill", "text": "Poseidon", "x": 700, "y": 170, "size": 28, "tone": "red", "t0": T.w(0, "Poseidon")},
                 cap("in *athena's* temple", T.w(0, "Athena"), y=990, size=42)])

    @shot(["Athena was furious.", "But she didn't punish Poseidon."])
    def _(T):
        return ({"mode": "black"}, {},
                [cap("athena was *furious*", T.w(0, "furious"), y=420, size=44),
                 {"type": "pill", "text": "Punish Poseidon", "x": 760, "y": 560, "size": 28, "t0": T.p(1)},
                 {"type": "redx", "x": 960, "y": 586, "size": 60, "t0": T.w(1, "Poseidon")}])

    @shot(["She punished Medusa.", "Her beautiful hair became snakes."], thuds=[("snakes", .1, 1)])
    def _(T):
        sw = T.w(1, "snakes")
        return (DARK, {"zoomFrom": 1, "zoomTo": 1.1, "y": 560},
                [svg(face(CX, 600, 1.1), t1=sw), svg(face(CX, 600, 1.1, snakes=True), t0=sw),
                 cap("she punished *medusa*", T.w(0, "Medusa"), y=200, size=38, t1=T.p(1) - .1),
                 cap("!snakes!", sw, y=200, size=72)])

    @shot(["Anyone who looked at her turned to stone."])
    def _(T):
        return (NIGHT, {"zoomFrom": 1, "zoomTo": 1.08, "y": 700},
                [svg(statue(760, 760, 1.2) + statue(960, 800, 1.3, 1) + statue(1160, 760, 1.2)),
                 svg(face(CX, 300, .55, snakes=True, glow=True)),
                 cap("turned to *stone*", T.w(0, "stone"), y=990, size=46)])

    @shot(["When the hero Perseus cut off her head, the winged horse Pegasus sprang from her neck."], chapter=True)
    def _(T):
        return (AEGEAN, {"zoomFrom": 1, "zoomTo": 1.12},
                [svg(face(CX, 600, .9, snakes=True, glow=True), t1=T.w(0, "Pegasus") - .3), cap("cut off her *head*", T.w(0, "cut"), y=290, size=46, t1=T.w(0, "Pegasus") - .3),
                 svg(wing(CX, 600, 1.0), t0=T.w(0, "Pegasus") - .3),
                 {"type": "pill", "text": "Perseus", "x": 700, "y": 170, "size": 28, "t0": T.w(0, "Perseus")},
                 {"type": "namecard", "title": "PEGASUS", "sub": "Born from Medusa", "x": CX, "y": 900, "w": 380, "t0": T.w(0, "Pegasus")},
                 cap("from her *neck*", T.w(0, "neck"), y=290, size=48)])

    @shot(["And Athena wore Medusa's face on her armour, forever."])
    def _(T):
        return (NIGHT, {"zoomFrom": 1, "zoomTo": 1.1},
                bands() + [shield(), cap("on athena's *armour*", T.w(0, "armour"), y=900, size=40)])

    @shot(["The monster was the victim."], tail=2.2)
    def _(T):
        end = T.p(0) + T.d(0)
        return (DARK, {"zoomFrom": 1.08, "zoomTo": 1},
                bands() + [svg(face(CX, 560, 1.0)),
                 cap("the monster was", T.p(0), y=170, size=48),
                 cap("the *victim*", T.w(0, "victim"), y=245, size=60)] + endcard(end))
    return st

# ================================================================ 2. Pandora
def pandora():
    st = Story(); shot = st.shot

    @shot(["Pandora never opened a box."])
    def _(T):
        return (DARK, {"zoomFrom": 1, "zoomTo": 1.1},
                bands() + [svg(jar(CX, 640, .9)),
                 cap("pandora never", T.p(0), y=200, size=54),
                 cap("opened a *box*", T.w(0, "box"), y=275, size=54),
                 {"type": "redx", "x": 1172, "y": 258, "size": 44, "t0": T.w(0, "box") + .4}])

    @shot(["In the original Greek poem, by Hesiod, it was a jar.", "A pithos.", "The kind of jar the philosopher Diogenes was said to live in."], chapter=True)
    def _(T):
        return (AEGEAN, {"zoomFrom": 1, "zoomTo": 1.08},
                [svg(jar(CX, 600, .95)), tag("Hesiod · c. 700 BC"),
                 cap("it was a *jar*", T.w(0, "jar"), y=990, size=50, t1=T.p(1) - .1),
                 {"type": "namecard", "title": "PITHOS", "sub": "Greek storage jar", "x": CX, "y": 990, "w": 380, "t0": T.p(1)},
                 {"type": "pill", "text": "Diogenes lived in one", "x": 710, "y": 160, "size": 26, "t0": T.w(2, "Diogenes")}])

    @shot(["The box came from a translation mistake, over two thousand years later."])
    def _(T):
        return ({"mode": "paper"}, {"zoomFrom": 1, "zoomTo": 1.06},
                [{"type": "doccard", "x": CX, "y": 500, "w": 540, "h": 660, "rotate": -2, "header": "Erasmus · 1508",
                  "title": "Pithos (jar)\nbecame\npyxis (box)", "footer": "A mistranslation", "t0": 0},
                 {"type": "stamp", "text": "Translation error", "x": CX, "y": 900, "size": 44, "t0": T.w(0, "mistake")}])

    @shot(["Pandora was the first woman, built by the gods as a punishment, after Prometheus stole fire."], chapter=True)
    def _(T):
        return (NIGHT, {"zoomFrom": 1, "zoomTo": 1.08},
                [svg(statue(CX, 520, 1.4)), svg(f'<circle cx="1150" cy="220" r="40" fill="{ORANGE}" opacity=".9"/><circle cx="1150" cy="220" r="90" fill="{ORANGE}" opacity=".15"/>', t0=T.w(0, "fire")),
                 stack([{"text": "First woman", "t0": T.w(0, "first")}, {"text": "Built by the gods", "t0": T.w(0, "built")},
                        {"text": "A punishment", "t0": T.w(0, "punishment"), "tone": "red"}], y=720, w=460)])

    @shot(["When she lifted the lid, every evil escaped.", "Sickness. Hard work. Sorrow."])
    def _(T):
        t = T.w(0, "lifted"); r = random.Random(3)
        wisps = [prop(wisp(), CX + r.uniform(-40, 40), 250, .55, bob=4, phase=i, t0=t + .25 + i * .22,
                      swim={"vx": r.uniform(-90, 90), "vy": -r.uniform(70, 120)}) for i in range(7)]
        return (DARK, {"zoomFrom": 1, "zoomTo": 1.05},
                [svg(jar(CX, 560, .9)), prop(lid(), CX, 330, .9, bob=0, moveTo={"x": 1150, "y": 200, "dur": .6, "t0": t})] + wisps +
                [cap("every evil *escaped*", T.w(0, "escaped"), y=990, size=40, t1=T.p(1) - .1),
                 stack([{"text": "Sickness", "t0": T.w(1, "Sickness")}, {"text": "Hard work", "t0": T.w(1, "Hard")},
                        {"text": "Sorrow", "t0": T.w(1, "Sorrow"), "tone": "red"}], y=840, w=380, size=28, gap=70)])

    @shot(["She slammed it shut.", "Only one thing was left inside.", "Hope."], thuds=[("slammed", .3, 0)])
    def _(T):
        hope = svg('<circle cx="960" cy="340" r="120" fill="#ffe9a8" opacity=".18"/><circle cx="960" cy="340" r="60" fill="#ffe9a8" opacity=".35"/><circle cx="960" cy="340" r="24" fill="#fff6d8"/>', t0=T.p(2) - .2)
        return (DARK, {"zoomFrom": 1, "zoomTo": 1.12, "y": 500},
                [svg(jar(CX, 560, .9)), hope,
                 prop(lid(), 1150, 200, .9, bob=0, moveTo={"x": CX, "y": 330, "dur": .4, "t0": T.w(0, "slammed")}),
                 cap("only one thing", T.w(1, "one"), y=200, size=48, t1=T.p(2) - .1),
                 cap("*hope*", T.p(2), y=200, size=90)])

    @shot(["Scholars still argue whether keeping hope locked away was a blessing, or a curse."], tail=2.2)
    def _(T):
        end = T.p(0) + T.d(0)
        return (NIGHT, {"zoomFrom": 1.06, "zoomTo": 1},
                bands() + [svg(jar(CX, 560, .7)),
                 cap("a blessing", T.w(0, "blessing"), y=170, size=52),
                 cap("or a !curse!?", T.w(0, "curse"), y=245, size=52)] + endcard(end))
    return st

# ================================================================ 3. Achilles
def achilles():
    st = Story(); shot = st.shot

    @shot(["Achilles' heel isn't in the Iliad."])
    def _(T):
        return (DARK, {"zoomFrom": 1, "zoomTo": 1.1},
                bands() + [helmet(CX, 720, 1.25),
                 cap("achilles' heel", T.p(0), y=200, size=54),
                 cap("isn't in the *iliad*", T.w(0, "Iliad"), y=275, size=44)])

    @shot(["Homer's epic never says Achilles was invincible."], chapter=True)
    def _(T):
        return ({"mode": "paper"}, {"zoomFrom": 1, "zoomTo": 1.06},
                [{"type": "doccard", "x": CX, "y": 500, "w": 520, "h": 640, "rotate": -1, "header": "Homer · c. 750 BC",
                  "title": "The Iliad", "footer": "24 books", "t0": 0},
                 {"type": "stamp", "text": "Not invincible", "x": CX, "y": 880, "size": 46, "t0": T.w(0, "invincible")}])

    @shot(["In fact, he gets wounded.", "A spear grazes his arm and draws blood."])
    def _(T):
        return (DARK, {"zoomFrom": 1, "zoomTo": 1.12},
                [helmet(CX, 520, 1.2),
                 svg(f'<path d="M760,760 L1160,680" stroke="{RED}" stroke-width="12" stroke-linecap="round"/>', t0=T.w(1, "grazes")),
                 cap("he gets *wounded*", T.w(0, "wounded"), y=200, size=48),
                 {"type": "pill", "text": "Iliad · book 21", "x": 760, "y": 860, "size": 26, "t0": T.w(1, "blood")}])

    @shot(["And his death? It isn't in the Iliad at all.", "The poem ends before it."])
    def _(T):
        return ({"mode": "black"}, {},
                [cap("his *death*?", T.w(0, "death"), y=420, size=60),
                 cap("not in the poem", T.w(0, "isn't"), y=500, size=46),
                 {"type": "pill", "text": "Ends with Hector's funeral", "x": 690, "y": 600, "size": 24, "t0": T.p(1)}])

    @shot(["The heel story shows up about eight hundred years later, in a Roman poem by Statius."], chapter=True)
    def _(T):
        return ({"mode": "paper"}, {"zoomFrom": 1, "zoomTo": 1.06},
                [{"type": "doccard", "x": CX, "y": 500, "w": 520, "h": 640, "rotate": 2, "header": "Statius · c. 95 AD",
                  "title": "Achilleid", "footer": "A Roman poem", "t0": T.w(0, "Roman") - .3},
                 cap("*~800 years* later", T.w(0, "eight"), y=500, size=46, t1=T.w(0, "Roman") - .4),
                 {"type": "stamp", "text": "First heel", "x": CX, "y": 880, "size": 50, "color": ORANGE, "t0": T.w(0, "Statius")}])

    @shot(["His mother Thetis dipped him in the river Styx, holding him by the heel."])
    def _(T):
        return (STYX, {"zoomFrom": 1, "zoomTo": 1.08},
                [svg('<rect x="-600" y="640" width="3120" height="900" fill="#103a44" opacity=".65"/><path d="M-600,640 Q-500,628 -400,640 T-200,640 T0,640 T200,640 T400,640 T600,640 T800,640 T1000,640 T1200,640 T1400,640 T1600,640 T1800,640 T2000,640 T2200,640 T2400,640" stroke="#7fe3f0" stroke-width="4" fill="none" opacity=".5"/>'),
                 foot(glow=False), foot(glow=True) | {"t0": T.w(0, "dipped")},
                 tag("River Styx"),
                 {"type": "circle", "x": 790, "y": 740, "rx": 70, "ry": 70, "color": RED, "t0": T.w(0, "heel")},
                 cap("held by the *heel*", T.w(0, "heel"), y=990, size=46)])

    @shot(["That one dry spot was the only place he could be hurt."])
    def _(T):
        return (STYX, {"zoomFrom": 1.1, "zoomTo": 1.3, "x": 790, "y": 740},
                [foot(glow=True), {"type": "circle", "x": 790, "y": 740, "rx": 80, "ry": 80, "color": RED, "t0": 0},
                 cap("the only *weak spot*", T.w(0, "only"), y=990, size=40)])

    @shot(["Paris's arrow found it."], thuds=[("found", .2, 0)])
    def _(T):
        hit = T.w(0, "found")
        return (STYX, {"zoomFrom": 1.05, "zoomTo": 1.15, "x": 860, "y": 700},
                [foot(glow=True), prop(arrow(), 300, 640, .9, bob=0, rotate=12, moveTo={"x": 660, "y": 712, "dur": .45, "t0": hit - .25}),
                 {"type": "stamp", "text": "Paris", "x": CX, "y": 300, "size": 60, "t0": hit + .2},
                 cap("the *arrow*", T.w(0, "arrow"), y=990, size=50)])

    @shot(["And in sixteen ninety-three, a Flemish anatomist named the tendon after him.", "The Achilles tendon."], chapter=True, tail=2.2)
    def _(T):
        end = T.p(1) + T.d(1)
        return (NIGHT, {"zoomFrom": 1, "zoomTo": 1.06},
                [foot(), svg(f'<path d="M812,480 L798,600 L790,720" stroke="{ORANGE}" stroke-width="14" stroke-linecap="round" fill="none"/>', t0=T.w(0, "tendon")),
                 tag("1693"),
                 {"type": "namecard", "title": "ACHILLES TENDON", "sub": "Named by Philip Verheyen", "x": CX, "y": 250, "w": 480, "t0": T.p(1)}] + endcard(end))
    return st

if __name__ == "__main__":
    tts, root = sys.argv[1], sys.argv[2]
    which = sys.argv[3:] or ["medusa", "pandora", "achilles"]
    B = {"medusa": medusa, "pandora": pandora, "achilles": achilles}
    for name in which:
        print("==", name)
        build(B[name](), tts, f"{root}/{name}", voice=VOICE, lang=LANG, speed=SPEED, width=1080, height=1920,
              gaps=(.32, .55, .22), lead=.3, tokens=TOKENS_GR)
