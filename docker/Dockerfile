FROM python:3.11.4-slim

WORKDIR /app

# Copy data into the working directory
COPY data data

# Setup Python prerequisites
RUN pip3 install --upgrade pip poetry setuptools wheel

# Build Python project
COPY slack_bot slack_bot
COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install --extras bot

# Set entrypoint
ENTRYPOINT [ "poetry" ]
CMD ["run", "python", "/app/slack_bot/run.py"]
