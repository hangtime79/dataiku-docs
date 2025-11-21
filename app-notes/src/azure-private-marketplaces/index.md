---
title: "Azure private marketplaces"
---

In order to filter the offers their employees can use and install on Azure portal, some customers may put in place a private marketplace. This private marketplace will only display a selected list of offers that have been approved by the customer.

# Add a Fleet Manager offer to a private marketplace

The customer is able to add public offers to their marketplace easily. However, Fleet Manager offers are private. Here is a procedure to do so:

* Open Azure portal on the chosen subscription
* Launch a shell from Azure portal by clicking on the shell icon in the right section of the top bar
* Select *Powershell* and set the chosen subscription
* To retrieve the private store ID, run the following
```
Install-Module -Name Az.Marketplace
Get-AzMarketplacePrivateStore
```
* To set the parameters describing the offers, run
```
# $Params = @{
#    PrivateStoreId = '<private-store-id>'
#    offerId = 'dataiku.fleet-manager'
#    SpecificPlanIdsLimitation =@('fm-<fm-version>')
# }
# where <private-store-id> is the store ID retrieved at previous step
# and <fm-version> is the FM major version
# e.g.
$Params = @{
   PrivateStoreId = '7gh67884-1r56-44fb-a93d-030d4ae08b2d'
   offerId = 'dataiku.fleet-manager'
   SpecificPlanIdsLimitation =@('fm-14')
}
```
* To add the offer to the private marketplace, run
```
Set-AzMarketplacePrivateStoreOffer @Params
```
* The offer should now be visible in the customer private marketplace

## References
* [Azure Set-AzMarketplacePrivateStoreOffer documentation](https://learn.microsoft.com/en-us/powershell/module/az.marketplace/set-azmarketplaceprivatestoreoffer?view=azps-14.3.0)
