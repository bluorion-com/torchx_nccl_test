import torch
import socket
import torch.distributed as dist

dist.init_process_group(backend="nccl")
print(f"Worker {dist.get_rank()} of {dist.get_world_size()} started on {socket.gethostname()}!")

a = torch.ones([1], dtype=torch.int32)
x = dist.all_reduce(a, op=dist.ReduceOp.SUM)
print(f"all_reduce output = {x}")
assert x == dist.get_world_size(), f"Expected {dist.get_world_size()} but got {x}"

