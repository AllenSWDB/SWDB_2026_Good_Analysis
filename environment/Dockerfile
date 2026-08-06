# hash:sha256:f5817036d8c78c85b6a6aa3cbb5699f37b669fe67630e7d2a4ede66dcefeb7d3
ARG REGISTRY_HOST
FROM $REGISTRY_HOST/codeocean/code-server-python-extensions-pack:v5.0

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
