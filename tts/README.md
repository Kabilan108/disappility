# text-to-speech

make sure piper is installed in the conda environment

run [`download-model.sh`](./download-model.sh) to download the model files

run this:

```shell
echo 'j cole is a fuck nigger' | piper --model tts/en_US-kathleen-low.onnx --output_raw | aplay -r 16000 -f S16_LE -t raw -
```
