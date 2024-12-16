# Setup

```
pipx install torchx[kubernetes]

echo "[kubernetes]" > ~/.torchxconfig
echo "queue=torchx" >> ~/.torchxconfig
echo "namespace=user-ns" >> ~/.torchxconfig
echo "image_repo=docker.io" >> ~/.torchxconfig
```

# Test
```
git clone https://github.com/bluorion-com/torchx_nccl_test.git && torchx_nccl_test

# TODO: Write test script.

torchx run --scheduler kubernetes utils.echo --image pytorch/pytorch:2.5.1-cuda12.4-cudnn9-devel --msg hello

```
