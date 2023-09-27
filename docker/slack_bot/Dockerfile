FROM python:3.11.4

WORKDIR /app

# Setup Python prerequisites
RUN pip3 install --upgrade pip poetry setuptools wheel

# Build Python project
COPY reginald .
COPY pyproject.toml .
RUN poetry install --extras api_bot

# Set entrypoint
CMD ["reginald_run_api_bot -e test_tube"]
