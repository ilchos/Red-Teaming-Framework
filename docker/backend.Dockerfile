FROM python:3.11.9 as builder

# костыль чтобы полелить установку зависимостей связанные с garak.
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

# Добавляем Rust и Cargo в PATH
ENV PATH="/root/.cargo/bin:${PATH}"

ENV PATH="/root/.local/bin:$PATH" \
    VIRTUAL_ENV=/app/.venv \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    POETRY_VERSION="1.8.3" \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    HF_INFERENCE_TOKEN="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"

WORKDIR /app

RUN pip config --user set global.progress_bar off
RUN pip install --upgrade pip
RUN pip install --user poetry==${POETRY_VERSION}
COPY poetry.lock pyproject.toml ./
RUN poetry config installer.max-workers 10
RUN poetry install --only backend

RUN mkdir logs
COPY src/backend src/backend

EXPOSE 8000

# CMD ["uvicorn", "src/backend:app", "--host", "0.0.0.0", "--port", "8000"]