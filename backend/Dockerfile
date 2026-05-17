FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY pyproject.toml uv.lock ./

RUN pip install --no-cache-dir uv \
    && uv sync --frozen --no-dev

COPY backend/ .

CMD ["uv", "run", "daphne", "-b", "0.0.0.0", "-p", "8000", "config.asgi:application"]