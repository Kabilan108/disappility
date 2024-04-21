#!/bin/bash

# kathleen (low) - 16000 Hz
# MODEL_URL="https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/kathleen/low/en_US-kathleen-low.onnx"
# CONFIG_URL="https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/kathleen/low/en_US-kathleen-low.onnx.json"

# hfc-female (medium) - 22050 Hz
# MODEL_URL="https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/hfc_female/medium/en_US-hfc_female-medium.onnx"
# CONFIG_URL="https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/hfc_female/medium/en_US-hfc_female-medium.onnx.json"

# amy (medium) - 22050 Hz
MODEL_URL="https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/amy/medium/en_US-amy-medium.onnx"
CONFIG_URL="https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/amy/medium/en_US-amy-medium.onnx.json"

DEST="$(dirname "$0")/models"
mkdir -p "$DEST"

wget -P "$DEST" $MODEL_URL
wget -P "$DEST" $CONFIG_URL
