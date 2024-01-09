import pulumi
from pulumi_azure_native import (
    automation,
    containerinstance,
    network,
    resources,
    storage,
)

# Get some configuration variables
stack_name = pulumi.get_stack()
config = pulumi.Config()


# Create an resource group
resource_group = resources.ResourceGroup(
    "resource_group", resource_group_name=f"rg-reginald-{stack_name}-deployment"
)

# Create an automation account
automation_account = automation.AutomationAccount(
    "automation_account",
    automation_account_name=f"aa-reginald-{stack_name}",
    resource_group_name=resource_group.name,
    sku=automation.SkuArgs(
        name="Free",
    ),
)

# Create a network security group
network_security_group = network.NetworkSecurityGroup(
    "network_security_group",
    network_security_group_name=f"nsg-reginald-{stack_name}-containers",
    resource_group_name=resource_group.name,
)

# Create a virtual network and subnet
virtual_network = network.VirtualNetwork(
    "virtual_network",
    address_space=network.AddressSpaceArgs(
        address_prefixes=["10.0.0.0/29"],
    ),
    resource_group_name=resource_group.name,
    # Define subnets inline to avoid creation/deletion issues
    subnets=[
        # Container subnet
        network.SubnetArgs(
            address_prefix="10.0.0.0/29",
            delegations=[
                network.DelegationArgs(
                    name="SubnetDelegationContainerGroups",
                    service_name="Microsoft.ContainerInstance/containerGroups",
                    type="Microsoft.Network/virtualNetworks/subnets/delegations",
                ),
            ],
            name="ContainersSubnet",
            network_security_group=network.NetworkSecurityGroupArgs(
                id=network_security_group.id
            ),
        ),
    ],
    virtual_network_name=f"vnet-reginald-{stack_name}",
    virtual_network_peerings=[],
)

# Define configuration file shares
storage_account = storage.StorageAccount(
    "storage_account",
    account_name=f"sareginald{stack_name}configuration"[:24],
    kind=storage.Kind.STORAGE_V2,
    resource_group_name=resource_group.name,
    sku=storage.SkuArgs(name=storage.SkuName.STANDARD_GRS),
)
file_share = storage.FileShare(
    "data_file_share",
    access_tier=storage.ShareAccessTier.TRANSACTION_OPTIMIZED,
    account_name=storage_account.name,
    resource_group_name=resource_group.name,
    share_name="llama-data",
    share_quota=5120,
)
storage_account_keys = pulumi.Output.all(
    storage_account.name, resource_group.name
).apply(
    lambda args: storage.list_storage_account_keys(
        account_name=args[0],
        resource_group_name=args[1],
        opts=pulumi.InvokeOptions(parent=storage_account),
    )
)
storage_account_key = storage_account_keys.apply(
    lambda keys: pulumi.Output.secret(keys.keys[0].value)
)

# Define the container group
container_group = containerinstance.ContainerGroup(
    "container_group-bot",
    container_group_name=f"aci-reginald-{stack_name}-bot",
    containers=[
        # api-bot container
        containerinstance.ContainerArgs(
            image="ghcr.io/alan-turing-institute/reginald_slackbot:pulumi",
            name="reginald-production",  # maximum of 63 characters
            environment_variables=[
                containerinstance.EnvironmentVariableArgs(
                    name="REGINALD_MODEL",
                    value="llama-index-llama-cpp",
                ),
                containerinstance.EnvironmentVariableArgs(
                    name="SLACK_APP_TOKEN",
                    secure_value=config.get_secret("REGINALD_SLACK_APP_TOKEN"),
                ),
                containerinstance.EnvironmentVariableArgs(
                    name="SLACK_BOT_TOKEN",
                    secure_value=config.get_secret("REGINALD_SLACK_BOT_TOKEN"),
                ),
                containerinstance.EnvironmentVariableArgs(
                    name="REGINALD_API_URL",
                    secure_value=config.get_secret("REGINALD_API_URL"),
                ),
            ],
            ports=[],
            resources=containerinstance.ResourceRequirementsArgs(
                requests=containerinstance.ResourceRequestsArgs(
                    cpu=1,
                    memory_in_gb=4,
                ),
            ),
        ),
    ],
    os_type=containerinstance.OperatingSystemTypes.LINUX,
    resource_group_name=resource_group.name,
    restart_policy=containerinstance.ContainerGroupRestartPolicy.ALWAYS,
    sku=containerinstance.ContainerGroupSku.STANDARD,
    volumes=[
        containerinstance.VolumeArgs(
            azure_file=containerinstance.AzureFileVolumeArgs(
                share_name=file_share.name,
                storage_account_key=storage_account_key,
                storage_account_name=storage_account.name,
            ),
            name="llama-data",
        ),
    ],
)

# Define the container group for the data creation
container_group = containerinstance.ContainerGroup(
    "container_group-data",
    container_group_name=f"aci-reginald-{stack_name}-data",
    containers=[
        # all_data index creation container
        containerinstance.ContainerArgs(
            image="ghcr.io/alan-turing-institute/reginald_create_index:pulumi",
            name="reginald-create-index",  # maximum of 63 characters
            environment_variables=[
                containerinstance.EnvironmentVariableArgs(
                    name="GITHUB_TOKEN",
                    secure_value=config.get_secret("GITHUB_TOKEN"),
                ),
                containerinstance.EnvironmentVariableArgs(
                    name="LLAMA_INDEX_WHICH_INDEX",
                    value="all_data",
                ),
                containerinstance.EnvironmentVariableArgs(
                    name="LLAMA_INDEX_MAX_INPUT_SIZE",
                    value="4096",
                ),
                containerinstance.EnvironmentVariableArgs(
                    name="LLAMA_INDEX_K",
                    value="3",
                ),
                containerinstance.EnvironmentVariableArgs(
                    name="LLAMA_INDEX_CHUNK_SIZE",
                    value="512",
                ),
                containerinstance.EnvironmentVariableArgs(
                    name="LLAMA_INDEX_CHUNK_OVERLAP_RATIO",
                    value="0.1",
                ),
                containerinstance.EnvironmentVariableArgs(
                    name="LLAMA_INDEX_NUM_OUTPUT",
                    value="512",
                ),
            ],
            ports=[],
            resources=containerinstance.ResourceRequirementsArgs(
                requests=containerinstance.ResourceRequestsArgs(
                    cpu=4,
                    memory_in_gb=16,
                ),
            ),
            volume_mounts=[
                containerinstance.VolumeMountArgs(
                    mount_path="/app/data",
                    name="llama-data",
                ),
            ],
        ),
    ],
    os_type=containerinstance.OperatingSystemTypes.LINUX,
    resource_group_name=resource_group.name,
    restart_policy=containerinstance.ContainerGroupRestartPolicy.NEVER,
    sku=containerinstance.ContainerGroupSku.STANDARD,
    volumes=[
        containerinstance.VolumeArgs(
            azure_file=containerinstance.AzureFileVolumeArgs(
                share_name=file_share.name,
                storage_account_key=storage_account_key,
                storage_account_name=storage_account.name,
            ),
            name="llama-data",
        ),
    ],
)
