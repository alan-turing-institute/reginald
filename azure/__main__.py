import pulumi
from pulumi_azure_native import containerinstance, network, resources, storage

# Get some configuration variables
stack_name = pulumi.get_stack()
config = pulumi.Config()
# azurecfg = pulumi.Config("azure-native")

# Create an resource group
resource_group = resources.ResourceGroup(
    "resource_group", resource_group_name=f"rg-reginald-{stack_name}-deployment"
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
    access_tier=storage.AccessTier.COOL,
    account_name=f"sareginald{stack_name}configuration"[:24],  # max 24 characters
    enable_https_traffic_only=False,
    encryption=storage.EncryptionArgs(
        key_source=storage.KeySource.MICROSOFT_STORAGE,
        services=storage.EncryptionServicesArgs(
            file=storage.EncryptionServiceArgs(
                enabled=True, key_type=storage.KeyType.ACCOUNT
            ),
        ),
    ),
    kind=storage.Kind.FILE_STORAGE,
    resource_group_name=resource_group.name,
    sku=storage.SkuArgs(name=storage.SkuName.PREMIUM_ZRS),
)
file_share = storage.FileShare(
    "data_file_share",
    access_tier=storage.ShareAccessTier.PREMIUM,
    account_name=storage_account.name,
    resource_group_name=resource_group.name,
    share_name="llama-data",
    share_quota=5120,
)

# Define the container group
container_group = containerinstance.ContainerGroup(
    "container_group",
    container_group_name=f"aci-reginald-{stack_name}",
    containers=[
        containerinstance.ContainerArgs(
            image="ghcr.io/alan-turing-institute/reginald:main",
            name="reginald",  # maximum of 63 characters
            environment_variables=[
                containerinstance.EnvironmentVariableArgs(
                    name="OPENAI_AZURE_API_BASE",
                    value=config.get_secret("OPENAI_AZURE_API_BASE"),
                ),
                containerinstance.EnvironmentVariableArgs(
                    name="OPENAI_AZURE_API_KEY",
                    secure_value=config.get_secret("OPENAI_AZURE_API_KEY"),
                ),
                containerinstance.EnvironmentVariableArgs(
                    name="OPENAI_API_KEY",
                    secure_value=config.get_secret("OPENAI_API_KEY"),
                ),
                containerinstance.EnvironmentVariableArgs(
                    name="REGINALD_MODEL",
                    value="openai",
                ),
                containerinstance.EnvironmentVariableArgs(
                    name="SLACK_APP_TOKEN",
                    secure_value=config.get_secret("SLACK_APP_TOKEN"),
                ),
                containerinstance.EnvironmentVariableArgs(
                    name="SLACK_BOT_TOKEN",
                    secure_value=config.get_secret("SLACK_BOT_TOKEN"),
                ),
            ],
            ports=[
                containerinstance.ContainerPortArgs(
                    port=80,
                    protocol=containerinstance.ContainerGroupNetworkProtocol.TCP,
                ),
            ],
            resources=containerinstance.ResourceRequirementsArgs(
                requests=containerinstance.ResourceRequestsArgs(
                    cpu=2,
                    memory_in_gb=8,
                ),
            ),
        ),
    ],
    os_type=containerinstance.OperatingSystemTypes.LINUX,
    resource_group_name=resource_group.name,
    restart_policy=containerinstance.ContainerGroupRestartPolicy.ALWAYS,
    sku=containerinstance.ContainerGroupSku.STANDARD,
    volumes=[],
)
