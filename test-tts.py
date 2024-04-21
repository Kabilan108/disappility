from TTS.api import TTS
import numpy as np
import pyaudio

# device = "cuda" if torch.cuda.is_available() else "cpu"
device = "cpu"

tts = TTS("tts_models/en/ljspeech/glow-tts").to(device)

text = """
Six fucking devils stepped up playing brave, God.
Had the fucking nerve to try and enter my grave yard.
I'm the Rzarector, be my sacrifice.
Commit suicide and I'll bring you back to life.
"""

wav = tts.tts(text=text)
wav = np.int16(np.array(wav) * 32767)
wav_bytes = wav.tobytes()

# Parameters
sample_rate = 22050  # or whatever your rate is
channels = 1  # mono; set to 2 for stereo
format = pyaudio.paInt16  # depends on the format of your WAV file

# Initialize PyAudio object
p = pyaudio.PyAudio()

# Open stream
stream = p.open(format=format, channels=channels, rate=sample_rate, output=True)

stream.write(wav_bytes)

stream.close()
