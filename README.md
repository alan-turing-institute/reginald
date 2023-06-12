# Reginald
The Reginald project consists of:

```
├── azure
│   └── Setup REGinald infrastructure on Azure
├── data
│   └── Extracts from the REG handbook and wiki
├── data_processing
│   └── Scripts for processing data
├── docker
│   └── Scripts for building a Docker image
├── models
│   └── REGinald models
└── slack_bot
    └── Preprocessor for wiki markdown
```

## Slack bot

This is a simple Slack bot written in Python that listens for @mentions in any channel it is in and responds with a simple message and an emoji.
The bot uses web sockets for communication.

### Prerequisites

This project uses [Poetry](https://python-poetry.org/) for dependency management.
Make sure you have Poetry installed on your machine.

Install the project dependencies:

```
poetry install --all-extras
```

If you only want to run a subset of the available packages then use:

- for the Azure configuration `--extra azure`
- for the Slack bot `--extra bot`
- for model building `--extra model`

### Getting started

1. Set up the bot in Slack: [Socket Mode Client](https://slack.dev/python-slack-sdk/socket-mode/index.html).

1. To connect to Slack, the bot requires an app token and a bot token. Put these into into a `.env` file:

    ```
    echo "export SLACK_BOT_TOKEN='your-bot-user-oauth-access-token'" >> .env
    echo "export SLACK_APP_TOKEN='your-app-level-token'" >> .env
    ```

2. Activate the virtual environment:
    ```
    poetry shell
    ```

3. Install the pre-commit hooks
    ```
    pre-commit install
    ```

### Running the Bot

1. Set environment variables:
    ```
    source .env
    ```

1. Run the bot:
    ```
    python slack_bot/bot.py
    ```

The bot will now listen for @mentions in the channels it's added to and respond with a simple message.
