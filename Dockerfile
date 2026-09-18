FROM python:3.14-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN useradd -m -u 1000 appuser \
    && mkdir /app \
    && chown appuser:appuser /app

WORKDIR /app
COPY --chown=appuser:appuser . /app

# Sync as appuser so the venv (incl. the editable project install) is owned by
# the runtime user - `uv run` needs write access to the venv at startup.
USER appuser
RUN uv sync --frozen --no-managed-python

CMD ["uv", "run", "app"]
