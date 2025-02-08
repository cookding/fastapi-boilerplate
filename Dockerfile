ARG DOCKERHUB_REGISTRY=docker.io
ARG APT_DEBIAN_MIRROR_HOST=
FROM ${DOCKERHUB_REGISTRY}/library/python:3.12-slim AS builder
ARG APT_DEBIAN_MIRROR_HOST

RUN if [ "${APT_DEBIAN_MIRROR_HOST}" != "" ]; then sed -i "s/deb.debian.org/${APT_DEBIAN_MIRROR_HOST}/g" /etc/apt/sources.list.d/debian.sources; fi

RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
        nodejs \
        npm \
        openssl \
    ; \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

ARG PIP_INDEX_URL=https://pypi.org/simple
ENV PIP_ONLY_BINARY=:all:
RUN pip install --index-url ${PIP_INDEX_URL} pdm

COPY pyproject.toml pdm.lock README.md /app/

ARG PDM_PYPI_URL=https://pypi.org/simple
ARG PDM_PYPI_USERNAME=
ARG PDM_PYPI_PASSWORD=
ENV PDM_ONLY_BINARY=:all:
ENV PDM_CHECK_UPDATE=false
RUN python -m venv .venv && \
    pdm install --check --prod --no-editable

ARG NPM_REGISTRY=https://registry.npmjs.org/
ARG NPM_REGISTRY_TOKEN_KEY=
ARG NPM_REGISTRY_TOKEN_VALUE=
ENV PATH=/app/.venv/bin:${PATH}
ENV PRISMA_BINARY_CACHE_DIR=/app/.venv/prisma-binaries
RUN npm config set registry "${NPM_REGISTRY}" && \
    if [ "${NPM_REGISTRY_TOKEN_KEY}" != "" ]; then npm config set "${NPM_REGISTRY_TOKEN_KEY}" "${NPM_REGISTRY_TOKEN_VALUE}"; fi
RUN prisma version # trigger prisma cli installation

COPY prisma /app/prisma
RUN prisma generate

FROM ${DOCKERHUB_REGISTRY}/library/python:3.12-slim as runner
ARG DOCKERHUB_REGISTRY=docker.io
ARG APT_DEBIAN_MIRROR_HOST

RUN if [ "${APT_DEBIAN_MIRROR_HOST}" != "" ]; then sed -i "s/deb.debian.org/${APT_DEBIAN_MIRROR_HOST}/g" /etc/apt/sources.list.d/debian.sources; fi

RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
        nodejs \
        npm \
        openssl \
    ; \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /app/.venv/ /app/.venv
COPY prisma /app/prisma
COPY src /app/src

ENV PYTHONUNBUFFERED=1
ENV PATH=/app/.venv/bin:${PATH}
ENV PRISMA_BINARY_CACHE_DIR=/app/.venv/prisma-binaries
ENV PYTHONPATH=/app/src

CMD ["python", "-m", "src.app.main"]
