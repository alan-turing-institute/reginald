FROM python:3.11.4-slim

WORKDIR /app

# Setup Python prerequisites
RUN pip3 install --upgrade pip poetry setuptools wheel

# Build Python project
COPY slack_bot slack_bot
COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install --extras bot

# Force install CPU version of torch
RUN poetry run python -m pip install --upgrade torch --index https://download.pytorch.org/whl/cpu

# Set entrypoint
ENTRYPOINT [ "poetry" ]
CMD ["run", "python", "/app/slack_bot/run.py"]
