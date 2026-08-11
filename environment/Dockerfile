# hash:sha256:bddbb5c36977a697804241adaa25e9024639651e6ab53ebc23e1ed4260fa8178
ARG REGISTRY_HOST
FROM $REGISTRY_HOST/codeocean/code-server-python-extensions-pack:v5.0

ARG DEBIAN_FRONTEND=noninteractive
ARG GIT_ASKPASS
COPY git-ask-pass /

RUN conda install -y \
        jupyter==1.1.1 \
    && conda clean -ya

RUN pip3 install -U --no-cache-dir \
    ipympl \
    matplotlib==3.11.1 \
    numpy==2.5.1 \
    pandas==3.0.5 \
    pynwb \
    rastermap \
    scikit-learn \
    scipy==1.18.0
