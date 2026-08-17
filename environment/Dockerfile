# hash:sha256:c49bc731aeb6b57797d80f5ba1d4109b0de9e2c8427020c51aaefe8eb97a3d56
ARG REGISTRY_HOST
FROM $REGISTRY_HOST/codeocean/code-server-python-extensions-pack:v5.0

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
    numpy==2.0.0 \
    pandas==3.0.5 \
    pynwb==4.1.0 \
    rastermap==1.0 \
    scikit-learn==1.9.0 \
    scipy==1.18.0
