To build this Docker image you need to be in the root of the repository.

## United model

The following command will build it the image for the full (or "united") model which has the model + slack bot and tag it as `reginald:latest`:

```
docker build . -t reginald:latest -f docker/united/Dockerfile
```

The following environment variables will be used by this image:

- `REGINALD_MODEL`: name of model to use
- `REGINALD_MODEL_NAME`: name of sub-model to use with the one requested if not using `hello` model
- `LLAMA_INDEX_MODE`: mode to use ("query" or "chat") if using `llama-index` model
- `LLAMA_INDEX_DATA_DIR`: data directory if using `llama-index` model
- `LLAMA_INDEX_WHICH_INDEX`: index to use if using `llama-index` model
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

**Note:** If none of these are set, then a `hello` model will be created by default.

## Slack bot only

The following command will build it the image for the Slack bot only and tag it as `reginald-slack-bot:latest`:

```
docker build . -t reginald-slack-bot:latest -f docker/slack_bot/Dockerfile
```

The following environment variables will be used by this image:
- `SLACK_APP_TOKEN`: app token for Slack
- `SLACK_BOT_TOKEN`: bot token for Slack
