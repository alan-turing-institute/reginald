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