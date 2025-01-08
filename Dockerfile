FROM docker.io/rayproject/ray:2.38.0-py312-cu123

RUN sudo apt update && sudo apt install -y pip infiniband-diags && sudo apt clean
RUN pip install torch==2.5.1

COPY ddp_allreduce.py ddp_allreduce.py
