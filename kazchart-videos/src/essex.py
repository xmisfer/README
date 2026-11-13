"""Build 'The Whale That Sank a Ship' (Essex, 1820) for KazChart, abyss preset.
Usage: python3 -I build.py <tts_dir> <out_dir>
Writes vo.wav, timeline.json, scene.json, script.txt into out_dir.
"""
import json, os, sys
import numpy as np
import soundfile as sf

TTS, OUT = sys.argv[1], sys.argv[2]
VOICE, SPEED, LANG = "bm_george", 0.94, "en-gb"
SR = 24000

# ---------------------------------------------------------------- art helpers
def ship_markup(sil=False):
    hull, rail, wood, sail, rope = ("#05090d",) * 5 if sil else ("#3b2a1f", "#e8e2d2", "#2a1d15", "#dcd3bd", "#2a1d15")
    s = f'<path fill="{hull}" d="M-222,-52 L232,-58 L206,0 C186,50 110,64 0,64 C-120,64 -186,54 -206,16 Z"/>'
    if not sil:
        s += f'<rect x="-205" y="-44" width="420" height="9" fill="{rail}" opacity=".85"/>'
        s += ''.join(f'<rect x="{x}" y="-44" width="14" height="9" fill="{hull}"/>' for x in range(-180, 200, 46))
    s += f'<path fill="none" stroke="{rope}" stroke-width="6" d="M226,-56 L330,-118"/>'
    for mx, h in ((-118, 300), (18, 345), (142, 285)):
        s += f'<rect x="{mx - 4}" y="{-52 - h}" width="8" height="{h}" fill="{wood}"/>'
        for k, (w, y0, y1) in enumerate(((172, -95, -170), (140, -180, -245), (100, -255, -305))):
            if -y1 > h + 40:
                continue
            w2 = w * 0.88
            s += f'<path fill="{sail}" opacity="{1 if sil else .96}" d="M{mx - w/2},{y0} L{mx + w/2},{y0} L{mx + w2/2},{y1} L{mx - w2/2},{y1} Z"/>'
        s += f'<path fill="none" stroke="{rope}" stroke-width="2" opacity=".7" d="M{mx},{-52 - h} L{mx - 120},-52 M{mx},{-52 - h} L{mx + 120},-52"/>'
    s += f'<path fill="{sail}" opacity="{1 if sil else .9}" d="M150,-320 L320,-116 L170,-90 Z"/>'
    return s

def boat_markup(sil=True):
    c = "#05090d" if sil else "#5a4232"
    s = f'<path fill="{c}" d="M-196,-54 L196,-54 L176,8 C120,58 -120,58 -176,8 Z"/>'
    for i, x in enumerate(range(-120, 140, 60)):
        s += f'<circle cx="{x}" cy="-78" r="15" fill="{c}"/><rect x="{x - 12}" y="-70" width="24" height="18" fill="{c}"/>'
        s += f'<path stroke="{c}" stroke-width="7" stroke-linecap="round" d="M{x},-62 L{x - 70},60"/>'
    return s

WL = 430  # waterline for cross-section shots

def sea_back():
    return {"type": "svg", "markup":
        '<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#18303f"/>'
        '<stop offset="1" stop-color="#6d8e9c"/></linearGradient></defs>'
        f'<rect x="-600" y="-600" width="3120" height="{WL + 600}" fill="url(#sky)"/>'
        '<circle cx="1480" cy="250" r="70" fill="#e9f3f2" opacity=".55"/>'
        '<circle cx="1480" cy="250" r="160" fill="#e9f3f2" opacity=".08"/>'}

def sea_front():
    return {"type": "svg", "markup":
        f'<rect x="-600" y="{WL}" width="3120" height="1400" fill="#17465d" opacity=".42"/>'
        f'<path fill="none" stroke="#cfe9f2" stroke-width="4" opacity=".55" d="M-600,{WL} '
        + ' '.join(f'Q{x + 60},{WL - 8} {x + 120},{WL}' for x in range(-600, 2520, 120)) + '"/>'}

SURF = 64
def ship(x, y, scale=1.0, sil=False, **kw):
    if sil and y < 40: y = SURF + 52 * scale - 6
    return {"type": "creature", "kind": "blob", "x": x, "y": y, "scale": scale, "bob": kw.pop("bob", 3),
            "mode": "silhouette" if sil else None, "inner": ship_markup(sil), **kw}

