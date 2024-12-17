# Setup

```
pipx install torchx[kubernetes]

echo "[kubernetes]" > ~/.torchxconfig
echo "queue=default" >> ~/.torchxconfig
echo "namespace=user-ns" >> ~/.torchxconfig
echo "image_repo=docker.io/gueraf/torchx_tmp" >> ~/.torchxconfig
```

# Test
```
git clone https://github.com/bluorion-com/torchx_nccl_test.git && torchx_nccl_test

# TODO: Write test script.

torchx run --workspace="" --scheduler kubernetes utils.echo --image gueraf/torchx_tmp --msg hello
```
