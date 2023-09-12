#! /usr/bin/env bash

# Arguments
SUBSCRIPTION_NAME=${1:-"Reg Hack Week 2023: Reginald"}
STACK_NAME=${2:-"production"}

# Fixed values
CONTAINER_NAME="pulumi"
ENCRYPTION_KEY_NAME="pulumi-encryption-key"
KEYVAULT_NAME=$(echo "kv-reginald-${STACK_NAME}" | head -c 24)
LOCATION="uksouth"
RESOURCE_GROUP_NAME="rg-reginald-${STACK_NAME}-backend"
STORAGE_ACCOUNT_NAME=$(echo "sareginald${STACK_NAME}backend$(echo "$SUBSCRIPTION_NAME" | md5sum)" | head -c 24)

# Ensure that the user is logged in
if ! (az account show > /dev/null); then
    az login
fi

# Switch subscription
echo "Creating Pulumi backend resources in '$SUBSCRIPTION_NAME'..."
az account set --subscription "$SUBSCRIPTION_NAME" --only-show-errors > /dev/null || exit 1

# Set up a resource group
az group create --location "$LOCATION" --name "$RESOURCE_GROUP_NAME" --only-show-errors > /dev/null || exit 2
echo "✅ Resource group '$RESOURCE_GROUP_NAME'"

# Create storage account and container
az storage account create --name "$STORAGE_ACCOUNT_NAME" --resource-group "$RESOURCE_GROUP_NAME" --allow-blob-public-access --only-show-errors > /dev/null || exit 3
echo "✅ Storage account '$STORAGE_ACCOUNT_NAME'"
az storage container create --name "$CONTAINER_NAME" --account-name "$STORAGE_ACCOUNT_NAME" --only-show-errors > /dev/null || exit 4
echo "✅ Storage container '$CONTAINER_NAME'"

# Create keyvault and encryption key
if ! (az keyvault show --name "$KEYVAULT_NAME" --resource-group "$RESOURCE_GROUP_NAME" --only-show-errors > /dev/null 2>&1); then
    az keyvault create --location "$LOCATION" --name "$KEYVAULT_NAME" --resource-group "$RESOURCE_GROUP_NAME" --only-show-errors > /dev/null || exit 5
fi
echo "✅ Keyvault '$KEYVAULT_NAME'"
if ! (az keyvault key show --name "$ENCRYPTION_KEY_NAME" --vault-name "$KEYVAULT_NAME" --only-show-errors > /dev/null 2>&1); then
    az keyvault key create --name "$ENCRYPTION_KEY_NAME" --vault-name "$KEYVAULT_NAME" --only-show-errors > /dev/null || exit 6
fi
echo "✅ Encryption key '$ENCRYPTION_KEY_NAME'"

# Check whether this user has access to the storage account
echo "Checking whether this user has appropriate permissions..."
USER_ID=$(az ad signed-in-user show --query "id" | xargs)
if [ "$(az role assignment list --include-inherited --assignee "$USER_ID" --role "Storage Blob Data Contributor")" ]; then
    echo "✅ User has 'Storage Blob Data Contributor' permissions on this subscription"
else
    echo "You will need 'Storage Blob Data Contributor' access to this subscription in order to continue"
    return 0
fi
az keyvault set-policy --name "$KEYVAULT_NAME" --object-id "$USER_ID" --secret-permissions "all" --key-permissions "all" --certificate-permissions "all" --only-show-errors > /dev/null || exit 7
echo "✅ User has read permissions on '$KEYVAULT_NAME'"

# Log in with Pulumi
echo "Logging in with Pulumi..."
echo "AZURE_STORAGE_KEY=$(az storage account keys list --account-name "$STORAGE_ACCOUNT_NAME" --resource-group "$RESOURCE_GROUP_NAME" --output tsv --query '[0].value')" > .secrets
source .secrets
pulumi login "azblob://$CONTAINER_NAME?storage_account=$STORAGE_ACCOUNT_NAME"

# Select the correct stack
if ! (pulumi stack select "$STACK_NAME" > /dev/null); then
    echo "Creating new Pulumi stack..."
    pulumi stack init "$STACK_NAME" --secrets-provider "azurekeyvault://$KEYVAULT_NAME.vault.azure.net/keys/$ENCRYPTION_KEY_NAME"
fi
echo "✅ Switched to Pulumi stack '$STACK_NAME'"
AZURE_KEYVAULT_AUTH_VIA_CLI=true pulumi stack change-secrets-provider "azurekeyvault://$KEYVAULT_NAME.vault.azure.net/keys/$ENCRYPTION_KEY_NAME"
echo "✅ Using Azure KeyVault '$KEYVAULT_NAME' for encryption"

# Configure the azure-native plugin
AZURE_KEYVAULT_AUTH_VIA_CLI=true pulumi config set azure-native:tenantId "$(az account list --all --query "[?isDefault].tenantId | [0]" --output tsv)"
AZURE_KEYVAULT_AUTH_VIA_CLI=true pulumi config set azure-native:subscriptionId "$(az account list --all --query "[?isDefault].id | [0]" --output tsv)"
AZURE_KEYVAULT_AUTH_VIA_CLI=true pulumi config set azure-native:location "$LOCATION"
echo "✅ Configured azure-native defaults"

