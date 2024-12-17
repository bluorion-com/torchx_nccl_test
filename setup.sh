pipx install torchx[kubernetes]

echo "[kubernetes]" > ~/.torchxconfig
echo "queue=default" >> ~/.torchxconfig
echo "namespace=user-ns" >> ~/.torchxconfig
echo "image_repo=docker.io/gueraf/torchx_tmp" >> ~/.torchxconfig
