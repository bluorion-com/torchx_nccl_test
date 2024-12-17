# Setup
```
git clone https://github.com/bluorion-com/torchx_nccl_test.git && torchx_nccl_test
./setup.sh
```

# Run test
```
export NUM_GPUS=72  # 9 * 8

torchx run \
  --workspace="" \
  --scheduler kubernetes dist.ddp \
  -j ${NUM_GPUS}x1 \
  --gpu 1 \
  --image gueraf/torchx_tmp@sha256:30f4479d05dac7a93bdf2a350b147f08df4df66c78470b702ab985e9e0901b31 \
  --script ddp_allreduce.py \
  -- \
  --num_integers 1000000

kubectl get jobs.batch.volcano.sh --sort-by=.metadata.creationTimestamp | tail -n 1
```

# Restart scheduler (after re-tagging)
```
kubectl get pods \
  | grep volcano \
  | grep scheduler \
  | grep -oP "^[^\s]+" \
  | xargs kubectl delete pod
```

# Re-label nodes
```
kubectl get nodes --selector='ray-gpu-status=gpu-hospital' \
  | grep -oP "th03[^\s]+" \
  | xargs -I % kubectl label node % ray-gpu-status=volcano --overwrite
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

kubectl get pods \
  | grep -oP "ddp[^\s]+" \
  | xargs kubectl delete pod

```

# Determine size of pool
```
kubectl get nodes --selector='ray-gpu-status=volcano' \
  | grep Ready \
  | wc -l

```
