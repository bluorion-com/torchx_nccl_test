import torch
import socket
import argparse
import torch.distributed as dist

parser = argparse.ArgumentParser(description="DDP AllReduce Example")
parser.add_argument("--num_integers", type=int, default=1, help="Number of integers to reduce")
args = parser.parse_args()

assert torch.cuda.is_available(), "CUDA is not available"

dist.init_process_group(backend="nccl")
print(f"Worker {dist.get_rank()} of {dist.get_world_size()} started on {socket.gethostname()}!")

a = torch.ones([args.num_integers], dtype=torch.int32, device="cuda")
dist.all_reduce(a, op=dist.ReduceOp.SUM)
a = a[0].item()
print(f"all_reduce output = {a}")
assert a == dist.get_world_size(), f"Expected {dist.get_world_size()} but got {a}"
