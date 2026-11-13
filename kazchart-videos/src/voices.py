import sys, os, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
tts, out = sys.argv[1], sys.argv[2]
k = Kokoro(os.path.join(tts, "kokoro.onnx"), os.path.join(tts, "voices.bin"))
nums = "one two three four five six seven eight".split()
V = [("bm_george","en-gb"),("bm_lewis","en-gb"),("bm_daniel","en-gb"),("am_michael","en-us"),("am_onyx","en-us"),("am_fenrir","en-us"),("bf_emma","en-gb"),("af_heart","en-us")]
parts = []
for i, (v, lang) in enumerate(V):
    a, sr = k.create(f"Voice {nums[i]}. In eighteen twenty, a whale did something no one believed was possible.", voice=v, speed=.94, lang=lang)
    parts += [a.astype(np.float32), np.zeros(int(.9 * sr), np.float32)]
    print(i + 1, v)
sf.write(os.path.join(out, "voice-samples.wav"), np.concatenate(parts), sr)