def boat(x, y, scale=.4, **kw):
    if y < 60: y = SURF + 54 * scale - 4
    return {"type": "creature", "kind": "blob", "mode": "silhouette", "x": x, "y": y, "scale": scale,
            "inner": boat_markup(), **kw}

def whale(x, y, scale=1.0, sil=False, **kw):
    e = {"type": "creature", "kind": "whale", "x": x, "y": y, "scale": scale, **kw}
    if sil: e["mode"] = "silhouette"
    return e

# ---------------------------------------------------------------- the script
# Each shot: narration lines + a builder that returns (bg, camera, elements, extras)
S = []
def shot(lines, chapter=False, **opt):
    def deco(fn):
        S.append(dict(lines=lines, chapter=chapter, fn=fn, **opt)); return fn
    return deco

@shot(["In eighteen twenty, a whale did something no one believed was possible."])
def _(T):
    return ({"depth": .85, "sun": {"x": 980, "y": -120, "r": 760}, "surface": True},
            {"zoomFrom": 1, "zoomTo": 1.12},
            [whale(260, 640, 1.6, sil=True, swim={"vx": 46}),
             {"type": "tag", "text": "1820", "t0": .3},
             {"type": "caption", "text": "a whale did the *impossible*", "t0": T.w(0, "something")}])

@shot(["It hunted a ship.", "And it won."])
def _(T):
    return ({"depth": .75, "sun": {"x": 1250, "y": -80, "r": 620}, "surface": True},
            {"zoomFrom": 1.05, "zoomTo": 1.15},
            [ship(1240, 4, 1.35, sil=True, swim={"vx": 8}),
             whale(380, 760, 1.2, sil=True, rotate=-20, moveTo={"x": 900, "y": 420, "dur": 3.2, "t0": 0}),
             {"type": "caption", "text": "it *hunted* a ship", "t0": T.w(0, "hunted"), "t1": T.p(1) - .1},
             {"type": "stamp", "text": "And it won", "x": 1420, "y": 640, "t0": T.w(1, "won")}])

@shot(["November twentieth, eighteen twenty.", "The middle of the Pacific Ocean."], chapter=True)
def _(T):
    return ({"depth": .35}, {"zoomFrom": 1, "zoomTo": 1.08, "x": 900, "y": 420},
            [sea_back(), ship(780, WL - 20, 1.25, swim={"vx": 14}), sea_front(),
             {"type": "tag", "text": "20 November 1820", "t0": .25},
             {"type": "caption", "text": "the middle of the *pacific*", "t0": T.w(1, "Pacific")}])

@shot(["The whaleship Essex, out of Nantucket, is fifteen months into her voyage."])
def _(T):
    return ({"depth": .35}, {"zoomFrom": 1.15, "zoomTo": 1.3, "x": 900, "y": 360},
            [sea_back(), ship(820, WL - 20, 1.25, swim={"vx": 10}), sea_front(),
             {"type": "factstack", "size": 27, "x": 90, "y": 760, "w": 520, "items": [
                 {"text": "Whaleship Essex", "t0": T.w(0, "Essex")},
                 {"text": "Out of Nantucket", "t0": T.w(0, "Nantucket")},
                 {"text": "15 months at sea", "t0": T.w(0, "fifteen")}]}])

@shot(["Her crew of twenty is hunting the most valuable animal in the ocean."])
def _(T):
    return ({"depth": .55}, {"zoomFrom": 1, "zoomTo": 1.1, "panX": -60},
            [whale(380, 600, 1.5, swim={"vx": 34}),
             {"type": "school", "kind": "fish", "x": 1450, "y": 330, "w": 380, "h": 140, "count": 14, "scale": .12, "swim": {"vx": -20}, "flip": True, "dim": True},
             {"type": "caption", "text": "the most *valuable* animal in the ocean", "pos": "top", "t0": T.w(0, "valuable")}])

@shot(["The sperm whale."])
def _(T):
    return ({"depth": .6, "spotlight": {"x": 980, "w": 520}}, {"zoomFrom": 1, "zoomTo": 1.18, "x": 1000},
            [whale(880, 560, 1.9, swim={"vx": 8}),
             {"type": "namecard", "title": "SPERM WHALE", "sub": "Physeter macrocephalus", "x": 960, "y": 900, "w": 440, "t0": T.w(0, "sperm")}])

