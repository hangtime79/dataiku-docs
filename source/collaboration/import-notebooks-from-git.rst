Importing Jupyter Notebooks from Git
####################################

If you have Jupyter Notebooks that have been developed outside of DSS and are available in a Git repository, you can import these Notebooks inside a DSS project.

.. note::
	To configure your git credentials, please refer to the :ref:`git setup <git.setup>`

Importing a new Jupyter Notebook
==================================

* Go to the project's Notebook list
* Click New Notebook > Import from Git
* Enter the URL of the Git repository
* Optionally, specify a branch name
* Click on List Notebooks
* Select the Notebooks you want to import

When you click Import X Notebook(s), the repository is fetched and the notebooks are imported in your project.

For more details on working with Git remotes, see :doc:`git`

Notebook lifecycle
==================================

During a Notebook import, DSS will save the reference of the remote git repository.

If you want to save your local modifications back into the remote repository, you can manually push your changes to the referenced git.

* Go to the project's Notebook list
* Select one or multiple Notebooks
* Open the right panel in the Action section
* Open the Associated remote Git subsection
* Click on the button Commit and push
* DSS will check for potential conflicts
* Optionally, write a custom commit message
* Click on Push Notebook(s) to confirm

On the opposite, if you want to retrieve the latest modification from your remote git in your local Notebook, you can pull the referenced git.

* Go to the project's Notebook list
* Select one or multiple Notebooks
* Open the right panel in the Action section
* Open the Associated remote Git subsection
* Click on the button Pull
* DSS will check for potential conflicts
* Click on Pull Notebook(s) to confirm

.. note::
	In case a conflict is detected, DSS proposes to override either the **local file** on pull, or the **remote file** on push. More advanced conflict resolutions must be solved outside of DSS.
	
How to manage a moved or renamed file on the remote
=====================================================

If someone has renamed or moved a notebook that you have imported, you can reconsolidate it by editing the git reference in DSS

* Go to the project's Notebook list
* Select one Notebook
* Open the right panel in the Action section
* Open the Associated remote Git subsection
* Click on the button Edit
* Enter the URL of the Git repository
* Optionally, specify a branch name
* Enter the path and the remote name of the Notebook. (The local and the remote name of a notebook can differ)

Export a notebook created in DSS
=====================================================

If you want to add a local Notebook to a remote repository, you can associate a git reference to a Notebook

* Go to the project's Notebook list
* Select one Notebook
* Open the right panel in the Action section
* Open the Associated remote Git subsection
* Click on the button Add
* Enter the URL of the Git repository
* Optionally, specify a branch name
* Enter the path and the remote name of the Notebook. (The local and the remote name of a notebook can differ)

You now need to push your Notebook to add it to your remote repository

