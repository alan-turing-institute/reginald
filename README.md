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
How the bot responds to messages is determined by the response engine that is set up - see the [models README](MODELS.md) for more details of the models available.
The main models we use are:
-  `llama-index-llama-cpp`: a model which uses the [`llama-index`](https://github.com/jerryjliu/llama_index) library to query a data index and then uses a quantised LLM (implemented using [`llama-python-cpp`](https://github.com/abetlen/llama-cpp-python)) to generate a response
- `llama-index-hf`: a model which uses the [`llama-index`](https://github.com/jerryjliu/llama_index) library to query a data index and then uses a Huggingface LLM to generate a response
- `llama-index-gpt-azure`: a model which uses the [`llama-index`](https://github.com/jerryjliu/llama_index) library to query a data index and then uses the Azure OpenAI API to query a LLM to generate a response

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

To set up the Slack bot, you must set Slack bot environment variables. To obtain them from Slack, follow the steps below:

1. Set up the bot in Slack: [Socket Mode Client](https://slack.dev/python-slack-sdk/socket-mode/index.html).

1. To connect to Slack, the bot requires an app token and a bot token. Put these into into a `.env` file:

    ```bash
    echo "SLACK_BOT_TOKEN='your-bot-user-oauth-access-token'" >> .env
    echo "SLACK_APP_TOKEN='your-app-level-token'" >> .env
    ```

1. Activate the virtual environment:

    ```bash
    poetry shell
    ```

### GitHub access tokens

We are currently using [`llama-hub`](https://github.com/emptycrown/llama-hub) GitHub readers for creating our data indexes and pulling from relevant repos for issues and files.
As a prerequisite, you will need to generate a "classic" personal access token with the `repo` and `read:org` scopes - see [here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) for instructions for creating and obtaining your personal access token.

Once, you do this, simply add this to your `.env` file:

```bash
echo "GITHUB_TOKEN='your-github-personal-access-token'" >> .env
```

### Running the Reginald bot locally

In order to run the full Reginald app locally (i.e. setting up the full response engine along with the Slack bot), you can follow the steps below:

1. Set environment variables (for more details on environtment variables, see the [environment variables README](ENVIRONMENT_VARIABLES.md)):

    ```bash
    source .env
    ```

1. Run the bot using `reginald_run` - note that this actually runs [`reginald/run.py`](https://github.com/alan-turing-institute/reginald/blob/main/reginald/run.py). To see CLI arguments:

    ```bash
    reginald_run --help
    ```

The `reginald_run` CLI takes in several arguments such as:
- `--model` (`-m`): to select the type of model to use
- `--model-name` (`-n`): to select the sub-model to use within the model selected
- `--mode`: to determine whether to use 'query' or 'chat' engine
- `--data-dir` (`-d`): specify the data directory location
- `--which-index` (`-w`): specify the directory name for looking up/writing data index (for `llama-index` models)
- `--force-new-index` (`-f`): whether or not to force create a new data index
- `--max-input-size` (`-max`): maxumum input size of LLM
- `--is-path` (`-p`): whether or not the model-name passed is a path to the model
- `--n-gpu-layers` (`-ngl`): number of layers to offload to GPU if using `llama-index-llama-cpp` model
- `--device` (`-dev`): device to host Huggingface model if using `llama-index-hf` model

**Note**: specifying CLI arguments will override any environment variables set.

For example, to set up a `llama-index-llama-cpp` _chat engine_ model running [Llama-2-7b-Chat](https://huggingface.co/TheBloke/Llama-2-7b-Chat-GGUF) (quantised to 4bit), you can run:

```bash
reginald_run \
  --model llama-index-llama-cpp \
  --model-name https://huggingface.co/TheBloke/Llama-2-7b-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf \
  --mode chat \
  --data-dir data/ \
  --which-index handbook \
  --max-input-size 4096 \
  --n-gpu-layers 2
```

The bot will now listen for @mentions in the channels it's added to and respond with a simple message.

### Running the response engine and Slack bot separately

There are some cases where you'd want to run the response engine and Slack bot separately.
For instance, with the `llama-index-llama-cpp` and `llama-index-hf` models, you are hosting your own LLM which you might want to host on a machine with GPUs.
The Slack bot can then be run on a separate (more cost-efficient) machine.
Doing this allows you to change the model or machine running the model without having to change the Slack bot.

To do this, you can follow the steps below:

- On the machine where you want to run the response engine, run the following command:

    1. Set up environment variables for the response engine (for more details on environtment variables, see the [environment variables README](ENVIRONMENT_VARIABLES.md)):

    ```bash
    source .response_engine_env
    ```

    2. Set up response engine using `reginald_run_api_llm` - note that this actually runs [`reginald/models/app.py`](https://github.com/alan-turing-institute/reginald/blob/main/reginald/models/app.py). To see CLI arguments:

    ```bash
    reginald_run_api_llm --help
    ```

    This command uses many of the same CLI arguments as described above. For example to set up a `llama-index-llama-cpp` _chat engine_ model running [Llama-2-7b-Chat](https://huggingface.co/TheBloke/Llama-2-7b-Chat-GGUF) (quantised to 4bit), you can run:

    ```bash
    reginald_run_api_llm \
        --model llama-index-llama-cpp \
        --model-name https://huggingface.co/TheBloke/Llama-2-7b-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf \
        --mode chat \
        --data-dir data/ \
        --which-index handbook \
        --max-input-size 4096 \
        --n-gpu-layers 2
    ```

- On the machine where you want to run the Slack bot, run the following command:

    1. Set up environment variables for the Slack bot (for more details on environtment variables, see the [environment variables README](ENVIRONMENT_VARIABLES.md)):

    ```bash
    source .slack_bot_env

    ```
    2. Set up Slack bot using `reginald_run_api_bot` - note that this actually runs [`reginald/slack_bot/setup_bot.py`](https://github.com/alan-turing-institute/reginald/blob/main/reginald/slack_bot/setup_bot.py). To see CLI arguments:

    ```bash
    reginald_run_api_bot --help
    ```

    This command takes in an emoji to respond with. For example, to set up a Slack bot that responds with the `:llama:` emoji, you can run:

    ```bash
    reginald_run_api_bot --emoji llama
    ```

### Running the bot in Docker

For full details of Docker setup, see the [Docker README](docker/README.md).

### Running the bot in Azure

1. Go to the `azure` directory

1. Ensure that you have installed `Pulumi` and the `Azure CLI`

1. Setup the Pulumi backend and deploy

```bash
./setup.sh && AZURE_KEYVAULT_AUTH_VIA_CLI=true pulumi up -y
```
