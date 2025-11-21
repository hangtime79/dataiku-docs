Code env permissions
######################

For each code env, on the Permissions panel, you can control who has the rights to manage and use the code environment.

**Owner.** This is the DSS user that owns the code environment and has all access/permissions by default.

**Usable by all.** By default, all DSS users on this instance can see this code environment and choose to use it. If you deselect this checkbox, you will be able to select which groups of users can view this code env in the list of possible code envs.

For each group defined in :doc:`Security <../security/index>`, you can also grant permissions to update the packages in the code environment, update user access to the code environment, and use (i.e. view in the list) the code environment.

.. note::

	The "use" permissions is advisory only. Not having the "use" permission will remove the code env from the list of possible code envs in the various code env selection dropdowns, but does not actually physically prevent you from using the code envs. This is especially true in the notebook where you can change the code env of a kernel.

	The "use" permission is mostly used to keep "clean" lists of blessed environments per group.

	The underlying binaries of a code env are structurally always readable and knowledgeable users can always use them.

	The update / manage permissions are, on the other hand, fully enforced.