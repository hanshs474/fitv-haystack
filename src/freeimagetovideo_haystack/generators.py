"""Free Image to Video generation component for Haystack pipelines.

Free image to video AI with no daily cap: start with no sign-up, keep going on
a free account. Every video comes with sound and no watermark. Pass ``api_key``
(a Haystack ``Secret``) or set ``FREEIMAGETOVIDEO_API_KEY``. Create a key at
https://freeimagetovideo.ai/settings/apikeys.
"""

from typing import Any, Dict, List, Optional

import freeimagetovideo
from haystack import component, default_from_dict, default_to_dict
from haystack.utils import Secret, deserialize_secrets_inplace


def _opts(**kw: Any) -> Dict[str, Any]:
    return {k: v for k, v in kw.items() if v is not None}


@component
class FreeImageToVideoGenerator:
    """Generates a video clip with sound from a prompt or animates a photo.

    ``model`` defaults to ``minimax-h3``.
    """

    def __init__(
        self,
        model: str = freeimagetovideo.DEFAULT_MODEL,
        duration: Optional[int] = None,
        resolution: Optional[str] = None,
        aspect_ratio: Optional[str] = None,
        api_key: Secret = Secret.from_env_var("FREEIMAGETOVIDEO_API_KEY"),
        timeout: float = 1800.0,
    ):
        self.model = model
        self.duration = duration
        self.resolution = resolution
        self.aspect_ratio = aspect_ratio
        self.api_key = api_key
        self.timeout = timeout

    def to_dict(self) -> Dict[str, Any]:
        return default_to_dict(
            self,
            model=self.model,
            duration=self.duration,
            resolution=self.resolution,
            aspect_ratio=self.aspect_ratio,
            api_key=self.api_key.to_dict(),
            timeout=self.timeout,
        )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FreeImageToVideoGenerator":
        deserialize_secrets_inplace(data["init_parameters"], keys=["api_key"])
        return default_from_dict(cls, data)

    @component.output_types(videos=List[str])
    def run(self, prompt: str, image_url: Optional[str] = None) -> Dict[str, List[str]]:
        """Generate one video clip, or animate ``image_url`` as the first frame."""
        url = freeimagetovideo.generate_video(
            prompt,
            image_url=image_url,
            model=self.model,
            api_key=self.api_key.resolve_value(),
            timeout=self.timeout,
            **_opts(
                duration=self.duration,
                resolution=self.resolution,
                aspect_ratio=self.aspect_ratio,
            ),
        )
        return {"videos": [url]}
