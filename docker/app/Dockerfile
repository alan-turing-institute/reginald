FROM python:3.11.4

WORKDIR /app

# Setup Python prerequisites
RUN pip3 install --upgrade pip poetry setuptools wheel

# Build Python project
COPY reginald reginald
COPY pyproject.toml .
COPY README.md .
RUN poetry install --extras api_bot

CMD ["poetry", "run", "reginald", "app"]
