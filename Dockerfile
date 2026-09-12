FROM python:3.14-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN useradd -m -u 1000 appuser

WORKDIR /app
ADD . /app

# RUN uv sync --frozen --no-install-project --no-managed-python
RUN uv sync --frozen --no-managed-python

USER appuser

CMD ["uv", "run", "app"]
