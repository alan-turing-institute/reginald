param (
    [Parameter()]
    [string]$ResourceGroupName,

    [Parameter()]
    [string]$VMName,

    [Parameter()]
    [string]$SubscriptionID,

    [Parameter()]
    [string]$Action
)

$azureContext = Connect-AzAccount -Identity

Get-AzSubscription -SubscriptionId $SubscriptionID | Set-AzContext -Name 'MyContextName'

$VM = Get-AzVM -ResourceGroupName $ResourceGroupName -Name $VMName

if ($Action -eq "Start") {
    echo "Starting the VM..."
    Start-AzVM -ResourceGroupName $ResourceGroupName -Name $VMName
} elseif ($Action -eq "Stop") {
    echo "Turning off the VM..."
    Stop-AzVM -ResourceGroupName $ResourceGroupName -Name $VMName -Force
} else {
    Write-Error "Invalid action. Use 'Start' or 'Stop'."
}
