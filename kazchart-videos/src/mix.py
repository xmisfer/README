"""Make drone bed + impact hits and mix them under vo.wav. Usage: python3 -I mix.py <out_dir>"""
import json, os, subprocess, sys
out = sys.argv[1]; os.chdir(out)
tl = json.load(open("timeline.json")); D = tl["duration"]
ff = lambda *a: subprocess.run(["ffmpeg", "-y", "-v", "error", *a], check=True)
ff("-f", "lavfi", "-i", "aevalsrc='0.22*sin(2*PI*55*t)*(0.6+0.4*sin(2*PI*0.07*t))+0.15*sin(2*PI*82.41*t)*(0.6+0.4*sin(2*PI*0.05*t+1))"
   f"+0.07*sin(2*PI*110*t+2*sin(2*PI*0.3*t))+0.04*sin(2*PI*164.8*t)*(0.5+0.5*sin(2*PI*0.031*t)):s=48000:d={D}'",
   "-f", "lavfi", "-i", f"anoisesrc=color=brown:amplitude=0.25:d={D}:r=48000",
   "-filter_complex", f"[1]lowpass=f=300,volume=0.6[n];[0][n]amix=inputs=2:normalize=0,lowpass=f=900,afade=t=in:d=3,afade=t=out:st={max(0, D - 4)}:d=4[a]",
   "-map", "[a]", "-ac", "2", "drone.wav")
ff("-f", "lavfi", "-i", "aevalsrc='0.95*sin(2*PI*(38+70*exp(-9*t))*t)*exp(-3.5*t)+0.25*(random(0)-0.5)*exp(-18*t):s=48000:d=1.6'",
   "-af", "lowpass=f=1200", "-ac", "2", "thud.wav")
ins = ["-i", "vo.wav", "-i", "drone.wav"]
filt = ["[0]aresample=48000,pan=stereo|c0=c0|c1=c0[vo]", "[1]volume=0.55[dr]"]; labels = ["[vo]", "[dr]"]
hits = [(t, 1.0) for t in tl["thuds"]] + [(t, .35) for t in tl["stamps"] if all(abs(t - h) > .3 for h in tl["thuds"])]
for i, (t, v) in enumerate(hits):
    ins += ["-i", "thud.wav"]; ms = int(max(0, t) * 1000)
    filt.append(f"[{i + 2}]adelay={ms}|{ms},volume={v}[h{i}]"); labels.append(f"[h{i}]")
filt.append("".join(labels) + f"amix=inputs={len(labels)}:normalize=0:duration=first,alimiter=limit=0.95[a]")
ff(*ins, "-filter_complex", ";".join(filt), "-map", "[a]", "mix.wav")
print("mixed", len(hits), "hits,", D, "s")
