from collections.abc import Generator
from uuid import uuid4
from typing import BinaryIO
from pathlib import Path
from pydub import AudioSegment
import contextlib
import tempfile
import requests
import magic
import mimetypes
import openai

WHISPER_SUPPORTED_FORMATS = {'.mp3', '.mp4', '.mpeg', '.mpga', '.m4a', '.wav', '.webm'}


def transcribe_audio(*, file_path: str | Path = None, file: BinaryIO = None) -> str:
    """Given a path of a audio file stored on file system, or the file itself opened in binary mode,
    the function transcribes the audio and returns the text.
    If file type is not one of :data:`WHISPER_SUPPORTED_FORMATS`
    the function will try to convert it to `.wav` and proceed further.

    Args:
        file_path (str | Path): Path of file to be transcribed. Defaults to None.
        file (BinaryIO, optional): File object to be transctibed. Defaults to None.

    Raises:
        ValueError: No parameters passed.

    Returns:
        str: Transcribed text.
    """

    
    
    converted_file_path = None

    if file:
        mime_type = magic.from_buffer(file.read(2048), mime=True)
        file.seek(0)

        formats = mimetypes.guess_all_extensions(mime_type)

        if not set(formats) & WHISPER_SUPPORTED_FORMATS:
            converted: AudioSegment = AudioSegment.from_file_using_temporary_files(file)
            converted_file_path = Path(uuid4().hex).with_suffix(".wav")
            converted.export(converted_file_path, format="wav")
        
        if converted_file_path:
            with converted_file_path.open("rb") as audio:
                results = openai.Audio.transcribe("whisper-1", audio)

            if converted_file_path:
                converted_file_path.unlink(missing_ok=True)
        else:
            results = openai.Audio.transcribe("whisper-1", file)
        
        return results["text"]
    
    elif file_path:
        file_path = Path(file_path)

        if file_path.suffix not in WHISPER_SUPPORTED_FORMATS:
            converted: AudioSegment = AudioSegment.from_file_using_temporary_files(file_path)
            
            converted_file_path = file_path.with_suffix(".wav")
            converted.export(converted_file_path, format="wav")


        with (converted_file_path or file_path).open("rb") as audio:
            results = openai.Audio.transcribe("whisper-1", audio)

        if converted_file_path:
            converted_file_path.unlink(missing_ok=True)
        
        return results["text"]
    
    raise ValueError("Function expected either `file_path` or `file` but got none.")


@contextlib.contextmanager
def audio_file_from_url(url: str) -> Generator[tempfile._TemporaryFileWrapper, None, None]:
    """Temorarily stored the file downloaded from given url to filesystem
    This function is wrapped in :decorator:`@contextlib.contextmanager` and should be used like this:
    ```
        with audio_file_from_url("https://www.example.com") as audio_file:
            pass # do something with the file
    ```

    File will be deleted afterwards.

    Args:
        url (str): Url of the file to be downloaded

    Yields:
        Generator[tempfile._TemporaryFileWrapper, None, None]: Temporary stored file.
    """
    with requests.get(url, stream=True) as r:
        r.raise_for_status()

        with tempfile.NamedTemporaryFile() as tmp_file:
            for chunk in r.iter_content(8192):
                tmp_file.write(chunk)
            
            tmp_file.seek(0)
            yield tmp_file