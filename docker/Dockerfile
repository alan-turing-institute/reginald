FROM python:3.11-alpine

WORKDIR /app

# Setup Python project
COPY slack_bot slack_bot
COPY pyproject.toml .
COPY poetry.lock .
RUN pip3 install --upgrade pip poetry setuptools wheel
RUN poetry install --extras bot

# Set entrypoint
ENTRYPOINT [ "poetry" ]
CMD ["run", "python", "/app/slack_bot/bot.py"]