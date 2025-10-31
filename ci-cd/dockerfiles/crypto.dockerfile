# ci-cd/dockerfiles/crypto.dockerfile
FROM python:3.13-slim

WORKDIR /app

RUN pip install --no-cache-dir poetry==2.2.1 && poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml ./

RUN poetry install --no-interaction --no-ansi --without=dev

COPY src/ ./

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]