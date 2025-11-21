Project Standards reports
#########################

Content
=======

The Project Standards report is the summary of the checks run on your project.
You can consult the result of each check and some additional information about the check.

They are divided into 4 sections:

* **To review**: Checks that did not pass, organized by severity
* **Success**: Checks that passed, requiring no further action
* **Not applicable**: Checks that contain logic that does not apply to the project
* **Error**: Checks that failed in execution due to an internal or plugin error


Consult and (re)run a report
============================

A Project Standard report can be associated with a project or a bundle.

Project report
______________

You can consult the last report in the flow, using the "Project Standards" buttons. You can also open the Project Standards page using the button "Check Project Standards" in the Bundles page.

In the report, there is a button to run or rerun the Project Standards checks. Once the new report is computed, it will be saved and will replace the old one.

Use this report to see if there are any issues with the project to fix and take action accordingly.

Bundle report
_____________

The report is included in the bundle. If you open the bundle, you will see a tab "Project Standards" containing the report.

If Project Standards is configured, checks will automatically be run, and the report will be added when you create a new bundle.
You can't rerun a report in a bundle. You need to recreate a new bundle if you want to improve the report after fixing the issues.

You can consult the bundle report to see if there are any issues with the project to fix before publishing the bundle.

Bundle report for deployer
==========================

On the project deployer, you can also configure your infrastructure to prevent deployments according to the Project Standards report. 
The report of the bundle will be analyzed before any deployment, and if the Project Standards policy is not respected, you can choose to:

- Do nothing
- Show a warning message
- Block the deployment

You will find those options in the "Deployment policies" tab of the infrastructure.
