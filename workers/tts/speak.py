from openai import OpenAI
import pygame

from pathlib import Path
from enum import Enum
import argparse
import tempfile
import warnings
import sys
import os

warnings.filterwarnings("ignore")

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)


class msg(str, Enum):
    SPEAK = "[SPEAK]"
    STOP = "[STOP]"
    READY = "[READY]"


def get_tempfile(suffix: str = ".mp3") -> Path:
    return Path(tempfile.mktemp(suffix=suffix))


def create_speech_file(prompt: str, model: str) -> Path:
    speech_file = get_tempfile()
    response = client.audio.speech.create(model=model, voice="alloy", input=prompt)
    response.stream_to_file(speech_file)
    return speech_file


def play_audio(file_path: str):
    try:
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except pygame.error:
        print("Error: Unable to load or play the MP3 file")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model",
        help="OpenAI TTS model to use.",
        default="tts-1",
    )
    args = parser.parse_args()

    if OPENAI_API_KEY is None:
        raise ValueError("OPENAI_API_KEY environment variable not set")

    pygame.init()
    sys.stdout.flush()

    print(msg.READY.value)
    sys.stdout.flush()

    try:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            if line == msg.STOP:
                break
            if line.startswith(msg.SPEAK):
                line = line[len(msg.SPEAK) :].strip()
                audio_stream = create_speech_file(line, args.model)
                play_audio(audio_stream)
                continue
    except (KeyboardInterrupt, EOFError):
        pygame.quit()
        return
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    pygame.quit()


if __name__ == "__main__":
    main()
