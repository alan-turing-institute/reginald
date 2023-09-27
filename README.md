# Reginald
The Reginald project consists of:

```
├── azure
│   └── Setup REGinald infrastructure on Azure
├── data
│   └── Directory to store llama-index data indexes and other public Turing data
├── docker
│   └── Scripts for building a Docker images for both Reginald app and Slack-bot only app
├── notebooks
│   └── data processing notebooks
│   └── development notebooks for llama-index REGinald models
└── reginald
    └── models: scripts for setting up query and chat engines
    └── slack_bot: scripts for setting up Slack bot
    └── scripts for setting up end to end Slack bot with query engine
```

## Slack bot

This is a simple Slack bot written in Python that listens for direct messages and @mentions in any channel it is in and responds with a message and an emoji.
The bot uses web sockets for communication.

### Prerequisites

This project uses [Poetry](https://python-poetry.org/) for dependency management.
Make sure you have Poetry installed on your machine.

#### Install the project dependencies:

```bash
poetry install --all-extras
```

If you only want to run a subset of the available packages then use:

- for the LLM-only and Slack-bot-only setup: `--extras api_bot`
- for the Azure configuration: `--extras azure`
- for running notebooks regarding using fine-tuning: `--extras ft_notebooks`
- for running notebooks regarding using `llama-index`: `--extras llama_index_notebooks`

Without installing extras, you will have the packages required in order to run the full Reginald model on your machine.

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

1. Run the bot using [`slack_bot/run.py`](https://github.com/alan-turing-institute/reginald/blob/main/slack_bot/run.py). To see CLI arguments:
    ```bash
    python slack_bot/run.py --help
    ```

The bot will now listen for @mentions in the channels it's added to and respond with a simple message.

### Running the bot in Azure

1. Go to the `azure` directory

1. Ensure that you have installed `Pulumi` and the `Azure CLI`

1. Setup the Pulumi backend and deploy

```bash
./setup.sh && AZURE_KEYVAULT_AUTH_VIA_CLI=true pulumi up -y
```
