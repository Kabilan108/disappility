import assemblyai as aai
import sounddevice  # noqa: F401
import httpx

from enum import Enum
import warnings
import sys
import re
import os

warnings.filterwarnings("ignore")

PTN = re.compile("([h]?an[n]?a)(.*?)(thank(?:s| you))")

aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")
DON_API_URL = os.getenv("DON_API_URL")

BUFFER = ""
LAST_COMMAND = ""
MIC_SAMPLE_RATE = 44_100
# MIC_SAMPLE_RATE = 16_000


class msg(str, Enum):
    READY = "[READY]"
    USERSAYS = "[USERSAYS]"
    STOP = "[STOP]"


def get_cmd(transcript: str) -> str:
    global PTN

    cmd = re.sub("[.,;:!?]", " ", transcript).strip()
    match = PTN.search(cmd)
    # match = PTN.search(transcript)

    if match:
        match = [x.strip() for x in match.groups()]
        return match[1]
    else:
        return None


def on_open(session_opened: aai.RealtimeSessionOpened):
    "This function is called when the connection has been established."
    global BUFFER


def on_data(transcript: aai.RealtimeTranscript):
    "This function is called when a new transcript has been received."
    global BUFFER, PTN, LAST_COMMAND

    if not transcript.text:
        return

    if len(BUFFER) == 0:
        i = 0
    else:
        for i, c in enumerate(BUFFER):
            if c != transcript.text[i]:
                BUFFER = BUFFER[:i]
                break
    BUFFER += " " + transcript.text.lower()[i:]

    match = PTN.search(BUFFER)
    if match:
        cmd = get_cmd(BUFFER)
        BUFFER = ""

        if cmd != LAST_COMMAND.strip():
            json_data = {"prompt": cmd}
            response = httpx.post(f"http://{DON_API_URL}/oiprocessor", json=json_data)
            print(response.json())

            # print(f"{msg.USERSAYS.value} {cmd}", flush=True)

        LAST_COMMAND = cmd


def on_error(error: aai.RealtimeError):
    "This function is called when the connection has been closed."
    print("An error occured:", error, file=sys.stderr, flush=True)


def on_close():
    "This function is called when the connection has been closed."
    global BUFFER
    print(BUFFER)
    print(msg.STOP.value, flush=True)


if __name__ == "__main__":
    transcriber = aai.RealtimeTranscriber(
        on_data=on_data,
        on_error=on_error,
        sample_rate=MIC_SAMPLE_RATE,
        on_open=on_open,  # optional
        on_close=on_close,  # optional
    )

    print(msg.READY.value, flush=True)

    transcriber.connect()
    microphone_stream = aai.extras.MicrophoneStream()
    transcriber.stream(microphone_stream)
    transcriber.close()
