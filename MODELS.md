# Reginald Models

We currently have the following models available:

- `hello`: a simple model which responds to a message with a greeting and an emoji
- `llama-index-llama-cpp`: a model which uses the [`llama-index`](https://github.com/jerryjliu/llama_index) library to query a data index and then uses a quantised LLM (implemented using [`llama-python-cpp`](https://github.com/abetlen/llama-cpp-python)) to generate a response
- `llama-index-hf`: a model which uses the [`llama-index`](https://github.com/jerryjliu/llama_index) library to query a data index and then uses an LLM from [Huggingface](https://huggingface.co/models) to generate a response
- `llama-index-gpt-azure`: a model which uses the [`llama-index`](https://github.com/jerryjliu/llama_index) library to query a data index and then uses the Azure OpenAI API to query a LLM to generate a response
- `llama-index-gpt-openai`: a model which uses the [`llama-index`](https://github.com/jerryjliu/llama_index) library to query a data index and then uses the OpenAI API to query a LLM to generate a response
- `chat-completion-azure`: a chat completion model which uses the Azure OpenAI API to query a LLM to generate a response (does not use `llama-index`)
- `chat-completion-openai`: a chat completion model which uses the OpenAI API to query a LLM to generate a response (does not use `llama-index`)

## `llama-index` Models

The library has several models which use the [`llama-index`](https://github.com/jerryjliu/llama_index) library which allow us to easily augment an LLM with our own data. In particular, we use `llama-index` to ingest several data sources, including several public sources:

- [The Research Engineering Group (REG) Handbook](https://alan-turing-institute.github.io/REG-handbook/)
- [The Turing Way](https://the-turing-way.netlify.app/)
- [The Research Software Engineering (RSE) course ran by REG](https://alan-turing-institute.github.io/rse-course/)
- [The Research Data Science (RDS) course ran by REG](https://alan-turing-institute.github.io/rds-course/)
- [The public Turing website](https://www.turing.ac.uk/)

And also some private sources from our private GitHub repositories (using the repo's Wiki pages, issues and some selected files).

All of these (besides the public Turing website) are loaded using [`llama-hub`](https://github.com/emptycrown/llama-hub) [GitHub readers](https://llamahub.ai/l/github_repo). Hence, when we are first building up the data index, we must set up the GitHub access tokens (see the [README](README.md) for more details), and you will only be able to build the `all_data` data index if you have access to our private repositories.

### Data index options

When running the Reginald Slack bot, you can specify which data index to use using the `LLAMA_INDEX_WHICH_INDEX` environment variable (see the [environment variables README](ENVIRONMENT_VARIABLES.md) for more details). The options are:
- `handbook`: only builds an index with the public REG handbook
- `wikis`: only builds an index with private REG repo Wiki pages
- `public`: builds an index with the all the public data listed above
- `all_data`: builds an index with all the data listed above including data from our private repo

Once a data index has been built, it will be saved in the `data` directory specified in the `reginald_run` (or `reginald_run_api_llm`) CLI arguments or the `LLAMA_INDEX_DATA_DIR` environment variable. If you want to force a new index to be built, you can use the `--force-new-index` or `-f` flag, or you can set the `LLAMA_INDEX_FORCE_NEW_INDEX` environment variable to `True`.

There are several options of the LLM to use with the `llama-index` models, some of which we have implemented in this library and which we discuss below.

## `llama-index` models with self-hosted LLM

We have two models which involve hosting the LLM ourselves and using the `llama-index` library to query the data index and then generate a response using the LLM. These models are:

### `llama-index-llama-cpp` Model

This model uses the [`llama-cpp-python`](https://github.com/abetlen/llama-cpp-python) library to host a quantised LLM. In our case, we have been using quantised versions of Meta's Llama-2 model uploaded by [TheBloke](https://huggingface.co/TheBloke) on Huggingface's model hub. An example of running this model locally is:

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

Note that the `--n-gpu-layers` argument is optional and specifies the number of layers to offload to the GPU. If not specified, it will default to 0. See the [`llama-cpp-python` README](https://github.com/abetlen/llama-cpp-python) to see how you can install the library with hardware acceleration.

Running this in a root of this repository will automatically pick up the data indices for the handbook in `data/llama_index_indices/handbook` directory.

Running this command requires about 7GB of RAM. We were able to run this on our M1 Pro (32GB) macbook pros with no issues and were able to run the [Llama-2-13B-chat](https://huggingface.co/TheBloke/Llama-2-13B-chat-GGUF) model too.

If you wish to download the quantised model (as a `.gguf` file) and host it yourself, you can do so by passing the file name to the `--model-name` argument and using the `--is-path` flag (alternatively, you can re-run the above but first set the environment variable `LLAMA_INDEX_IS_PATH` to `True`):

```bash
reginald_run \
  --model llama-index-llama-cpp \
  --model-name gguf_models/llama-2-7b-chat.Q4_K_M.gguf \
  --is-path \
  --mode chat \
  --data-dir data/ \
  --which-index handbook \
  --max-input-size 4096 \
  --n-gpu-layers 2
```

given that the `llama-2-7b-chat.Q4_K_M.gguf` file is in a `gguf_models` directory.

### `llama-index-hf` Model

This model uses an LLM from [Huggingface](https://huggingface.co/models) to generate a response. An example of running this model locally is:

```bash
reginald_run \
  --model llama-index-hf \
  --model-name microsoft/phi-1_5 \
  --mode chat \
  --data-dir data/ \
  --which-index handbook \
  --max-input-size 2048 \
  --device auto
```

Note currently the [`microsoft/phi-1_5`](https://huggingface.co/microsoft/phi-1_5) model has a predefined maximum length of 2048 context length. Hence, we must set the `--max-input-size` argument to be less than or equal to 2048 as the default value for this argument is 4096. We also set the `--device` argument to be `auto` so that the model will be run on the GPU if available.

## `llama-index` models using an API

We have two models which use an API to query a LLM to generate a response. These models are:

### `llama-index-gpt-azure` Model

To use this model, you must set the following environment variables:
- `OPENAI_AZURE_API_BASE`: API base for Azure OpenAI
- `OPENAI_AZURE_API_KEY`: API key for Azure OpenAI

An example of running this model locally is:

```bash
reginald_run \
  --model llama-index-gpt-azure \
  --model-name "reginald-gpt35-turbo" \
  --mode chat \
  --data-dir data/ \
  --which-index handbook
```

Note that `"reginald-gpt35-turbo"` is the name of our deployment of the "gpt-3.5-turbo" model on Azure. This probably is different on your deployment and resource group on Azure.

### `llama-index-gpt-openai` Model

To use this model, you must set the `OPENAI_API_KEY` environment variable and set this to be an API key for OpenAI.

An example of running this model locally is:

```bash
reginald_run \
  --model llama-index-gpt-openai \
  --model-name "gpt-3.5-turbo" \
  --mode chat \
  --data-dir data/ \
  --which-index handbook
```

## `chat-completion` Models

The library also has several models which use the OpenAI API (or the Azure OpenAI API) to query a LLM to generate a response. These models do not use the `llama-index` library and hence do not use a data index - these are purely chat completion models.

### `chat-completion-azure` Model

To use this model, you must set the following environment variables:
- `OPENAI_AZURE_API_BASE`: API base for Azure OpenAI
- `OPENAI_AZURE_API_KEY`: API key for Azure OpenAI

An example of running this model locally is:

```bash
reginald_run \
  --model chat-completion-azure \
  --model-name "reginald-curie"
```

Note that `"reginald-curie"` is the name of our deployment of a fine-tuned model on Azure. This probably is different on your deployment and resource group on Azure.
With Azure's AI Studio, it is possible to fine-tune your own model with Q&A pairs (see [here](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/fine-tuning) for more details).

### `chat-completion-openai` Model

To use this model, you must set the `OPENAI_API_KEY` environment variable and set this to be an API key for OpenAI.

An example of running this model locally is:

```bash
reginald_run \
  --model chat-completion-openai \
  --model-name "gpt-3.5-turbo"
```
