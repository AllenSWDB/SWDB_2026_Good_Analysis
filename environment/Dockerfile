# hash:sha256:9a18af007a5b5bbdb66ea5d01bb698388a9f11b69f957772d88452560a70b219
ARG REGISTRY_HOST
FROM $REGISTRY_HOST/codeocean/swdb:Python3.12code-server4.133

ARG DEBIAN_FRONTEND=noninteractive
ARG GIT_ASKPASS
COPY git-ask-pass /

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
