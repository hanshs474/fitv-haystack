import json
from unittest import mock

import freeimagetovideo
import pytest
from haystack.utils import Secret
from freeimagetovideo_haystack import FreeImageToVideoGenerator


def test_text_to_video_and_roundtrip(monkeypatch):
    monkeypatch.setenv("FREEIMAGETOVIDEO_API_KEY", "sk-env")
    gen = FreeImageToVideoGenerator(duration=6, resolution="480p")
    gen2 = FreeImageToVideoGenerator.from_dict(gen.to_dict())
    with mock.patch.object(
        freeimagetovideo,
        "generate_video",
        return_value="https://cdn.freeimagetovideo.ai/v.mp4",
    ) as g:
        out = gen2.run(prompt="a paper lantern", image_url="https://example.com/a.jpg")
    assert out == {"videos": ["https://cdn.freeimagetovideo.ai/v.mp4"]}
    assert g.call_args.args[0] == "a paper lantern"
    assert g.call_args.kwargs["image_url"] == "https://example.com/a.jpg"
    assert g.call_args.kwargs["model"] == "minimax-h3"
    assert g.call_args.kwargs["api_key"] == "sk-env"
    assert g.call_args.kwargs["duration"] == 6
    assert g.call_args.kwargs["resolution"] == "480p"
    assert "aspect_ratio" not in g.call_args.kwargs


def test_auth_error_propagates():
    def transport(url, payload, headers):
        return 401, json.dumps({"code": -1, "message": "Invalid API key"}).encode("utf-8")

    real = freeimagetovideo.generate_video
    with mock.patch.object(
        freeimagetovideo,
        "generate_video",
        side_effect=lambda *a, **k: real(*a, transport=transport, **k),
    ):
        with pytest.raises(freeimagetovideo.AuthError):
            FreeImageToVideoGenerator(api_key=Secret.from_token("sk-bad")).run(prompt="x")
