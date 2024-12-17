# Setup
```
git clone https://github.com/bluorion-com/torchx_nccl_test.git && torchx_nccl_test
./setup.sh
```

# Run test
```
export NUM_GPUS=112  # 14 * 8

torchx run \
  --workspace="" \
  --scheduler kubernetes dist.ddp \
  --script ddp_allreduce.py \
  -j ${NUM_GPUS}x1 \
  --gpu 1 \
  --image gueraf/torchx_tmp@sha256:97b43bf0ad698d9ed8ea680674aa4f730439a27e28c5bdf3add4fb793138d4d6

kubectl get jobs.batch.volcano.sh --sort-by=.metadata.creationTimestamp | tail -n 1
```

# Debug scheduling issues
```
kubectl get pods -o wide \
  | grep ddpallreduce \
  | grep Running \
  | grep -oP "th03[^\s]+" \
  | sort | uniq -c | sort -nr

```

# Cleanup
```
kubectl get jobs.batch.volcano.sh \
  | grep -oP "ddp[^\s]+" \
  | xargs kubectl delete jobs.batch.volcano.sh

```

# Determine size of pool
```
kubectl get nodes --selector='ray-gpu-status=volcano' | wc -l
```