@shot(["Its giant head holds a waxy oil that lit the lamps and candles of the world."])
def _(T):
    return ({"depth": .65}, {},
            [whale(560, 600, 1.7, swim={"vx": 6}),
             {"type": "circle", "x": 840, "y": 600, "rx": 170, "ry": 120, "t0": T.w(0, "head")},
             {"type": "factstack", "size": 27, "x": 1200, "y": 440, "w": 560, "items": [
                 {"text": "Spermaceti oil", "t0": T.w(0, "oil")},
                 {"text": "Lamps & candles", "t0": T.w(0, "lamps")},
                 {"text": "Worth a fortune", "t0": T.w(0, "world")}]}])

@shot(["That morning, the lookout spots a pod.", "The men lower their small boats and give chase."])
def _(T):
    return ({"depth": .3, "sun": {"x": 720, "y": -60, "r": 560}, "surface": True}, {"zoomFrom": 1, "zoomTo": 1.08},
            [{"type": "school", "kind": "whale", "mode": "silhouette", "x": 900, "y": 660, "w": 1000, "h": 260, "count": 5, "scale": .6, "swim": {"vx": 40}, "seed": 3},
             boat(380, 34, .42, swim={"vx": 70}, t0=T.p(1)), boat(760, 30, .42, swim={"vx": 66}, t0=T.p(1) + .3, phase=2),
             boat(1140, 36, .42, swim={"vx": 72}, t0=T.p(1) + .6, phase=4),
             {"type": "tag", "text": "The hunt", "t0": .2},
             {"type": "caption", "text": "the men *give chase*", "t0": T.w(1, "chase")}])

@shot(["But one whale stays behind.", "A huge bull."])
def _(T):
    return ({"depth": .62}, {"zoomFrom": 1, "zoomTo": 1.15, "x": 900},
            [{"type": "school", "kind": "whale", "mode": "silhouette", "x": 1500, "y": 300, "w": 500, "h": 160, "count": 3, "scale": .35, "swim": {"vx": 60}, "dim": True, "seed": 9},
             whale(760, 600, 2.3, swim={"vx": 4}),
             {"type": "caption", "text": "one whale *stays behind*", "t0": T.w(0, "stays")}])

@shot(["The first mate guessed it was eighty-five feet long."])
def _(T):
    return ({"depth": .66, "seabed": "dark", "seabedY": 940}, {},
            [{"type": "gridlines", "lines": [{"y": 260, "label": "25 m"}, {"y": 900, "label": "0 m"}], "t0": 0},
             whale(900, 540, 2.0, swim={"vx": 2}, bob=2),
             {"type": "bracket", "x1": 390, "y1": 720, "x2": 1280, "y2": 720, "label": "~26 M · 85 FT", "t0": T.w(0, "eighty")},
             {"type": "pill", "text": "The first mate's estimate", "x": 90, "y": 120, "t0": T.w(0, "mate"), "size": 26},
             {"type": "pill", "text": "Most adult males: ~16 m", "x": 1180, "y": 120, "t0": T.w(0, "long") + .4, "size": 26}])

@shot(["It isn't fleeing.", "It is lining up with the ship."])
def _(T):
    return ({"depth": .72, "sun": {"x": 1350, "y": -100, "r": 520}, "surface": True}, {"zoomFrom": 1, "zoomTo": 1.12, "x": 1360, "y": 150},
            [ship(1360, 4, 1.4, sil=True, swim={"vx": 4}),
             whale(240, 420, 1.1, sil=True, rotate=-9, swim={"vx": 30}),
             {"type": "caption", "text": "it isn't *fleeing*", "t0": T.w(0, "fleeing"), "t1": T.p(1) - .1},
             {"type": "caption", "text": "it's !lining up!", "t0": T.w(1, "lining")},
             {"type": "reticle", "x": 1360, "y": 150, "r": 90, "t0": T.w(1, "ship")}])

