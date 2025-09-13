from __future__ import annotations

import io
from typing import BinaryIO, Optional, Union

from openai import OpenAI


_client: Optional[OpenAI] = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI()
    return _client


def transcribe_file_like(file_obj: Union[BinaryIO, any], *, response_format: str = "json", prompt: str | None = None) -> str:
    """Transcribe an audio file-like object using OpenAI gpt-4o-transcribe.

    Parameters
    ----------
    file_obj: Union[BinaryIO, any]
        An open, binary file-like object or Django uploaded file.
    response_format: str
        Either "json" or "text" supported by gpt-4o-transcribe.
    prompt: Optional[str]
        Optional prompt to steer the transcription.

    Returns
    -------
    str
        The transcription text.
    """

    client = _get_client()
    
    # Handle Django uploaded files by reading content and creating BytesIO
    if hasattr(file_obj, 'read') and hasattr(file_obj, 'name'):
        # This is likely a Django uploaded file
        if hasattr(file_obj, 'seek'):
            try:
                file_obj.seek(0)
            except Exception:
                pass
        
        # Read the content and create a BytesIO object with a name
        content = file_obj.read()
        file_name = getattr(file_obj, 'name', 'audio.webm')
        
        # Create a BytesIO object and set a name attribute for OpenAI
        bio = io.BytesIO(content)
        bio.name = file_name
        actual_file = bio
    else:
        # Regular file-like object
        actual_file = file_obj

    kwargs: dict = {
        "model": "gpt-4o-transcribe",
        "file": actual_file,
    }
    if response_format in {"json", "text"}:
        kwargs["response_format"] = response_format
    if prompt:
        kwargs["prompt"] = prompt

    result = client.audio.transcriptions.create(**kwargs)

    # SDK returns an object with `.text` even for text response_format
    return getattr(result, "text", "") or ""