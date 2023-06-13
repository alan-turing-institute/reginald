import pulumi
from pulumi_azure_native import containerinstance, network, resources

# Get some configuration variables
stack_name = pulumi.get_stack()

# Create an resource group
resource_group = resources.ResourceGroup(
    "resource_group",
    resource_group_name=f"rg-reginald-{stack_name}-deployment"
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
                    name="SLACK_APP_TOKEN", value=""
                ),
                containerinstance.EnvironmentVariableArgs(
                    name="SLACK_BOT_TOKEN", value=""
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
                    cpu=0.5,
                    memory_in_gb=0.5,
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