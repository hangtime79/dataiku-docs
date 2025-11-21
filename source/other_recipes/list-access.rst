List Access
############

The list access recipe lets you retrieve the :ref:`security tokens <document-level-security>` (here implemented with DSS group names) from a Sharepoint folder. To be more precise, this recipe lists the files from a Sharepoint folder, displays the Entra groups that have access to each file and provides the mapping between the Entra groups and the DSS groups.

This recipe is useful to create the input dataset, containing the security tokens, for the :doc:`embed recipe </generative-ai/knowledge/documents>`.

Settings
==============

A key configuration for the list access recipe is located in the settings, under the :doc:`/security/authentication/azure-ad` section. If you set the :ref:`Azure AD groups readable by <azure-ad-permissions>` setting to *Everybody*, it allows all the users to retrieve the DSS groups and their respective Azure AD mappings. As a result, running the list access recipe will leverage the existing mappings defined in DSS. However, you can run this recipe without this setting activated, but you will need to provide a :ref:`manual mapping dataset <list-access-inputs>` as a second input.

.. _list-access-inputs:

Inputs
==============

Here are the inputs that the list access recipe expects:

* *Sharepoint folder*: The folder the content of which will be listed alongside the mapping of the groups. This input is mandatory.
* *Manual mapping dataset* (Optional): You can provide a dataset containing the mapping between the DSS groups and the Entra groups. The expected format is the following: a column for the DSS group of type string and another column for the Entra groups in a JSON array format (ex: ["entra-group1", "entra-group2"]). This input is useful if the *Azure AD groups readable by* setting is set to *Nobody*, because you provide the mapping yourself. However, in case this setting is set to *Everybody*, the manual mapping you provide will be used as an additional source of mapping alongside the existing DSS group mappings. Finally, if you enter here a mapping for a DSS group that was already mapped to Azure AD groups by the admin, the manual dataset will override the existing.

Output columns
==============

Structure of the output dataset:

* *path*: Path to the file in the folder.
* *entra_groups*: List of Entra groups that have access to the file.
* *dss_groups*: DSS groups that are mapped to the Entra groups. These will be used as security tokens in the rest of the workflow. They are in a JSON array format and each DSS group name is prefixed by *dss_group* (ex: ["dss_group:tech-members", "dss_group:readers"])
* *error_details*: Error messages raised during the computation with a per file granularity.