# Set app secrets
OPENAI_AZURE_API_BASE=""
OPENAI_AZURE_API_KEY=""
OPENAI_API_KEY=""
REGINALD_MODEL=""
HANDBOOK_SLACK_APP_TOKEN=""
HANDBOOK_SLACK_BOT_TOKEN=""
LLAMA_SLACK_APP_TOKEN=""
LLAMA_SLACK_BOT_TOKEN=""
if [ -e ../.env ]; then
    OPENAI_AZURE_API_BASE=$(grep "OPENAI_AZURE_API_BASE" ../.env | grep -v "^#" | cut -d '"' -f 2)
    OPENAI_AZURE_API_KEY=$(grep "OPENAI_AZURE_API_KEY" ../.env | grep -v "^#" | cut -d '"' -f 2)
    OPENAI_API_KEY=$(grep "OPENAI_API_KEY" ../.env | grep -v "^#" | cut -d '"' -f 2)
    REGINALD_MODEL=$(grep "REGINALD_MODEL" ../.env | grep -v "^#" | cut -d '"' -f 2)
    HANDBOOK_SLACK_APP_TOKEN=$(grep "HANDBOOK_SLACK_APP_TOKEN" ../.env | grep -v "^#" | cut -d '"' -f 2)
    HANDBOOK_SLACK_BOT_TOKEN=$(grep "HANDBOOK_SLACK_BOT_TOKEN" ../.env | grep -v "^#" | cut -d '"' -f 2)
    LLAMA_SLACK_APP_TOKEN=$(grep "LLAMA_SLACK_APP_TOKEN" ../.env | grep -v "^#" | cut -d '"' -f 2)
    LLAMA_SLACK_BOT_TOKEN=$(grep "LLAMA_SLACK_BOT_TOKEN" ../.env | grep -v "^#" | cut -d '"' -f 2)
fi

# We always need a model name and Slack tokens
if [ -z "$REGINALD_MODEL" ]; then
    echo "Please provide a REGINALD_MODEL:"
    read -r REGINALD_MODEL
fi
AZURE_KEYVAULT_AUTH_VIA_CLI=true pulumi config set REGINALD_MODEL "$REGINALD_MODEL"

# Handbook
if [ -z "$HANDBOOK_SLACK_APP_TOKEN" ]; then
    echo "Please provide a HANDBOOK_SLACK_APP_TOKEN:"
    read -r HANDBOOK_SLACK_APP_TOKEN
fi
AZURE_KEYVAULT_AUTH_VIA_CLI=true pulumi config set --secret HANDBOOK_SLACK_APP_TOKEN "$HANDBOOK_SLACK_APP_TOKEN"
if [ -z "$HANDBOOK_SLACK_BOT_TOKEN" ]; then
    echo "Please provide a HANDBOOK_SLACK_BOT_TOKEN:"
    read -r HANDBOOK_SLACK_BOT_TOKEN
fi
AZURE_KEYVAULT_AUTH_VIA_CLI=true pulumi config set --secret HANDBOOK_SLACK_BOT_TOKEN "$HANDBOOK_SLACK_BOT_TOKEN"

# Llama tokens
if [ -z "$LLAMA_SLACK_APP_TOKEN" ]; then
    echo "Please provide a LLAMA_SLACK_APP_TOKEN:"
    read -r LLAMA_SLACK_APP_TOKEN
fi
AZURE_KEYVAULT_AUTH_VIA_CLI=true pulumi config set --secret LLAMA_SLACK_APP_TOKEN "$LLAMA_SLACK_APP_TOKEN"
if [ -z "$LLAMA_SLACK_BOT_TOKEN" ]; then
    echo "Please provide a LLAMA_SLACK_BOT_TOKEN:"
    read -r LLAMA_SLACK_BOT_TOKEN
fi
AZURE_KEYVAULT_AUTH_VIA_CLI=true pulumi config set --secret LLAMA_SLACK_BOT_TOKEN "$LLAMA_SLACK_BOT_TOKEN"

# The ChatCompletionAzure and LlamaGPTAzure models need an Azure backend
if [[ $REGINALD_MODEL == *azure* ]]; then
    if [ -z "$OPENAI_AZURE_API_BASE" ]; then
        echo "Please provide a OPENAI_AZURE_API_BASE:"
        read -r OPENAI_AZURE_API_BASE
    fi
    AZURE_KEYVAULT_AUTH_VIA_CLI=true pulumi config set OPENAI_AZURE_API_BASE "$OPENAI_AZURE_API_BASE"
    if [ -z "$OPENAI_AZURE_API_KEY" ]; then
        echo "Please provide a OPENAI_AZURE_API_KEY:"
        read -r OPENAI_AZURE_API_KEY
    fi
    AZURE_KEYVAULT_AUTH_VIA_CLI=true pulumi config set --secret OPENAI_AZURE_API_KEY "$OPENAI_AZURE_API_KEY"
fi

# The ChatCompletionOpenAI and LlamaGPTOpenAI models need an OpenAI key
if [[ $REGINALD_MODEL == *openai* ]]; then
    if [ -z "$OPENAI_API_KEY" ]; then
        echo "Please provide a OPENAI_API_KEY:"
        read -r OPENAI_API_KEY
    fi
    AZURE_KEYVAULT_AUTH_VIA_CLI=true pulumi config set --secret OPENAI_API_KEY "$OPENAI_API_KEY"
fi
