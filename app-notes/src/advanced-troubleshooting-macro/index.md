# Running the Advanced Troubleshooting macro

This is a procedure that may be requested by Dataiku Support in order to deeply investigate the resource consumption of your workloads, typically when you run in performance/stability issues.

The steps must be performed with administration rights.

1. Install the following plugin in your DSS instance: <https://devupdate.dataiku.com/dss/14/plugins/advanced-troubleshooting/0.0.1/dss-plugin-advanced-troubleshooting-0.0.1.zip>

2. In a project, create a managed folder on a local filesystem connection

3. Create a scenario in that project

4. Add a step "Run macro", in which you run the "Gather troubleshooting data" macro

5. Select the folder you just created. Leave other options unchanged

6. Schedule this scenario to run every 5 minutes

7.  Let the scenario run for a few days. Wait for the issue to reoccur.

8. Disable the scheduling

9. From the folder, download all data (it may take a bit of time before the download starts)

10. Grab a new instance diag with full logs history

11. Send both the instance diag and the download of the folder data to the support ticket, using <https://dl.dataiku.com> (please don't forget to send the generated link)