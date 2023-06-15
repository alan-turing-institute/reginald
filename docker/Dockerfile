FROM python:3.11.4

WORKDIR /app

# Setup Python prerequisites
RUN pip3 install --upgrade pip poetry setuptools wheel

# Build Python project
COPY slack_bot slack_bot
COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install --extras bot

# Copy public data
RUN mkdir -p data/public
COPY data/public data/public

# Set entrypoint
ENTRYPOINT [ "poetry" ]
CMD ["run", "python", "/app/slack_bot/run.py"]
