"""USS Indianapolis (1945), 16:9 abyss documentary. Usage: python3 indy.py <tts_dir> <out_dir>"""
import sys
from kzlib import *

st = Story(); shot = st.shot

def ship_cs(x, s=.95, **kw):   # cruiser on the waterline in cross-section shots
    return prop(cruiser(), x, WL - 30 * s, s, **kw)
def ship_below(x, s=.9, **kw):  # cruiser silhouette seen from below the surface
    return prop(cruiser('sil'), x, SURF + 54 * s - 6, s, "silhouette", **kw)
def swimmers(xs, y=SURF + 8, s=1.0, seed=0):
    import random; r = random.Random(seed)
    return {"type": "svg", "markup": "".join(swimmer(x + r.uniform(-20, 20), y + r.uniform(-4, 6), s * r.uniform(.85, 1.1), r.uniform(0, 6)) for x in xs)}

@shot(["In the summer of nineteen forty-five, nearly nine hundred men went into the sea.", "Only three hundred and sixteen came out."])
def _(T):
    return ({"depth": .8, "sun": {"x": 960, "y": -100, "r": 700}, "surface": True}, {"zoomFrom": 1, "zoomTo": 1.12, "x": 960, "y": 200},
            [swimmers(range(420, 1560, 95), seed=1),
             shark(-200, 620, .9, sil=True, swim={"vx": 140}, t0=T.p(1) - .4),
             {"type": "tag", "text": "1945", "t0": .3},
             {"type": "caption", "text": "nearly *900* men went into the sea", "t0": T.w(0, "nine"), "t1": T.p(1) - .1},
             {"type": "caption", "text": "only !316! came out", "t0": T.w(1, "three")}])

@shot(["This is the story of the U.S.S. Indianapolis."], chapter=True)
def _(T):
    return ({"depth": .35}, {"zoomFrom": 1, "zoomTo": 1.08, "x": 960, "y": 420},
            [sea_back(), ship_cs(900, swim={"vx": 10}), sea_front(),
             {"type": "tag", "text": "July 1945", "t0": .2},
             {"type": "namecard", "title": "USS INDIANAPOLIS", "sub": "Heavy cruiser · CA-35", "x": 960, "y": 860, "w": 520, "t0": T.w(0, "Indianapolis")}])

@shot(["A heavy cruiser with almost twelve hundred men aboard,", "she had just completed a top secret mission."])
def _(T):
    return ({"depth": .35}, {"zoomFrom": 1.12, "zoomTo": 1.25, "x": 900, "y": 380},
            [sea_back(), ship_cs(880, swim={"vx": 6}), sea_front(),
             {"type": "factstack", "x": 90, "y": 740, "w": 560, "size": 27, "gap": 80, "items": [
                 {"text": "Heavy cruiser", "t0": T.w(0, "heavy")},
                 {"text": "1,195 men aboard", "t0": T.w(0, "twelve")},
                 {"text": "Top secret mission", "t0": T.w(1, "secret"), "tone": "red"}]}])

@shot(["Delivering parts of the atomic bomb that would soon fall on Hiroshima."])
def _(T):
    return ({"mode": "paper"}, {"zoomFrom": 1, "zoomTo": 1.08},
            [{"type": "doccard", "x": 960, "y": 540, "w": 640, "h": 740, "header": "Tinian Island · 26 July 1945",
              "title": "Cargo delivered:\natomic bomb\ncomponents", "footer": "Destination: Hiroshima", "t0": 0},
             {"type": "stamp", "text": "Top secret", "x": 1300, "y": 820, "size": 50, "t0": T.w(0, "atomic")}])

@shot(["Then she sailed on alone, with no escort."], chapter=True)
def _(T):
    return ({"depth": .55, "rays": True, "surface": True, "sun": {"x": 700, "y": -80, "r": 520}}, {"zoomFrom": 1, "zoomTo": 1.1, "x": 960, "y": 200},
            [ship_below(1100, swim={"vx": 20}),
             {"type": "caption", "text": "*alone*. no escort.", "t0": T.w(0, "alone")}])

