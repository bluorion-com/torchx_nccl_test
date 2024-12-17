# Setup
```
./setup.sh
```

# Run test
```
export NUM_GPUS=120  # 15 * 8

torchx run \
  --workspace="" \
  --scheduler kubernetes dist.ddp \
  --script ddp_allreduce.py \
  -j ${NUM_GPUS}x1 \
  --gpu 1 \
  --image gueraf/torchx_tmp@sha256:97b43bf0ad698d9ed8ea680674aa4f730439a27e28c5bdf3add4fb793138d4d6
```

# Determine size of pool
```
kubectl get nodes --selector='ray-gpu-status=volcano' | wc -l
```
