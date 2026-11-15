# freeimagetovideo-haystack

Free image to video AI with no daily cap: start with no sign-up, keep going on a free account. Every video comes with sound and no watermark. This is the Haystack integration for [Free Image to Video](https://freeimagetovideo.ai/?utm_source=pypi-haystack&utm_medium=package).

Turn a prompt into a video clip ([free text to video AI](https://freeimagetovideo.ai/video/free-text-to-video-ai)), or [animate a photo](https://freeimagetovideo.ai/video/animate-photo-ai) as the first frame ([image to video AI with sound](https://freeimagetovideo.ai/video/image-to-video-ai-with-sound)), inside a Haystack pipeline.

## Install

```bash
pip install freeimagetovideo-haystack
```

## API key

Create a key at [freeimagetovideo.ai/settings/apikeys](https://freeimagetovideo.ai/settings/apikeys) and export it:

```bash
export FREEIMAGETOVIDEO_API_KEY=sk-...
```

API runs draw on your plan's daily full-speed allowance, then wait in the relaxed queue ([pricing](https://freeimagetovideo.ai/pricing)).

## Usage

```python
from freeimagetovideo_haystack import FreeImageToVideoGenerator

gen = FreeImageToVideoGenerator(duration=6, resolution="480p", aspect_ratio="16:9")

# Text to video
clip = gen.run(prompt="a paper lantern drifting over a night river")["videos"][0]

# Image to video
moved = gen.run(
    prompt="the camera slowly orbits the statue",
    image_url="https://example.com/statue.jpg",
)["videos"][0]
```
