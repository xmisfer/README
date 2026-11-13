"""Shared helpers for KazChart story builds: art markup, Kokoro voiceover, timing, scene + timeline output."""
import json, os
import numpy as np
import soundfile as sf

SR = 24000
SURF = 64      # bottom edge of the engine's surface band
WL = 430       # waterline in cross-section shots
BLACK = "#05090d"

# ---------------------------------------------------------------- art (local coords, facing right)
def sailship(sil=False):
    hull, rail, wood, sail, rope = (BLACK,) * 5 if sil else ("#3b2a1f", "#e8e2d2", "#2a1d15", "#dcd3bd", "#2a1d15")
    s = f'<path fill="{hull}" d="M-222,-52 L232,-58 L206,0 C186,50 110,64 0,64 C-120,64 -186,54 -206,16 Z"/>'
    if not sil:
        s += f'<rect x="-205" y="-44" width="420" height="9" fill="{rail}" opacity=".85"/>'
        s += ''.join(f'<rect x="{x}" y="-44" width="14" height="9" fill="{hull}"/>' for x in range(-180, 200, 46))
    s += f'<path fill="none" stroke="{rope}" stroke-width="6" d="M226,-56 L330,-118"/>'
    for mx, h in ((-118, 300), (18, 345), (142, 285)):
        s += f'<rect x="{mx - 4}" y="{-52 - h}" width="8" height="{h}" fill="{wood}"/>'
        for w, y0, y1 in ((172, -95, -170), (140, -180, -245), (100, -255, -305)):
            if -y1 > h + 40: continue
            w2 = w * .88
            s += f'<path fill="{sail}" opacity="{1 if sil else .96}" d="M{mx - w/2},{y0} L{mx + w/2},{y0} L{mx + w2/2},{y1} L{mx - w2/2},{y1} Z"/>'
        s += f'<path fill="none" stroke="{rope}" stroke-width="2" opacity=".7" d="M{mx},{-52 - h} L{mx - 120},-52 M{mx},{-52 - h} L{mx + 120},-52"/>'
    s += f'<path fill="{sail}" opacity="{1 if sil else .9}" d="M150,-320 L320,-116 L170,-90 Z"/>'
    return s

def whaleboat(sil=True):
    c = BLACK if sil else "#5a4232"
    s = f'<path fill="{c}" d="M-196,-54 L196,-54 L176,8 C120,58 -120,58 -176,8 Z"/>'
    for x in range(-120, 140, 60):
        s += f'<circle cx="{x}" cy="-78" r="15" fill="{c}"/><rect x="{x - 12}" y="-70" width="24" height="18" fill="{c}"/>'
        s += f'<path stroke="{c}" stroke-width="7" stroke-linecap="round" d="M{x},-62 L{x - 70},60"/>'
    return s

def cruiser(mode=None):
    """WWII heavy cruiser, ~900 local units long. mode: None | 'sil' | 'sonar'"""
    if mode == 'sil': hull = sup = dark = deck = BLACK; st = ''
    elif mode == 'sonar': hull = sup = dark = deck = '#0b2a12'; st = 'stroke="#39ff6a" stroke-width="4"'
    else: hull, sup, dark, deck, st = '#66727a', '#7d8a92', '#3d474e', '#8f9ba2', ''
    s = f'<path fill="{hull}" {st} d="M-440,-54 L470,-62 L440,-10 L400,40 C200,58 -200,58 -420,46 Z"/>'
    if mode is None: s += f'<path fill="{dark}" opacity=".5" d="M-420,20 L420,14 L400,40 C200,58 -200,58 -420,46 Z"/>'
    s += f'<rect x="-130" y="-122" width="230" height="70" fill="{sup}" {st}/>'
    s += f'<path fill="{sup}" {st} d="M40,-122 L40,-196 L70,-214 L112,-214 L112,-122 Z"/>'
    s += f'<rect x="84" y="-300" width="8" height="90" fill="{dark}" {st}/><path stroke="{dark}" stroke-width="5" d="M60,-270 L116,-270"/>'
    for fx in (-70, -165):
        s += f'<path fill="{dark}" {st} d="M{fx},-122 L{fx - 8},-200 L{fx + 36},-200 L{fx + 44},-122 Z"/>'
    for tx, d in ((190, 1), (285, 1), (-300, -1)):
        s += f'<path fill="{dark}" {st} d="M{tx - 34},-54 L{tx - 28},-86 L{tx + 30},-86 L{tx + 36},-54 Z"/>'
        for k in (-8, 0, 8):
            s += f'<path stroke="{dark}" stroke-width="5" d="M{tx},{-74 + k} L{tx + d * 90},{-80 + k}"/>'
    s += f'<path fill="none" stroke="{dark}" stroke-width="2" opacity=".7" d="M88,-300 L-300,-54 M88,-300 L440,-58"/>'
    return s

