FROM python:3.14-slim as builder
WORKDIR /app

RUN pip install "poetry>=2.0.1"

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && poetry install --only main --no-interaction --no-ansi --no-root

FROM python:3.14-slim
WORKDIR /app

COPY --from=builder /usr/local/lib/python3.14/site-packages /usr/local/lib/python3.14/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY backend/ ./backend/

ENV PYTHONPATH=/app
CMD ["sh", "-c", "alembic -c backend/alembic.ini upgrade head && uvicorn backend.main:app --host 0.0.0.0 --port 8000"]