@shot(["It rams the bow.", "The ship shudders."], thud=("rams", .85))
def _(T):
    hit = T.w(0, "rams")
    return ({"depth": .72, "sun": {"x": 1300, "y": -100, "r": 520}, "surface": True}, {"zoomFrom": 1.1, "zoomTo": 1.2, "x": 1300, "y": 200},
            [ship(1100, 4, 1.4, sil=True),
             whale(520, 540, 1.1, sil=True, rotate=-14, moveTo={"x": 1176, "y": 200, "dur": .9, "t0": hit - .05}),
             {"type": "stamp", "text": "Impact", "x": 1460, "y": 560, "t0": hit + .85},
             {"type": "caption", "text": "the ship *shudders*", "t0": T.w(1, "shudders")}])

@shot(["Then it turns, swims off, and comes back faster."])
def _(T):
    return ({"depth": .85, "rays": False}, {"zoomFrom": 1, "zoomTo": 1.1},
            [whale(1300, 620, 1.3, sil=True, flip=True, swim={"vx": -110}),
             whale(-300, 520, 1.3, sil=True, swim={"vx": 520}, t0=T.w(0, "back")),
             {"type": "caption", "text": "it comes back *faster*", "t0": T.w(0, "faster")}])

@shot(["It hits again."], thud=("hits", .6))
def _(T):
    hit = T.w(0, "hits")
    return ({"depth": .72, "sun": {"x": 1300, "y": -100, "r": 520}, "surface": True}, {"zoomFrom": 1.15, "zoomTo": 1.25, "x": 1300, "y": 200},
            [ship(1100, 4, 1.4, sil=True, rotate=3),
             whale(700, 420, 1.1, sil=True, rotate=-12, moveTo={"x": 1176, "y": 205, "dur": .6, "t0": hit - .05}),
             {"type": "stamp", "text": "Again", "x": 1400, "y": 560, "t0": hit + .6}])

@shot(["The bow is smashed open.", "Within minutes, the Essex begins to sink."])
def _(T):
    return ({"depth": .45}, {"zoomFrom": 1.05, "zoomTo": 1.2, "x": 900, "y": 440},
            [sea_back(), ship(800, WL - 20, 1.25, rotate=9, moveTo={"x": 830, "y": WL + 140, "dur": T.dur, "t0": 0}, bob=1), sea_front(),
             {"type": "circle", "x": 1080, "y": 470, "rx": 120, "ry": 90, "t0": T.w(0, "smashed"), "t1": T.p(1)},
             {"type": "tag", "text": "Minutes", "t0": T.w(1, "minutes")},
             {"type": "caption", "text": "the essex is *sinking*", "t0": T.w(1, "sink")}])

@shot(["Twenty men.", "Three small boats.", "Thousands of kilometres from the nearest continent."], chapter=True)
def _(T):
    return ({"depth": .5, "sun": {"x": 1200, "y": -80, "r": 420}, "surface": True}, {"zoomFrom": 1, "zoomTo": 1.1, "x": 1200},
            [boat(1000, 34, .32, swim={"vx": 6}), boat(1240, 28, .32, swim={"vx": 6}, phase=2), boat(1470, 36, .32, swim={"vx": 6}, phase=4),
             {"type": "factstack", "size": 27, "x": 90, "y": 600, "w": 700, "gap": 80, "items": [
                 {"text": "20 men", "t0": T.p(0)},
                 {"text": "3 whaleboats", "t0": T.p(1)},
                 {"text": "Thousands of km from land", "t0": T.w(2, "Thousands"), "tone": "red"}]}])

@shot(["The nearest islands were the Marquesas.", "But the officers had heard stories of cannibals there.",
       "So they chose the longest route of all.", "South America."])
def _(T):
    return ({"depth": .82, "rays": False}, {},
            [{"type": "checklist", "x": 640, "y": 420, "w": 680, "title": "Their options", "t0": .1,
              "items": [{"text": "Marquesas · closest"}, {"text": "South America · farthest", "check": T.w(3, "America")}]},
             {"type": "redx", "x": 1150, "y": 450, "size": 36, "t0": T.w(1, "cannibals")},
             {"type": "pill", "text": "Feared cannibals", "x": 1350, "y": 420, "t0": T.w(1, "cannibals") + .2, "tone": "red", "size": 26},
             {"type": "caption", "text": "the *longest* route", "pos": "top", "t0": T.w(2, "longest")}])

