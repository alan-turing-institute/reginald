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
    └── Python Slack bot
```

## Slack bot

This is a simple Slack bot written in Python that listens for @mentions in any channel it is in and responds with a simple message and an emoji.
The bot uses web sockets for communication.

### Prerequisites

This project uses [Poetry](https://python-poetry.org/) for dependency management.
Make sure you have Poetry installed on your machine.

#### Install the project dependencies:

```bash
poetry install --all-extras
```

If you only want to run a subset of the available packages then use:

- for the Azure configuration `--extra azure`
- for the Slack bot `--extra bot`
- for model building `--extra model`


####  Install the pre-commit hooks

```bash
pre-commit install
```

### Obtaining Slack tokens

1. Set up the bot in Slack: [Socket Mode Client](https://slack.dev/python-slack-sdk/socket-mode/index.html).

1. To connect to Slack, the bot requires an app token and a bot token. Put these into into a `.env` file:

    ```bash
    echo "export SLACK_BOT_TOKEN='your-bot-user-oauth-access-token'" >> .env
    echo "export SLACK_APP_TOKEN='your-app-level-token'" >> .env
    ```

1. Activate the virtual environment:
    ```bash
    poetry shell
    ```

### Running the bot locally

1. Set environment variables:
    ```bash
    source .env
    ```

1. Run the bot:
    ```bash
    python slack_bot/bot.py
    ```

The bot will now listen for @mentions in the channels it's added to and respond with a simple message.

### Running the bot in Azure

1. Go to the `azure` directory

1. Ensure that you have installed `Pulumi` and the `Azure CLI`

1. Setup the Pulumi backend (if it already exists this will just check that you have access)

```bash
./setup.sh
```

1. Deploy with Pulumi

```bash
> source .secrets
> AZURE_KEYVAULT_AUTH_VIA_CLI=true pulumi refresh
> AZURE_KEYVAULT_AUTH_VIA_CLI=true pulumi preview
> AZURE_KEYVAULT_AUTH_VIA_CLI=true pulumi update
```
