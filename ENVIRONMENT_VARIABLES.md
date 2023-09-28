## Environment variables for running Reginald

To set up the Reginald app (which consists of _both_ the full response engine along with the Slack bot), you can use the `reginald_run` on the terminal. To see the CLI arguments, you can simply run:

```bash
reginald_run --help
```

**Note**: specifying CLI arguments will override any environment variables set.

Below are the key environment variables that must be set:

### Slack bot tokens

You must set the Slack bot environment variables (see the main [README](README.md) for information on obtaining them from Slack):
- `SLACK_APP_TOKEN`: app token for Slack
- `SLACK_BOT_TOKEN`: bot token for Slack

### OpenAI / Azure OpenAI API keys

If you're using a model which uses the OpenAI API, you must set the OPENAI_API_KEY environment variable:

- `OPENAI_API_KEY`: API key for OpenAI if using `chat-completion-openai` or `llama-index-gpt-openai` models

If you're using a model which uses Azure's OpenAI instance, you must set the following environment variables:
- `OPENAI_AZURE_API_BASE`: API base for Azure OpenAI if using `chat-completion-azure` or `llama-index-gpt-azure` models
- `OPENAI_AZURE_API_KEY`: API key for Azure OpenAI if using `chat-completion-azure` or `llama-index-gpt-azure` models

### GitHub tokens

For creating a data index, you must set the GitHub token environment variable `GITHUB_TOKEN` (see the main [README](README.md) for information on obtaining them from GitHub):
- `GITHUB_TOKEN`: GitHub access token

### Model environment variables

Lastly, to avoid using CLI variables and be able to simply use `reginald_run`, you can also set the following variables too:

- `REGINALD_MODEL`: name of model to use (see the [models README](MODELS.md)) for the list of models available
- `REGINALD_MODEL_NAME`: name of sub-model to use with the one requested if not using `hello` model.
    - For `llama-index-llama-cpp` and `llama-index-hf`` models, this specifies the LLM model (or path to that model) which we would like to use
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

### Using an environment file

Rather than passing in the environment variables on the command line, you can use an environment file, e.g. `.env`, and set the variables using:

```bash
source .env
```

## Environment variables for running _only_ the response engine



## Environment variables for running _only_ the Slack-bot