@shot(["Food ran out.", "Then water.", "Men began to die."])
def _(T):
    return ({"mode": "black"}, {},
            [{"type": "bignumber", "from": 1, "to": 60, "prefix": "DAY ", "x": 960, "y": 470, "size": 130, "color": "#e9eef2", "dur": T.dur, "t0": 0},
             {"type": "factstack", "size": 27, "x": 660, "y": 600, "w": 600, "items": [
                 {"text": "Food · gone", "t0": T.p(0) + .3},
                 {"text": "Water · gone", "t0": T.p(1) + .2},
                 {"text": "Men begin to die", "t0": T.w(2, "die"), "tone": "red"}]}])

@shot(["To survive, the living did the unthinkable."])
def _(T):
    return ({"mode": "black"}, {"zoomFrom": 1, "zoomTo": 1.05},
            [{"type": "stamp", "text": "The unthinkable", "x": 960, "y": 560, "size": 70, "t0": T.w(0, "unthinkable")}])

@shot(["They ate the dead.", "In the captain's boat, they drew lots to decide who would be next."])
def _(T):
    return ({"depth": .95, "rays": False, "surface": True}, {"zoomFrom": 1, "zoomTo": 1.12, "x": 960, "y": 200},
            [boat(960, 40, .6, bob=6),
             {"type": "caption", "text": "they drew *lots*", "t0": T.w(1, "lots")}])

@shot(["After about ninety days, passing whaleships finally found them."], chapter=True)
def _(T):
    return ({"depth": .2, "sun": {"x": 900, "y": -60, "r": 700}, "surface": True}, {"zoomFrom": 1, "zoomTo": 1.1},
            [ship(1500, 4, 1.2, sil=True, swim={"vx": -30}, flip=True), boat(700, 30, .4),
             {"type": "tag", "text": "February 1821", "t0": .2},
             {"type": "caption", "text": "rescued after *~90 days*", "t0": T.w(0, "ninety")}])

@shot(["Of twenty men, only eight survived."])
def _(T):
    return ({"depth": .55, "rays": False}, {},
            [{"type": "bignumber", "from": 20, "to": 8, "x": 960, "y": 600, "size": 240, "t0": T.w(0, "eight") - .5, "dur": 1.0},
             {"type": "pill", "text": "Out of 20 men", "x": 770, "y": 700, "t0": T.w(0, "twenty"), "size": 26},
             {"type": "caption", "text": "*survived*", "t0": T.w(0, "survived"), "y": 860}])

@shot(["Years later, a young sailor named Herman Melville read the first mate's account."], chapter=True)
def _(T):
    return ({"mode": "paper"}, {"zoomFrom": 1, "zoomTo": 1.08},
            [{"type": "doccard", "x": 960, "y": 560, "w": 640, "h": 760, "header": "1821 · Owen Chase, first mate",
              "title": "Narrative of the\nshipwreck of the\nwhale-ship Essex", "footer": "A true account", "t0": 0},
             {"type": "tag", "text": "Herman Melville", "t0": T.w(0, "Melville")},
             {"type": "circle", "x": 960, "y": 270, "rx": 290, "ry": 50, "t0": T.w(0, "account")}])

@shot(["In eighteen fifty-one, he turned it into a novel.", "You know it as Moby-Dick."])
def _(T):
    return ({"mode": "paper"}, {"zoomFrom": 1.02, "zoomTo": 1.1},
            [{"type": "doccard", "x": 960, "y": 540, "w": 600, "h": 740, "rotate": 2, "header": "1851 · Herman Melville",
              "title": "Moby-Dick\nor, the whale", "footer": "A novel", "t0": 0},
             {"type": "tag", "text": "1851", "t0": T.w(0, "fifty")},
             {"type": "stamp", "text": "Based on the Essex", "x": 1280, "y": 820, "size": 42, "color": "#3ecf6a", "t0": T.w(1, "Moby")}])

@shot(["What happened to the whale, no one knows."], chapter=True)
def _(T):
    return ({"depth": .95, "rays": False, "spotlight": {"x": 1100, "w": 380}}, {"zoomFrom": 1, "zoomTo": 1.1, "x": 1100},
            [whale(1250, 620, 1.4, sil=True, flip=True, swim={"vx": -60}),
             {"type": "caption", "text": "!no one knows!", "t0": T.w(0, "knows")}])

@shot(["Was it defending its pod?", "Was it provoked by the hammering of the crew's repairs?",
       "Or did it know exactly what it was doing?"], tail=2.4)