def submarine(mode=None):
    if mode == 'sil': c, d, st = BLACK, BLACK, ''
    elif mode == 'sonar': c, d, st = '#0b2a12', '#0b2a12', 'stroke="#39ff6a" stroke-width="4"'
    else: c, d, st = '#262d32', '#151a1e', ''
    return (f'<path fill="{c}" {st} d="M-330,0 C-300,-50 -150,-56 0,-56 C180,-56 300,-40 340,0 C300,40 180,58 0,58 C-150,58 -300,50 -330,0 Z"/>'
            f'<path fill="{d}" {st} d="M-40,-54 L-30,-116 L70,-116 L96,-54 Z"/><rect x="20" y="-170" width="6" height="56" fill="{d}"/>'
            f'<path fill="{d}" d="M-330,0 L-380,-40 L-372,0 L-380,40 Z"/>')

def swimmer(x, y, s=1.0, ph=0.0):
    """Silhouette of a man in a life vest seen from below: head at the surface, legs dangling."""
    k = np.sin(ph) * 10
    return (f'<g transform="translate({x} {y}) scale({s})" fill="{BLACK}">'
            f'<circle cx="0" cy="-8" r="15"/><rect x="-20" y="4" width="40" height="52" rx="10"/>'
            f'<path stroke="{BLACK}" stroke-width="12" stroke-linecap="round" fill="none" d="M-18,14 L-40,{44 + k} M18,14 L40,{40 - k}"/>'
            f'<path stroke="{BLACK}" stroke-width="13" stroke-linecap="round" fill="none" d="M-8,54 L{-14 + k},116 M8,54 L{14 - k},112"/></g>')

def sea_back(sun_x=1480):
    return {"type": "svg", "markup":
        '<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#18303f"/>'
        '<stop offset="1" stop-color="#6d8e9c"/></linearGradient></defs>'
        f'<rect x="-600" y="-600" width="3120" height="{WL + 600}" fill="url(#sky)"/>'
        f'<circle cx="{sun_x}" cy="250" r="70" fill="#e9f3f2" opacity=".55"/>'
        f'<circle cx="{sun_x}" cy="250" r="160" fill="#e9f3f2" opacity=".08"/>'}

def sea_front():
    return {"type": "svg", "markup":
        f'<rect x="-600" y="{WL}" width="3120" height="1400" fill="#17465d" opacity=".42"/>'
        f'<path fill="none" stroke="#cfe9f2" stroke-width="4" opacity=".55" d="M-600,{WL} '
        + ' '.join(f'Q{x + 60},{WL - 8} {x + 120},{WL}' for x in range(-600, 2520, 120)) + '"/>'}

def prop(markup, x, y, scale=1.0, mode=None, **kw):
    """A drawn object riding on the creature rig (swim, bob, moveTo, approach). The rig's placeholder
    ellipse (rx160 ry50 local) is coloured like 'blob' in tokens and must be covered by the markup."""
    e = {"type": "creature", "kind": "blob", "x": x, "y": y, "scale": scale, "inner": markup, "bob": kw.pop("bob", 3), **kw}
    if mode in ("silhouette", "sonar"): e["mode"] = mode
    return e

def ship(x, y, scale=1.0, sil=False, **kw):
    if sil and y < 40: y = SURF + 52 * scale - 6
    return prop(sailship(sil), x, y, scale, "silhouette" if sil else None, **kw)

def boat(x, y, scale=.4, **kw):
    if y < 60: y = SURF + 54 * scale - 4
    return prop(whaleboat(), x, y, scale, "silhouette", **kw)

