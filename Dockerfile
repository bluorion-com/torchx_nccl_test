FROM docker.io/rayproject/ray:2.38.0-py312-cu123

RUN sudo apt update && \
    sudo apt install -y \
    pip \
    infiniband-diags \
    libibverbs-dev \
    && sudo apt clean && \
    sudo rm -rf /var/cache/apt/archives /var/lib/apt/lists/*
RUN pip install torch==2.5.1

COPY ddp_allreduce.py ddp_allreduce.py
