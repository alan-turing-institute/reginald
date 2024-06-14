param (
    [Parameter()]
    [string]$ResourceGroupName,

    [Parameter()]
    [string]$ContainerGroupName,

    [Parameter()]
    [string]$SubscriptionID,
)

$azureContext = Connect-AzAccount -Identity

Get-AzSubscription -SubscriptionId $SubscriptionID | Set-AzContext -Name 'MyContextName'

echo "Restarting the VM..."
Get-AzContainerGroup -ResourceGroupName $ResourceGroupName -Name $ContainerGroupName | Restart-AzContainerGroup