@shot(["Just after midnight on July thirtieth, a Japanese submarine found her."])
def _(T):
    return ({"mode": "sonar"}, {},
            [{"type": "sonar", "t0": 0, "blips": [{"x": 1420, "y": 300, "label": "USS Indianapolis", "t": T.w(0, "found")}]},
             prop(submarine('sonar'), 330, 560, .5, "sonar", bob=2),
             prop(cruiser('sonar'), 1420, 380, .45, "sonar", bob=2, t0=T.w(0, "found") - .2),
             {"type": "tag", "text": "30 July · 00:14", "t0": .2},
             {"type": "pill", "text": "Submarine I-58", "x": 160, "y": 700, "size": 24, "t0": T.w(0, "Japanese")}])

@shot(["Two torpedoes.", "Twelve minutes.", "The Indianapolis was gone."], thuds=[("Two", .2, 0)])
def _(T):
    return ({"depth": .45}, {"zoomFrom": 1.05, "zoomTo": 1.2, "x": 900, "y": 440},
            [sea_back(), ship_cs(880, rotate=8, moveTo={"x": 900, "y": WL + 170, "dur": T.dur, "t0": 0}, bob=1), sea_front(),
             {"type": "factstack", "x": 1300, "y": 700, "w": 480, "size": 27, "gap": 80, "items": [
                 {"text": "2 torpedoes", "t0": T.p(0)},
                 {"text": "12 minutes", "t0": T.p(1)},
                 {"text": "Gone", "t0": T.w(2, "gone"), "tone": "red"}]}])

@shot(["About three hundred men went down with her."])
def _(T):
    return ({"depth": .9, "rays": False}, {"zoomFrom": 1, "zoomTo": 1.06},
            [{"type": "bignumber", "from": 0, "to": 300, "prefix": "~", "x": 960, "y": 560, "size": 200, "t0": T.w(0, "three") - .2, "dur": 1.2},
             {"type": "caption", "text": "went down with the ship", "y": 700, "t0": T.w(0, "down")}])

@shot(["The rest, nearly nine hundred, were left floating in the open ocean."], chapter=True)
def _(T):
    return ({"depth": .5, "sun": {"x": 960, "y": -100, "r": 760}, "surface": True}, {"zoomFrom": 1, "zoomTo": 1.15, "x": 960, "y": 150},
            [swimmers(range(260, 1720, 80), seed=3),
             {"type": "tag", "text": "Philippine Sea", "t0": .2},
             {"type": "caption", "text": "floating in the *open ocean*", "t0": T.w(0, "floating")}])

@shot(["Few lifeboats.", "Little water.", "And no one knew they were missing."])
def _(T):
    return ({"depth": .6, "surface": True, "sun": {"x": 1300, "y": -100, "r": 500}}, {"zoomFrom": 1, "zoomTo": 1.08, "x": 1300, "y": 150},
            [swimmers(range(1000, 1700, 90), seed=5),
             {"type": "factstack", "x": 90, "y": 560, "w": 620, "size": 28, "gap": 84, "items": [
                 {"text": "Few lifeboats", "t0": T.p(0)},
                 {"text": "Little water", "t0": T.p(1)},
                 {"text": "No one knew", "t0": T.w(2, "knew"), "tone": "red"}]}])

@shot(["Then the sharks came."])
def _(T):
    return ({"depth": .75, "surface": True, "sun": {"x": 960, "y": -100, "r": 560}}, {"zoomFrom": 1, "zoomTo": 1.15, "x": 960, "y": 200},
            [swimmers(range(560, 1400, 85), seed=7),
             shark(150, 620, 1.0, sil=True, swim={"vx": 150}),
             shark(1850, 820, .8, sil=True, flip=True, swim={"vx": -140}, phase=2),
             {"type": "caption", "text": "then the !sharks! came", "t0": T.w(0, "sharks")}])

