import argparse
import os
import socket
import time

import torch
import torch.distributed as dist


def parse_args():
    parser = argparse.ArgumentParser(description="DDP AllReduce Example")
    parser.add_argument("--num_integers", type=int, default=1, help="Number of integers to reduce")
    parser.add_argument(
        "--environment_variables_csv",
        type=str,
        default="NCCL_DEBUG=INFO,NCCL_NET=IB",
        help="Environment variables FOO=BAR,BAZ=BOO",
    )
    parser.add_argument(
        "--do_work",
        type=bool,
        default=True,
        help="Whether to do work.",
    )
    parser.add_argument(
        "--sleep_forever",
        type=bool,
        default=False,
        help="Sleep forever after all_reduce",
    )
    parser.add_argument(
        "--print_info_only",
        type=bool,
        default=False,
        help="Print info only",
    )
    args = parser.parse_args()
    return args


def print_info(args):
    print(f"environment_variables_csv: {args.environment_variables_csv}", flush=True)
    if len(args.environment_variables_csv) > 0:
        for env_var in args.environment_variables_csv.split(","):
            key, value = env_var.split("=")
            os.environ[key] = value

    print(f"MASTER_PORT: {os.environ.get("MASTER_PORT", "Not Set")}", flush=True)
    print(f"MASTER_ADDR: {os.environ.get("MASTER_ADDR", "Not Set")}", flush=True)
    print(f"WORLD_SIZE: {os.environ.get("WORLD_SIZE", "Not Set")}", flush=True)
    print(f"RANK: {os.environ.get("RANK", "Not Set")}", flush=True)

    assert torch.cuda.is_available(), "CUDA is not available"
    assert torch.cuda.device_count() == 1, f"Expected 1 GPU, but got {torch.cuda.device_count()}"
    gpu_serial_number = torch.cuda.get_device_properties(0).uuid
    print(f"GPU Serial Number: {gpu_serial_number}", flush=True)


def init_process_group():
    print("Initializing process group", flush=True)
    dist.init_process_group(backend="nccl")
    print(
        f"Worker {dist.get_rank()} of {dist.get_world_size()} started on {socket.gethostname()}!",
        flush=True,
    )


def destroy_process_group():
    dist.destroy_process_group()
    print("Process group destroyed", flush=True)


def do_work(args):
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
    print(f"all_reduce output = {a}", flush=True)
    assert a == dist.get_world_size(), f"Expected {dist.get_world_size()} but got {a}"


def sleep_forever():
    print("Sleeping forever...", flush=True)
    while True:
        time.sleep(1)


def main():
    args = parse_args()
    print_info(args)

    if not args.print_info_only:
        init_process_group()
        if args.do_work:
            do_work(args)
        destroy_process_group()

    if args.sleep_forever:
        sleep_forever()


if __name__ == "__main__":
    main()
