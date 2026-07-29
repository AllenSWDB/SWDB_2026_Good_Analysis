# hash:sha256:cb999df95eeac30de2af48e81a09a64746a01cc9da781ae090c73b4cd1fcb070
ARG REGISTRY_HOST
FROM $REGISTRY_HOST/codeocean/code-server-python-extensions-pack:v5.0

ARG DEBIAN_FRONTEND=noninteractive
ARG GIT_ASKPASS
COPY git-ask-pass /

RUN conda install -y \
        jupyter==1.1.1 \
    && conda clean -ya

RUN pip3 install -U --no-cache-dir \
    matplotlib \
    numpy \
    pandas \
    scipy
