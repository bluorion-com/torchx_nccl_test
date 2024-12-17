FROM docker.io/rayproject/ray:2.38.0-py312-cu123

RUN sudo apt update && sudo apt install -y pip && sudo apt clean
RUN pip install torch

COPY ddp_allreduce.py ddp_allreduce.py
