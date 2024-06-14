# llm-reginald

This module contains an [LLM](https://llm.datasette.io/) plugin for interacting with [Reginald](https://github.com/alan-turing-institute/reginald).

The plugin is available to use immediately after reginald is installed, as long as the `llm_plugin` extra dependencies are selected when installing the package (either with `pip install .[llm_plugin]` or `poetry install --extras llm_plugin` or `poetry install --all-extras`).

The plugin requires a running Reginald server to work.  By default this is assumed to be at `http://localhost:8000`.  Refer to the package README for instructions.

Assuming [LLM](http://llm.datasette.io/) is installed, you can interact with Reginald like this:

```
llm -m reginald 'Who are you?'
```

Using a different server URL:

```
llm -m reginald -o server_url <server_url> ...
```
