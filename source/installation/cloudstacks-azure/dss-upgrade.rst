Upgrades of DSS instances
###########################

Fleet Manager manages upgrades of DSS. Upgrades are always done under administrator control and are not performed automatically.

To upgrade an instance:

* Go to the settings of the instance
* In the "Version" field, select the new DSS version you want to upgrade to
* Reprovision the instance

Upon reprovisioning, DSS will start a new virtual machine with the new DSS version and will reattach the data volume to the new DSS version, performing any upgrade on the fly as required.

Updating the list of available versions
========================================

If your Fleet Manager instance has direct outgoing Internet access (without proxy), Fleet Manager will automatically fetch the list of newly available DSS versions, and these versions will appear directly in your Fleet Manager.

If this is not the case, please contact your Dataiku Technical Account Manager or Customer Success Manager.