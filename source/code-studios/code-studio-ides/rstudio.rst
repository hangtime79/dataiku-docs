RStudio Server
##############

In this section, we will define a Code Studio template to run RStudio Server to interactively edit and debug R recipes, libraries, ...

Create a Code Studio template
=============================

* In "Administration > Code Studios", click **Create Code Studio template** and create a new template named ``rstudio-template``
* in the "Definition" tab, click on **Add a block** and select ``RStudio``
* Click **Build**

Then in the "General" tab, you can grant permission to use to given DSS groups (or all) to control which user is allowed to make RStudio runtimes. The selected users can now create new RStudio Code Studios in their projects.

Launch a Code Studio instance
=============================

After having built a RStudio template:

* ensure the project is associated to a cluster, either by setting a default cluster in "Administration > Settings > Containerized execution" or by setting a cluster for the project in its "Settings > Cluster selection"
* In the "Code Studios" section, click **New Code Studio**, select the ``rstudio-template`` template, fill in a name, and create the Code Studio.
* once in the Code Studio, click **Start**

After the Code Studio has started, you can access a RStudio server instance. Work done in the Code Studio will usually materialize as modified files in the container. These would disappear when the Code Studio is stopped, so in order to safe keep them, synchronizing them back to the DSS server's filesystem is needed with the **Sync files with DSS** button (see :ref:`synchronized_files`).

Edit a recipe
=============

You will see a folder called "recipes" in your RStudio file explorer,
listing all your DSS project recipes, open one recipe, edit it, and then click **Sync files with DSS**.
Now check that the recipe content has been updated in the DSS flow.

Edit Project Libraries
======================

In your RStudio file explorer, you will see a folder called "project-lib-versioned". This folder contains all the files from your project Libraries. You can edit existing files/folders and create new ones. Click **Sync files with DSS** to save your changes to Dataiku.
