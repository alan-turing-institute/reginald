FROM python:3.11.9

WORKDIR /app

# Setup Python prerequisites
RUN pip3 install --upgrade pip poetry setuptools wheel

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Build Python project
COPY pyproject.toml .
RUN touch README.md
RUN poetry install --without dev --no-root  && rm -rf $POETRY_CACHE_DIR

COPY reginald reginald

RUN poetry install --extras api_bot --without dev

CMD ["poetry", "run", "reginald", "bot"]
