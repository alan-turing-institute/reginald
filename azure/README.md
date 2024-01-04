You will need to install

- Pulumi
- Azure CLI

in order to run this code.

1. Have a .pulumi_env file (in this directory) including the variables that you need.

For the `api_bot` model, you will need to have the following variables:

```bash
REGINALD_SLACK_APP_TOKEN
REGINALD_SLACK_BOT_TOKEN
REGINALD_API_URL
GITHUB_TOKEN
```

For the `hack_week` model, you will need to have the following variables:

```bash
OPENAI_AZURE_API_BASE
OPENAI_AZURE_API_KEY
HANDBOOK_SLACK_APP_TOKEN
HANDBOOK_SLACK_BOT_TOKEN
GPT_AZURE_SLACK_APP_TOKEN
GPT_AZURE_SLACK_BOT_TOKEN
GITHUB_TOKEN
OPENAI_API_KEY (optional)
```

2. Move into the folder for the model you want to deploy, e.g. for the `api_bot` model:

```bash
cd api_bot
```

3. Setup the Pulumi backend (if it already exists this will just check that you have access)

```bash
./setup.sh
```

This may create a local `.secrets` file.
This file contains the secrets that you need to deploy the model and includes the environment variables needed for the container instance (see Step 1.).
You will need to source this file before deploying in the next step.

4. Deploy with Pulumi

```bash
> source .secrets (if this exists)
> AZURE_KEYVAULT_AUTH_VIA_CLI=true pulumi up
```