def whale(x, y, scale=1.0, sil=False, **kw):
    e = {"type": "creature", "kind": "whale", "x": x, "y": y, "scale": scale, **kw}
    if sil: e["mode"] = "silhouette"
    return e

def shark(x, y, scale=1.0, sil=False, **kw):
    e = {"type": "creature", "kind": "shark", "x": x, "y": y, "scale": scale, **kw}
    if sil: e["mode"] = "silhouette"
    return e

TOKENS = {"creature": {"whale": ["#8f8e8a", "#6f6e6a", "#b5b4ae"], "fish": ["#7f97a6", "#c3d2da", "#4c606c"],
                       "shark": ["#5d6872", "#d9dcdc", "#2b3138"], "blob": ["#3b2a1f", "#3b2a1f", "#3b2a1f"]}}

# ---------------------------------------------------------------- story builder
class Story:
    def __init__(self): self.S = []
    def shot(self, lines, chapter=False, **opt):
        def deco(fn):
            self.S.append(dict(lines=lines, chapter=chapter, fn=fn, **opt)); return fn
        return deco

class Timing:
    def __init__(self, s, start, end): self.s, self.start, self.dur = s, start, end - start
    def p(self, i): return round(self.s["ph"][i][0] - self.start, 2)
    def d(self, i): return self.s["ph"][i][1]
    def w(self, i, word):
        line = self.s["lines"][i]; k = line.find(word)
        assert k >= 0, (word, line)
        a0, d = self.s["ph"][i]
        return round(a0 - self.start + d * k / len(line) - .05, 2)

def _trim(a, thr=.008):
    idx = np.where(np.abs(a) > thr)[0]
    return a if not len(idx) else a[max(0, idx[0] - int(.03 * SR)): idx[-1] + int(.08 * SR)]

def build(story, tts_dir, out, voice, lang, speed=.94, width=1920, height=1080, gaps=(.42, .85, .28), lead=.5, tokens=None, say=None):
    """say: {written word: spoken spelling}, applied to the voiceover only; captions and timing keep the written line."""
    from kokoro_onnx import Kokoro
    kok = Kokoro(os.path.join(tts_dir, "kokoro.onnx"), os.path.join(tts_dir, "voices.bin"))
    S = story.S
    shot_gap, chap_gap, line_gap = gaps
    audio, cur = [np.zeros(int(lead * SR), np.float32)], lead
    for si, s in enumerate(S):
        if si:
            g = chap_gap if s["chapter"] else shot_gap
            audio.append(np.zeros(int(g * SR), np.float32)); cur += g
        s["ph"] = []
        for li, line in enumerate(s["lines"]):
            if li:
                audio.append(np.zeros(int(line_gap * SR), np.float32)); cur += line_gap
            spoken = line
            for w, sp in (say or {}).items(): spoken = spoken.replace(w, sp)
            a, sr = kok.create(spoken, voice=voice, speed=speed, lang=lang)
            a = _trim(a.astype(np.float32)); d = len(a) / SR
            s["ph"].append((cur, d)); audio.append(a); cur += d
    tail = S[-1].get("tail", 2.0)
    audio.append(np.zeros(int(tail * SR), np.float32)); cur += tail
    os.makedirs(out, exist_ok=True)
    sf.write(os.path.join(out, "vo.wav"), np.concatenate(audio), SR)

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
        for word, off, li in s.get("thuds", []):
            thuds.append(round(starts[i] + T.w(li, word) + off, 2))
        shots.append(sh)
    scene = {"preset": "abyss", "width": width, "height": height, "fps": 30, "grain": .05,
             "tokens": tokens or TOKENS, "shots": shots}
    json.dump(scene, open(os.path.join(out, "scene.json"), "w"), indent=1)
    stamps = [round(sh["start"] + e["t0"], 2) for sh in shots for e in sh["elements"] if e["type"] == "stamp"]
    json.dump({"duration": round(cur, 2), "thuds": thuds, "stamps": stamps}, open(os.path.join(out, "timeline.json"), "w"), indent=1)
    open(os.path.join(out, "script.txt"), "w").write("\n\n".join(" ".join(s["lines"]) for s in S) + "\n")
    print("duration", round(cur, 2), "shots", len(shots), "thuds", thuds)
    return shots