@shot(["Oceanic whitetips, drawn by the sinking, the noise, and the blood."])
def _(T):
    return ({"depth": .62}, {"zoomFrom": 1, "zoomTo": 1.15, "x": 900},
            [shark(700, 520, 1.6, swim={"vx": 20}),
             {"type": "namecard", "title": "OCEANIC WHITETIP", "sub": "Carcharhinus longimanus", "x": 960, "y": 880, "w": 520, "t0": T.w(0, "Oceanic")},
             {"type": "factstack", "x": 1320, "y": 300, "w": 440, "size": 26, "gap": 76, "items": [
                 {"text": "The sinking", "t0": T.w(0, "sinking")},
                 {"text": "The noise", "t0": T.w(0, "noise")},
                 {"text": "The blood", "t0": T.w(0, "blood"), "tone": "red"}]}])

@shot(["Men learned to stay in tight groups.", "Those who drifted away were taken."])
def _(T):
    return ({"depth": .8, "surface": True, "sun": {"x": 800, "y": -100, "r": 480}}, {"zoomFrom": 1, "zoomTo": 1.1, "x": 900, "y": 150},
            [swimmers(range(640, 1000, 55), seed=9), swimmers([1500], seed=10),
             {"type": "circle", "x": 820, "y": 130, "rx": 260, "ry": 110, "color": "#3ecf6a", "t0": T.w(0, "tight")},
             shark(1950, 420, .7, sil=True, flip=True, swim={"vx": -140}, t0=T.p(1)),
             {"type": "circle", "x": 1500, "y": 130, "rx": 90, "ry": 100, "color": "#e5383b", "t0": T.w(1, "drifted")},
             {"type": "caption", "text": "stay in *tight groups*", "t0": T.w(0, "tight"), "t1": T.p(1) - .1},
             {"type": "caption", "text": "drift away and you were !taken!", "t0": T.w(1, "taken")}])

@shot(["But most of the dying came from the sun, thirst, and salt water."], chapter=True)
def _(T):
    return ({"depth": .25, "sun": {"x": 960, "y": -100, "r": 900}, "surface": True, "rayOpacity": .2}, {"zoomFrom": 1, "zoomTo": 1.08},
            [swimmers(range(700, 1300, 110), seed=11),
             {"type": "factstack", "x": 660, "y": 520, "w": 600, "size": 28, "gap": 84, "items": [
                 {"text": "Exposure", "t0": T.w(0, "sun")},
                 {"text": "Dehydration", "t0": T.w(0, "thirst")},
                 {"text": "Saltwater poisoning", "t0": T.w(0, "salt"), "tone": "red"}]}])

@shot(["Some men began to hallucinate.", "Others drank the sea."])
def _(T):
    return ({"mode": "black"}, {"zoomFrom": 1, "zoomTo": 1.06},
            [{"type": "caption", "text": "they began to *hallucinate*", "y": 520, "t0": T.w(0, "hallucinate"), "t1": T.p(1) - .1},
             {"type": "caption", "text": "others !drank the sea!", "y": 520, "t0": T.w(1, "drank")}])

@shot(["On the fourth day, a plane on routine patrol spotted them, by pure chance."], chapter=True)
def _(T):
    return ({"depth": .15, "sun": {"x": 1100, "y": -60, "r": 800}, "surface": True}, {"zoomFrom": 1, "zoomTo": 1.1, "x": 960, "y": 150},
            [swimmers(range(500, 1450, 110), seed=13),
             {"type": "tag", "text": "2 August 1945", "t0": .2},
             {"type": "stamp", "text": "Pure chance", "x": 960, "y": 640, "size": 60, "color": "#3ecf6a", "t0": T.w(0, "chance")},
             {"type": "caption", "text": "spotted on *day four*", "t0": T.w(0, "fourth")}])

