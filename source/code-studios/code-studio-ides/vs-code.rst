Visual Studio Code
##################

In this section, we will define a Code Studio template to run Visual Studio Code to interactively edit and debug Python recipes, libraries, ...

Create a Code Studio template
=============================

* In "Administration > Code Studios", click **Create Code Studio template** and create a new template named ``vscode-template``
* In the "Definition" tab, click on **Add a block** and select ``Visual Studio Code``
* Click **Build**

Then in the "General" tab, you can grant permission to specific DSS groups (or all) to control which user can make Visual Studio Code runtimes. The selected users can now create new Code Studios in their projects using this template.

Launch a Code Studio instance
=============================

After having built a Code Studio template, in a project:

* Ensure the project is associated with a cluster, either by setting a default cluster in "Administration > Settings > Containerized execution" or by setting a cluster for the project in its "Settings > Cluster selection."
* In the "Code Studios" section, click **New Code Studio**, select the ``vscode-template`` template, fill in a name and create the Code Studio.
* Once in the Code Studio, click **Start**.

After the Code Studio has started, you can access a Visual Studio Code server instance. Work done in the Code Studio will usually materialize as modified files in the container. These would disappear when the Code Studio is stopped, so in order to safe keep them, synchronizing them back to the DSS server's filesystem is needed with the **Sync files with DSS** button (see :ref:`synchronized_files`).

Edit a recipe
=============

In your Visual Studio Code file explorer, you will see a folder called "recipes" listing all your DSS project recipes, open one recipe, edit it and then click **Sync files with DSS**. Now check that the recipe content has been updated in the DSS flow.

Edit Project Libraries
======================

In your VS Code file explorer, you will see a folder called "project-lib-versioned". This folder contains all the files from your project Libraries. You can edit existing files/folders and create new ones. Click **Sync files with DSS** to save your changes to Dataiku.
