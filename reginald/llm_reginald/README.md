# llm-reginald

[LLM](https://llm.datasette.io/) plugin for interacting with [Reginald](https://github.com/alan-turing-institute/reginald).

Assuming LLM is already installed, install this plugin with

```
llm install https://github.com/alan-turing-institute/llm-reginald
```

The plugin requires that a Reginald server is running.  By default this is assumed to be at `http://localhost:8000`.  This can be started by running the following command (for instance), provided by the Reginald package:

```
reginald_run_api_llm     --model llama-index-llama-cpp     --model-name https://huggingface.co/TheBloke/Llama-2-7b-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf     --mode chat     --data-dir data/     --which-index handbook     --max-input-size 4096 --n-gpu-layers -1
```

You can now interact with the llm model as

```
llm -m reginald 'Who are you?'
```

Use a different server URL:

```
llm -m reginald -o server_url <server_url> ...
```
