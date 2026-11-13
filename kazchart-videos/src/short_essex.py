"""Vertical Short (1080x1920) of the Essex story. Visible world column: x 656-1264 (centre 960).
Usage: python3 -I short_essex.py <tts_dir> <out_dir>"""
import sys
from kzlib import *

st = Story(); shot = st.shot
CX = 960
def cap(text, t0, y=None, size=50, **kw):
    e = {"type": "caption", "text": text, "x": CX, "size": size, "t0": t0, **kw}
    if y: e["y"] = y
    return e
def tag(text, t0=.2): return {"type": "tag", "text": text, "x": 690, "y": 90, "t0": t0}

@shot(["In eighteen twenty, a whale hunted a ship."])
def _(T):
    return ({"depth": .75, "sun": {"x": 960, "y": -60, "r": 520}, "surface": True}, {"zoomFrom": 1, "zoomTo": 1.1, "x": 960, "y": 300},
            [ship(940, 4, .95, sil=True),
             whale(820, 900, .9, sil=True, rotate=-58, moveTo={"x": 980, "y": 330, "dur": 2.6, "t0": 0}),
             tag("1820"),
             cap("a whale", T.w(0, "whale"), y=760),
             cap("*hunted* a ship", T.w(0, "hunted"), y=830)])

@shot(["The whaleship Essex was deep in the Pacific,", "when a giant sperm whale turned around,"])
def _(T):
    return ({"depth": .35}, {"zoomFrom": 1.05, "zoomTo": 1.15, "x": 960, "y": 420},
            [sea_back(sun_x=1180), ship(900, WL - 20, .95, swim={"vx": 6}), sea_front(),
             whale(1300, 760, .9, flip=True, swim={"vx": -40}, t0=T.p(1)),
             cap("the *essex*", T.w(0, "Essex"), y=980, t1=T.p(1) - .1),
             cap("a *sperm whale*", T.w(1, "sperm"), y=980, size=46)])

@shot(["and rammed it."], thuds=[("rammed", .55, 0)])
def _(T):
    hit = T.w(0, "rammed")
    return ({"depth": .72, "sun": {"x": 1000, "y": -100, "r": 460}, "surface": True}, {"zoomFrom": 1.05, "zoomTo": 1.15, "x": 1060, "y": 200},
            [ship(900, 4, 1.0, sil=True),
             whale(900, 720, .85, sil=True, rotate=-30, moveTo={"x": 970, "y": 260, "dur": .6, "t0": hit - .1}),
             {"type": "stamp", "text": "Impact", "x": CX, "y": 640, "size": 60, "t0": hit + .55}])

@shot(["Then it came back.", "And hit it again."], thuds=[("hit", .5, 1)])
def _(T):
    hit = T.w(1, "hit")
    return ({"depth": .78, "sun": {"x": 1000, "y": -100, "r": 460}, "surface": True}, {"zoomFrom": 1.1, "zoomTo": 1.2, "x": 1060, "y": 200},
            [ship(900, 4, 1.0, sil=True, rotate=3),
             whale(1150, 820, .85, sil=True, flip=True, rotate=20, t1=T.p(1) - .2),
             whale(860, 780, .85, sil=True, rotate=-32, t0=T.p(1) - .2, moveTo={"x": 970, "y": 265, "dur": .55, "t0": hit - .05}),
             cap("it came *back*", T.w(0, "back"), y=980, t1=T.p(1) - .1),
             {"type": "stamp", "text": "Again", "x": CX, "y": 640, "size": 60, "t0": hit + .5}])

@shot(["The ship sank in minutes."])
def _(T):
    return ({"depth": .45}, {"zoomFrom": 1.05, "zoomTo": 1.15, "x": 960, "y": 440},
            [sea_back(sun_x=1180), ship(890, WL - 20, .95, rotate=10, moveTo={"x": 910, "y": WL + 150, "dur": T.dur, "t0": 0}, bob=1), sea_front(),
             cap("sank in *minutes*", T.w(0, "minutes"), y=980, size=44)])

@shot(["Twenty men.", "Three small boats.", "Thousands of kilometres from land."])
def _(T):
    return ({"depth": .5, "sun": {"x": 960, "y": -80, "r": 420}, "surface": True}, {"zoomFrom": 1, "zoomTo": 1.08, "x": 960, "y": 200},
            [boat(800, 34, .25, swim={"vx": 4}), boat(960, 28, .25, swim={"vx": 4}, phase=2), boat(1120, 36, .25, swim={"vx": 4}, phase=4),
             {"type": "factstack", "x": 690, "y": 560, "w": 540, "size": 28, "gap": 84, "items": [
                 {"text": "20 men", "t0": T.p(0)},
                 {"text": "3 small boats", "t0": T.p(1)},
                 {"text": "Thousands of km", "t0": T.w(2, "Thousands"), "tone": "red"}]}])

@shot(["They ran out of food.", "Then water."])
def _(T):
    return ({"mode": "black"}, {},
            [{"type": "bignumber", "from": 1, "to": 60, "prefix": "DAY ", "x": CX, "y": 470, "size": 110, "color": "#e9eef2", "dur": T.dur, "t0": 0},
             {"type": "factstack", "x": 720, "y": 590, "w": 480, "size": 28, "gap": 84, "items": [
                 {"text": "Food · gone", "t0": T.w(0, "food")},
                 {"text": "Water · gone", "t0": T.p(1) + .1, "tone": "red"}]}])

@shot(["Ninety days later, only eight were still alive."])
def _(T):
    return ({"depth": .55, "rays": False}, {},
            [{"type": "bignumber", "from": 20, "to": 8, "x": CX, "y": 600, "size": 260, "t0": T.w(0, "eight") - .5, "dur": 1.0},
             {"type": "pill", "text": "Out of 20 men", "x": 770, "y": 690, "t0": T.w(0, "Ninety"), "size": 28},
             cap("*survived*", T.w(0, "alive"), y=880, size=54)])

@shot(["Their story became Moby-Dick."], chapter=True)
def _(T):
    return ({"mode": "paper"}, {"zoomFrom": 1, "zoomTo": 1.08},
            [{"type": "doccard", "x": CX, "y": 520, "w": 540, "h": 680, "rotate": 2, "header": "1851 · Herman Melville",
              "title": "Moby-Dick\nor, the whale", "footer": "A novel", "t0": 0},
             {"type": "stamp", "text": "True story", "x": CX, "y": 900, "size": 50, "color": "#3ecf6a", "t0": T.w(0, "Moby")}])

@shot(["And no one knows why the whale attacked."], chapter=True, tail=2.2)
def _(T):
    return ({"depth": .95, "rays": False, "spotlight": {"x": 960, "w": 300}}, {"zoomFrom": 1, "zoomTo": 1.1},
            [whale(1120, 620, 1.0, sil=True, flip=True, swim={"vx": -40}),
             cap("!no one knows why!", T.w(0, "knows"), y=900, size=40),
             {"type": "stamp", "text": "Never explained", "x": CX, "y": 300, "size": 42, "t0": T.p(0) + T.d(0) + .4}])

build(st, sys.argv[1], sys.argv[2], voice="am_michael", lang="en-us", speed=.98, width=1080, height=1920,
      gaps=(.3, .6, .22), lead=.3)
