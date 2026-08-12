# hash:sha256:9e78f0bde2568d20f7f5eebe82c4bef06fa22e6eb134d61c05e8213fbe14beff
ARG REGISTRY_HOST
FROM $REGISTRY_HOST/codeocean/code-server-python-extensions-pack:v5.0

ARG DEBIAN_FRONTEND=noninteractive
ARG GIT_ASKPASS
COPY git-ask-pass /

RUN conda install -y \
        jupyter==1.1.1 \
    && conda clean -ya

RUN pip3 install -U --no-cache-dir \
    ipympl==0.10.0 \
    matplotlib==3.11.1 \
    numpy==2.0.0 \
    pandas==3.0.5 \
    pynwb==4.1.0 \
    rastermap==1.0 \
    scikit-learn==1.9.0 \
    scipy==1.18.0
