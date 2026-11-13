# KazChart videos

Source files for the videos made with the KazChart skill (`.claude/skills/kazchart-skill`). The rendered MP4s aren't stored here because they're too large; these files rebuild them.

| Folder | Video | Format | Voice |
|---|---|---|---|
| `essex/` | The Whale That Hunted a Ship (1820) | 16:9, 2:17 | bm_george |
| `essex-short/` | Essex Short | 9:16, 0:33 | am_michael |
| `indianapolis/` | USS Indianapolis (1945) | 16:9, 1:53 | am_michael |

Each folder has `scene.json` (what the engine renders), `script.txt` (the narration) and `upload-notes.md` (titles, description, chapters and a fact list). `essex/` also has the thumbnail and its scene (`thumb.json`).

## Rebuild a video
Needs Node + Playwright + ffmpeg (see the skill's SKILL.md), plus `pip install kokoro-onnx soundfile` and the Kokoro model files `kokoro-v1.0.int8.onnx` (saved as `kokoro.onnx`) and `voices-v1.0.bin` (saved as `voices.bin`) from the kokoro-onnx GitHub releases, in a folder `TTS`.

```bash
cd kazchart-videos/src
python3 indy.py TTS out/indy        # voiceover + scene.json + timeline.json
python3 mix.py out/indy             # drone + impact hits mixed under the voice -> mix.wav
node ../../.claude/skills/kazchart-skill/scripts/render.mjs out/indy/scene.json out/indy/video.mp4 --audio out/indy/mix.wav
```

`essex.py` is the original standalone build of the long Essex video. `short_essex.py` and `indy.py` use the shared helpers in `kzlib.py`: ship, cruiser, submarine, whaleboat and swimmer art, Kokoro voiceover timing and scene output. To try another voice, change `voice=` in the `build(...)` call (`python3 voices.py TTS .` writes a sample reel of eight voices). `still.mjs` renders one frame to PNG, which is how the thumbnail was made.
