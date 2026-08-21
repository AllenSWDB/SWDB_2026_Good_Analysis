# hash:sha256:d6dd9836c8af8556a2432d06bf037ff62dc1bde9571cdb7b93e396cd127dccc2
ARG REGISTRY_HOST
FROM $REGISTRY_HOST/codeocean/swdb:Python3.12code-server4.133

ARG DEBIAN_FRONTEND=noninteractive
ARG GIT_ASKPASS
COPY git-ask-pass /

RUN conda install -y \
        jupyter==1.1.1 \
    && conda clean -ya

RUN pip3 install -U --no-cache-dir \
    hdmf-zarr==0.13.0 \
    ipympl==0.10.0 \
    matplotlib==3.11.1 \
    numpy==2.5.1 \
    pandas==3.0.5 \
    pynwb==4.1.0 \
    rastermap==1.0 \
    scikit-learn==1.9.0 \
    scipy==1.18.0
