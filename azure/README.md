You will need to install

- Pulumi
- Azure CLI

in order to run this code.

1. Setup the Pulumi backend (if it already exists this will just check that you have access)

```bash
./setup.sh
```

this will also create a local `.secrets` file

2. Deploy with Pulumi

```bash
> source .secrets
> AZURE_KEYVAULT_AUTH_VIA_CLI=true pulumi update
```