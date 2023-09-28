To build this Docker image you need to be in the root of the repository (i.e. the parent directory of this one).

## Reginald model

The following command will build it the image for the (full) Reginald model which has the model + slack bot and tag it as `reginald:latest`:

```
docker build . -t reginald:latest -f docker/reginald/Dockerfile
```

The following environment variables can be used by this image:

- `REGINALD_MODEL`: name of model to use
- `REGINALD_MODEL_NAME`: name of sub-model to use with the one requested if not using `hello` model.
    - For `llama-index-llama-cpp` and `llama-index-hf`` models, this specifies the LLM (or path to that model) which we would like to use
    - For `chat-completion-azure` and `llama-index-gpt-azure`, this refers to the deployment name on Azure
    - For `chat-completion-openai` and `llama-index-gpt-openai`, this refers to the model/engine name on OpenAI
- `LLAMA_INDEX_MODE`: mode to use ("query" or "chat") if using `llama-index` model
- `LLAMA_INDEX_DATA_DIR`: data directory if using `llama-index` model
- `LLAMA_INDEX_WHICH_INDEX`: index to use ("handbook", "wikis", "public" or "all_data") if using `llama-index` model
- `LLAMA_INDEX_FORCE_NEW_INDEX`: whether to force a new index if using `llama-index` model
- `LLAMA_INDEX_MAX_INPUT_SIZE`: max input size if using `llama-index-llama-cpp` or `llama-index-hf` model
- `LLAMA_INDEX_IS_PATH`: whether to treat REGINALD_MODEL_NAME as a path if using `llama-index-llama-cpp` model
- `LLAMA_INDEX_N_GPU_LAYERS`: number of GPU layers if using `llama-index-llama-cpp` model
- `LLAMA_INDEX_DEVICE`: device to use if using `llama-index-hf` model
- `OPENAI_API_KEY`: API key for OpenAI if using `chat-completion-openai` or `llama-index-gpt-openai` models
- `OPENAI_AZURE_API_BASE`: API base for Azure OpenAI if using `chat-completion-azure` or `llama-index-gpt-azure` models
- `OPENAI_AZURE_API_KEY`: API key for Azure OpenAI if using `chat-completion-azure` or `llama-index-gpt-azure` models
- `SLACK_APP_TOKEN`: app token for Slack
- `SLACK_BOT_TOKEN`: bot token for Slack

To run you can use the following command (to run the `hello` model):

```
docker run -e REGINALD_MODEL=hello -e SLACK_APP_TOKEN=<slack-app-token> -e SLACK_BOT_TOKEN=<slack-bot-token> reginald:latest
```

## Slack bot only

The following command will build it the image for the Slack bot only and tag it as `reginald-slack-bot:latest`:

```
docker build . -t reginald-slack-bot:latest -f docker/slack_bot/Dockerfile
```

The following environment variables will be used by this image:

- `REGINALD_EMOJI`: emoji to use for bot
- `SLACK_APP_TOKEN`: app token for Slack
- `SLACK_BOT_TOKEN`: bot token for Slack

To run you can use the following command:

```
docker run -e REGINALD_EMOJI=wave -e SLACK_APP_TOKEN=<slack-app-token> -e SLACK_BOT_TOKEN=<slack-bot-token> reginald-slack-bot:latest
```

## Using an environment file

Rather than passing in the environment variables on the command line using the `-e` flag in `docker run`, you can use an environment file:

```
docker run --env-file .env reginald:latest
```

where `.env` is a file containing the environment variables, e.g. for running the `llama-index-llama-cpp` model using the `handbook` index:

```
REGINALD_MODEL=llama-index-llama-cpp
REGINALD_MODEL_NAME=https://huggingface.co/TheBloke/Llama-2-7B-chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf
LLAMA_INDEX_MODE=chat
LLAMA_INDEX_DATA_DIR=data
LLAMA_INDEX_WHICH_INDEX=handbook
LLAMA_INDEX_MAX_INPUT_SIZE=2048
SLACK_APP_TOKEN=<slack-app-token>
SLACK_BOT_TOKEN=<slack-bot-token>
```
