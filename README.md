# Torch job
## Setup
```
git clone https://github.com/bluorion-com/torchx_nccl_test.git && torchx_nccl_test
```

## Run test
```
# edit pytorch_volcano_job.yaml
kubectl delete -f pytorch_volcano_job.yaml ; kubectl apply -f pytorch_volcano_job.yaml
```

## Re-label nodes
```
kubectl get nodes --selector='ray-gpu-status=gpu-hospital' \
  | grep -oP "th03[^\s]+" \
  | xargs -I % kubectl label node % ray-gpu-status=volcano --overwrite
```

## Determine size of pool
```
kubectl get nodes --selector='ray-gpu-status=volcano' \
  | grep Ready \
  | wc -l

```

# Mellanox RDMA test
```
POD=pytorch-job-master-0
kubectl exec --stdin --tty $POD --container rdma-test -- /bin/bash
./start_server.sh
```

```
POD=pytorch-job-worker-0
kubectl exec --stdin --tty $POD --container rdma-test -- /bin/bash
./start_client.sh pytorch-job-master-0.pytorch-job
```

# Old (torchx) notes

## Run test
```
export NUM_GPUS=2

torchx run \
  --workspace="" \
  --scheduler kubernetes dist.ddp \
  -j ${NUM_GPUS}x1 \
  -h gpu.small \
  --gpu 1 \
  --image gueraf/torchx_tmp@sha256:6204d3df23fad2534b04c7f9cb525ce098f304d3559ff6218474ba9396d3e7d7 \
  --script ddp_allreduce.py \
  -- \
  --num_integers 1000000 \
  --environment_variables_csv="NCCL_DEBUG=INFO,NCCL_NET=IB" \
  --sleep_forever=True

kubectl get jobs.batch.volcano.sh --sort-by=.metadata.creationTimestamp | tail -n 1
```

## Restart scheduler (after re-tagging)
```
kubectl get pods \
  | grep volcano \
  | grep scheduler \
  | grep -oP "^[^\s]+" \
  | xargs kubectl delete pod
```
## Debug scheduling issues
```
kubectl get pods -o wide \
  | grep ddpallreduce \
  | grep Running \
  | grep -oP "th03[^\s]+" \
  | sort | uniq -c | sort -nr

```

## Cleanup
```
kubectl get jobs.batch.volcano.sh \
  | grep -oP "ddp[^\s]+" \
  | xargs kubectl delete jobs.batch.volcano.sh

kubectl get pods \
  | grep -oP "ddp[^\s]+" \
  | xargs kubectl delete pod

```
