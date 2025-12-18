FROM python:3.12-slim-trixie AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --compile-bytecode --no-cache

COPY . .

FROM python:3.12-slim-trixie

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN useradd --create-home --shell /bin/bash appuser

WORKDIR /home/appuser/app

COPY --chown=appuser:appuser --from=builder /app/ ./

RUN mkdir -p /home/appuser/.cache/huggingface && \
  chown -R appuser:appuser /home/appuser/.cache

ENV PATH="/home/appuser/app/.venv/bin:$PATH" \
  PYTHONUNBUFFERED=1 \
  HF_HOME="/home/appuser/.cache/huggingface"

USER appuser

CMD ["uv", "run", "src/main.py"]
