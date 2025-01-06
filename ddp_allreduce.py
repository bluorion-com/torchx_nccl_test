import argparse
import socket
import time

import torch
import torch.distributed as dist

parser = argparse.ArgumentParser(description="DDP AllReduce Example")
parser.add_argument("--num_integers", type=int, default=1, help="Number of integers to reduce")
args = parser.parse_args()

assert torch.cuda.is_available(), "CUDA is not available"
assert torch.cuda.device_count() == 1, f"Expected 1 GPU, but got {torch.cuda.device_count()}"
gpu_serial_number = torch.cuda.get_device_properties(0).uuid
print(f"GPU Serial Number: {gpu_serial_number}")

dist.init_process_group(backend="nccl")
print(f"Worker {dist.get_rank()} of {dist.get_world_size()} started on {socket.gethostname()}!")

a = torch.ones([args.num_integers], dtype=torch.int32, device="cuda")
dist.barrier()
start_time = time.time()
dist.all_reduce(a, op=dist.ReduceOp.SUM)
end_time = time.time()
runtime = end_time - start_time

print(
    f"all_reduce took {runtime} seconds for {args.num_integers} integers, {4 * args.num_integers / 1024.0**3 / runtime} GB/s"
)

a = a[0].item()
print(f"all_reduce output = {a}")
assert a == dist.get_world_size(), f"Expected {dist.get_world_size()} but got {a}"
dist.destroy_process_group()