def _(T):
    return ({"depth": 1, "rays": False}, {"zoomFrom": 1, "zoomTo": 1.08},
            [{"type": "factstack", "size": 27, "x": 560, "y": 400, "w": 800, "gap": 84, "items": [
                 {"text": "Defending its pod?", "t0": T.p(0) + .2},
                 {"text": "Provoked by the noise?", "t0": T.w(1, "hammering")},
                 {"text": "Or did it mean to?", "t0": T.w(2, "exactly"), "tone": "red"}]},
             {"type": "stamp", "text": "Never explained", "x": 960, "y": 860, "size": 48, "t0": T.p(2) + T.d(2) + .5}])

# ---------------------------------------------------------------- voiceover
from kokoro_onnx import Kokoro
kok = Kokoro(os.path.join(TTS, "kokoro.onnx"), os.path.join(TTS, "voices.bin"))

def trim(a, thr=0.008):
    idx = np.where(np.abs(a) > thr)[0]
    if not len(idx): return a
    return a[max(0, idx[0] - int(.03 * SR)): idx[-1] + int(.08 * SR)]

audio, cur = [np.zeros(int(.5 * SR), dtype=np.float32)], .5
for si, s in enumerate(S):
    if si:
        gap = .85 if s["chapter"] else .42
        audio.append(np.zeros(int(gap * SR), dtype=np.float32)); cur += gap
    s["ph"] = []
    for li, line in enumerate(s["lines"]):
        if li:
            audio.append(np.zeros(int(.28 * SR), dtype=np.float32)); cur += .28
        a, sr = kok.create(line, voice=VOICE, speed=SPEED, lang=LANG)
        assert sr == SR
        a = trim(a.astype(np.float32)); d = len(a) / SR
        s["ph"].append((cur, d)); audio.append(a); cur += d
        print(f"{cur:7.2f}  {line}")
tail = S[-1].get("tail", 2.0)
audio.append(np.zeros(int(tail * SR), dtype=np.float32)); cur += tail
sf.write(os.path.join(OUT, "vo.wav"), np.concatenate(audio), SR)

# ---------------------------------------------------------------- scene
class Timing:
    def __init__(self, s, start, end):
        self.s, self.start, self.dur = s, start, end - start
    def p(self, i): return round(self.s["ph"][i][0] - self.start, 2)
    def d(self, i): return self.s["ph"][i][1]
    def w(self, i, word):
        line = self.s["lines"][i]; k = line.find(word)
        assert k >= 0, (word, line)
        a0, d = self.s["ph"][i]
        return round(a0 - self.start + d * k / len(line) - .05, 2)

starts = [0.0] + [round(s["ph"][0][0] - .18, 2) for s in S[1:]]
ends = starts[1:] + [round(cur, 2)]
shots, thuds = [], []
for i, s in enumerate(S):
    T = Timing(s, starts[i], ends[i])
    bg, cam, els = s["fn"](T)
    els = [{k: v for k, v in e.items() if v is not None} for e in els]
    sh = {"start": starts[i], "end": ends[i], "bg": bg, "camera": cam, "elements": els}
    if s["chapter"] or i == 0: sh["fadeIn"] = .5
    if i == len(S) - 1: sh["fadeOut"] = 1.4
    if s.get("thud"):
        word, off = s["thud"]; thuds.append(round(starts[i] + T.w(0, word) + off, 2))
    shots.append(sh)

scene = {"preset": "abyss", "width": 1920, "height": 1080, "fps": 30, "grain": .05,
         "tokens": {"creature": {"whale": ["#8f8e8a", "#6f6e6a", "#b5b4ae"], "fish": ["#7f97a6", "#c3d2da", "#4c606c"],
                                 "blob": ["#3b2a1f", "#3b2a1f", "#3b2a1f"]}},
         "shots": shots}
json.dump(scene, open(os.path.join(OUT, "scene.json"), "w"), indent=1)
json.dump({"duration": round(cur, 2), "thuds": thuds, "stamps": [round(sh["start"] + e["t0"], 2) for sh in shots for e in sh["elements"] if e["type"] == "stamp"]},
          open(os.path.join(OUT, "timeline.json"), "w"), indent=1)
open(os.path.join(OUT, "script.txt"), "w").write("\n\n".join(" ".join(s["lines"]) for s in S) + "\n")
print("duration", round(cur, 2), "shots", len(shots), "thuds", thuds)
