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
echo "Setting app secrets..."
REGINALD_SLACK_APP_TOKEN=""
REGINALD_SLACK_BOT_TOKEN=""
REGINALD_API_URL=""
GITHUB_TOKEN=""
if [ -e ../.pulumi_env ]; then
    REGINALD_SLACK_APP_TOKEN=$(grep "REGINALD_SLACK_APP_TOKEN" ../.pulumi_env | grep -v "^#" | cut -d '"' -f 2)
    REGINALD_SLACK_BOT_TOKEN=$(grep "REGINALD_SLACK_BOT_TOKEN" ../.pulumi_env | grep -v "^#" | cut -d '"' -f 2)
    REGINALD_API_URL=$(grep "REGINALD_API_URL" ../.pulumi_env | grep -v "^#" | cut -d '"' -f 2)
    GITHUB_TOKEN=$(grep "GITHUB_TOKEN" ../.pulumi_env | grep -v "^#" | cut -d '"' -f 2)
fi

# Slack tokens
if [ -z "$REGINALD_SLACK_APP_TOKEN" ]; then
    echo "Please provide a REGINALD_SLACK_APP_TOKEN:"
    read -r REGINALD_SLACK_APP_TOKEN
else
    echo "✅ REGINALD_SLACK_APP_TOKEN environment variable found in .pulumi_env"
fi
AZURE_KEYVAULT_AUTH_VIA_CLI=true pulumi config set --secret REGINALD_SLACK_APP_TOKEN "$REGINALD_SLACK_APP_TOKEN"
if [ -z "$REGINALD_SLACK_BOT_TOKEN" ]; then
    echo "Please provide a REGINALD_SLACK_BOT_TOKEN:"
    read -r REGINALD_SLACK_BOT_TOKEN
else
    echo "✅ REGINALD_SLACK_BOT_TOKEN environment variable found in .pulumi_env"
fi
AZURE_KEYVAULT_AUTH_VIA_CLI=true pulumi config set --secret REGINALD_SLACK_BOT_TOKEN "$REGINALD_SLACK_BOT_TOKEN"

# API URL
if [ -z "$REGINALD_API_URL" ]; then
    echo "Please provide a REGINALD_API_URL:"
    read -r REGINALD_API_URL
else
    echo "✅ REGINALD_API_URL environment variable found in .pulumi_env"
fi
AZURE_KEYVAULT_AUTH_VIA_CLI=true pulumi config set --secret REGINALD_API_URL "$REGINALD_API_URL"

# GitHub token
if [ -z "$GITHUB_TOKEN" ]; then
    echo "Please provide a GITHUB_TOKEN:"
    read -r GITHUB_TOKEN
else
    echo "✅ GITHUB_TOKEN environment variable found in .pulumi_env"
fi
AZURE_KEYVAULT_AUTH_VIA_CLI=true pulumi config set --secret GITHUB_TOKEN "$GITHUB_TOKEN"
