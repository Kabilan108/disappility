from piper import PiperVoice
import sounddevice  # noqa: F401
import pyaudio

from pathlib import Path
from enum import Enum
import argparse
import sys


class msg(str, Enum):
    SPEAK = "[SPEAK]"
    STOP = "[STOP]"
    READY = "[READY]"


def play_audio_stream(audio_stream, sample_rate=22050):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=sample_rate, output=True)

    try:
        for audio_bytes in audio_stream:
            stream.write(audio_bytes)
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model",
        help="Path to the ONNX model file",
        required=True,
    )
    parser.add_argument(
        "--sample_rate",
        help="Sample rate to synthesize at",
        default=22050,
        type=int,
    )
    args = parser.parse_args()

    model = Path(args.model)
    if not model.exists():
        raise ValueError(f"Model file {model} does not exist")

    config = Path(args.model + ".json")
    if not config.exists():
        raise ValueError(f"Config file {config} does not exist")

    voice = PiperVoice.load(model, config_path=config, use_cuda=False)
    synthesizer_args = {"sentence_silence": 0.0}

    print(msg.READY.value)

    try:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            if line == msg.STOP:
                break
            if line.startswith(msg.SPEAK):
                line = line[len(msg.SPEAK) :].strip()
                audio_stream = voice.synthesize_stream_raw(line, **synthesizer_args)
                play_audio_stream(audio_stream, sample_rate=args.sample_rate)
                continue
    except (KeyboardInterrupt, EOFError):
        return
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
