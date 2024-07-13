# celery_ml_deploy


## Sources
Some parts of the code are copied as is from https://huggingface.co/microsoft/Florence-2-base-ft/tree/main

This is done to solve a bug of `transformers` where the code cannot run without a GPU due to forceful import of `flash_attn` when the class definition is loaded with `trust_remote_code=True`.

## Local Env Setup

### CPU

```bash
pip install -r requirements.txt -extra-index-url https://download.pytorch.org/whl/cpu
```

### GPU (TODO: add support for GPU inference)
Torch

```bash
conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia
```

```bash
pip install -r requirements.txt
```

## Docker

```bash
docker-compose up
```