@shot(["Of nearly twelve hundred men aboard, three hundred and sixteen survived."])
def _(T):
    return ({"depth": .55, "rays": False}, {},
            [{"type": "bignumber", "from": 1195, "to": 316, "x": 960, "y": 590, "size": 230, "t0": T.w(0, "three") - .3, "dur": 1.4},
             {"type": "pill", "text": "Of 1,195 aboard", "x": 790, "y": 680, "size": 26, "t0": T.w(0, "twelve")},
             {"type": "caption", "text": "*survived*", "y": 880, "t0": T.w(0, "survived")}])

@shot(["It remains the worst loss at sea from a single ship in U.S. Navy history."])
def _(T):
    return ({"depth": .9, "rays": False}, {"zoomFrom": 1, "zoomTo": 1.08},
            [prop(cruiser('sil'), 960, 560, .9, "silhouette", rotate=-4, opacity=.6, bob=1),
             {"type": "stamp", "text": "Worst loss in navy history", "x": 960, "y": 560, "size": 50, "t0": T.w(0, "worst")}])

@shot(["Her captain, Charles McVay, was court-martialed for losing his ship."], chapter=True)
def _(T):
    return ({"mode": "paper"}, {"zoomFrom": 1, "zoomTo": 1.08},
            [{"type": "doccard", "x": 960, "y": 540, "w": 640, "h": 740, "header": "U.S. Navy · December 1945",
              "title": "Court-martial\nof Capt. Charles\nB. McVay III", "footer": "Hazarding his vessel", "t0": 0},
             {"type": "stamp", "text": "Convicted", "x": 1290, "y": 820, "size": 54, "t0": T.w(0, "court")}])

@shot(["Fifty-five years later, Congress cleared his name.", "He did not live to see it."])
def _(T):
    return ({"mode": "paper"}, {"zoomFrom": 1.03, "zoomTo": 1.1},
            [{"type": "doccard", "x": 960, "y": 540, "w": 640, "h": 740, "rotate": 2, "header": "U.S. Congress · October 2000",
              "title": "Resolution:\nCapt. McVay\nexonerated", "footer": "55 years later", "t0": 0},
             {"type": "stamp", "text": "Cleared", "x": 1280, "y": 820, "size": 60, "color": "#3ecf6a", "t0": T.w(0, "cleared")},
             {"type": "caption", "text": "he did not live to see it", "y": 1010, "t0": T.w(1, "live")}])

@shot(["In twenty seventeen, the wreck was finally found,", "five and a half kilometres down."], chapter=True)
def _(T):
    return ({"depth": 1, "rays": False}, {},
            [{"type": "meter", "title": "Depth of the wreck", "value": .5, "number": 5500, "unit": "m", "sub": "found in 2017 · Philippine Sea", "t0": T.p(1) - .3, "dur": 1.0},
             {"type": "tag", "text": "2017", "t0": .2}])

@shot(["She is still there.", "In the dark.", "With the men who never left her."], tail=2.6)
def _(T):
    return ({"depth": 1, "rays": False, "spotlight": {"x": 1000, "w": 520}, "seabed": "dark", "seabedY": 860}, {"zoomFrom": 1, "zoomTo": 1.15, "x": 1000, "y": 760},
            [prop(cruiser(), 1000, 800, .7, rotate=5, bob=0, opacity=.85),
             {"type": "caption", "text": "*still there*", "pos": "top", "t0": T.w(0, "still"), "t1": T.p(1) - .1},
             {"type": "caption", "text": "with the men who *never left her*", "pos": "top", "t0": T.w(2, "never")}])

build(st, sys.argv[1], sys.argv[2], voice="am_michael", lang="en-us", speed=.94,
      tokens={**TOKENS, "creature": {**TOKENS["creature"], "blob": ["#66727a", "#66727a", "#66727a"]}})
