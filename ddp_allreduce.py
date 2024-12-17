import torch
import socket
import torch.distributed as dist

assert torch.cuda.is_available(), "CUDA is not available"

dist.init_process_group(backend="nccl")
print(f"Worker {dist.get_rank()} of {dist.get_world_size()} started on {socket.gethostname()}!")

a = torch.ones([1], dtype=torch.int32, device="cuda")
x = dist.all_reduce(a, op=dist.ReduceOp.SUM)
print(f"all_reduce output = {x}")
assert x == dist.get_world_size(), f"Expected {dist.get_world_size()} but got {x}"

