from typing import Any
from uuid import uuid4
import logging
import json

from google.cloud import texttospeech, storage

from django.conf import settings
from langchain.tools import BaseTool


logger = logging.getLogger(__name__)


class TextToSpeechTool(BaseTool):
    name="tts"
    description="This tool grants you the ability to express yourself using voice. Use this tool if user wants you to send a voice message."
    return_direct = True
    handle_tool_error = True
    
    voice_name: str

    def __init__(self, voice_name: str, **data: Any) -> None:
        super().__init__(voice_name=voice_name, **data)

    def _run(self, query: str, *args: Any, **kwargs: Any) -> str:
        return self.get_voice(query)
    
    def _arun(self, *args: Any, **kwargs: Any):
        raise NotImplemented()

    def get_voice(self, input: str) -> str:
        tts_client = texttospeech.TextToSpeechClient(client_options={
            "api_key": settings.GCLOUD_API_KEY,
        })

        # Set the text input to be synthesized
        synthesis_input = texttospeech.SynthesisInput(text=input)

        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US", name=self.voice_name
        )

        # Select the type of audio file you want returned
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.OGG_OPUS
        )

        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        response = tts_client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )


        storage_client = storage.Client(client_options={
            "api_key": settings.GCLOUD_API_KEY
        })
        bucket = storage_client.bucket("voice-msg")
        blob = bucket.blob(str(uuid4()))

        blob.upload_from_string(response.audio_content, content_type="audio/ogg")

        return json.dumps({
            "audio_url": blob.public_url,
            "audio_text": input
        })

