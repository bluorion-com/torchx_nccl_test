# Setup

```
./setup.sh
```

# Run test
```
export NUM_GPUS=16

torchx run \
  --workspace="" \
  --scheduler kubernetes dist.ddp \
  --script ddp_allreduce.py \
  -j ${NUM_GPUS}x1 \
  --gpu 1 \
  --image gueraf/torchx_tmp@sha256:41bd45c736b6da020464b0fcc5b8b9b6c621f05688e6f1652456fd438a96d856
```

# Determine size of pool
```
kubectl get nodes --selector='ray-gpu-status=volcano' | wc -l
```