ARG DOCKERHUB_REGISTRY=docker.io
FROM ${DOCKERHUB_REGISTRY}/library/python:3.12-slim AS builder

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


FROM ${DOCKERHUB_REGISTRY}/library/python:3.12-slim as runner
ARG DOCKERHUB_REGISTRY=docker.io

WORKDIR /app

COPY --from=builder /app/.venv/ /app/.venv
COPY src /app/src

ENV PYTHONUNBUFFERED=1
ENV PATH=/app/.venv/bin:${PATH}
ENV PYTHONPATH=/app/src

CMD ["python", "-m", "src.app.main"]
