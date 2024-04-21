# disappility

## setup

### python environment setup

install uv

```shell
# linux, mac
curl -LsSf https://astral.sh/uv/install.sh | sh

# windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

run this from the top leve `aiccessible` folder

```shell
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

copy .env.template to .env and replace `PYTHON_PATH` with the output from `which python`

### piper (text-to-speech)

run the following:

```shell
./workers/piper/download-model.sh
```

### electron

```shell
npm install
npm run electron
```
