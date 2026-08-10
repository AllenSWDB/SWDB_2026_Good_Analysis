# hash:sha256:b0479cfcb348814fa349b84beadfd65571133f76941c2357fda1952a0cba4db1
ARG REGISTRY_HOST
FROM $REGISTRY_HOST/codeocean/code-server-python-extensions-pack:code-server4.129.0python3.12.4codeocean-mcp-serveruvpyreflyetc

ARG DEBIAN_FRONTEND=noninteractive
ARG GIT_ASKPASS
COPY git-ask-pass /

RUN conda install -y \
        jupyter==1.1.1 \
    && conda clean -ya

RUN pip3 install -U --no-cache-dir \
    matplotlib==3.11.1 \
    numpy==2.5.1 \
    pandas==3.0.5 \
    scipy==1.18.0
