Project Standards
#################

.. toctree::
    :maxdepth: 1

    settings
    reports
    
Project Standards changes how Enterprise customers ensure the quality of their projects in Dataiku. It integrates automated quality control directly into Dataiku’s design, deployment, and Govern flows to reduce the manual back and forth needed to review. 

Project Standards help large organizations:

* **Define organization-wide best practices**: Incorporate predefined checks or create your own customized checks.
* **Speed up project collaboration**: Strengthen your production environment by enforcing minimum quality thresholds for all deployments, whether through the Deployer or Govern Sign-off process. This significantly reduces manual quality controls, increasing scalability and enabling faster deployment of projects to automation.
* **Reduce production issues**: Promote and enforce best practices in a controlled, automated environment before project deployment. Designers can address common project issues themselves, without relying on inconsistently applied manual review.
* **Upskill teams building Dataiku projects**: Provide designers with interactive, in-product guidance that helps them understand and implement necessary changes to meet production-grade quality thresholds.


.. note::
    Project Standards is only available with a `Dataiku for Enterprise AI` license.

How it works
============

Instance administrators define organizational quality best practices using Project Standards checks. These checks are run and surfaced in a report during project design and at the start of the deployment journey (during bundle creation). Each check generates a severity, which communicates how important it is to meet corporate production standards.

Infrastructure administrators can choose to enforce project deployment controls based on Project Standards by defining the maximum acceptable severity level for a bundle to be deployable. They can also use Project Standards in conjunction with the Govern Sign Off process, as Project Standard report is synchronized automatically in Govern.

How to start
============

The first thing to do is to import checks and include them in scopes. Admins can manage that in the :doc:`settings </mlops/project-standards/settings>`.

Then, the checks can be run on projects or bundles and generate :doc:`reports </mlops/project-standards/reports>`.
