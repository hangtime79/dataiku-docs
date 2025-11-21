Deployment Governance policies
##############################

.. note::
	The following information applies to both deployment of model versions on an API node and deployment of bundles on an Automation node.  

Once Dataiku Deployer is linked with your Dataiku Govern instance, you might define a governance policy for each Deployer Infrastructure.

.. image:: img/govern-policy.png

From the infrastructure settings, you can choose between 3 different governance policies that will apply for all deployments made on this infrastructure:

1. **Prevent the deployment of unapproved packages.** If the model version or the bundle is approved, its status will be updated and it can be deployed. If the model version or the bundle is abandoned or rejected, the workflow will be locked and deployment will be blocked. You will get an error asking you to complete the approval process before deployment.
2. **Warn and ask for confirmation before deploying unapproved packages.** You will receive a warning asking you if you really want to continue the deployment.
3. **Always deploy without checking.** You will be able to deploy regardless of the sign-off status. This is the default value.