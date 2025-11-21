ERR_MISC_EOPENF: Too many open files
####################################

DSS and its subprocesses hold more open file descriptors than the limit configured for this system/process/user.

Remediation
===========

This issue can only be fixed by a DSS administrator.

To fix this issue:

* Stop DSS, and make sure no processes are still running
* Check the allowed number of open files with ``ulimit -n`` (as the unix user that runs dss)
* `Increase that limit <https://www.cyberciti.biz/faq/linux-increase-the-maximum-number-of-open-files/>`_, ideally to 64,000
* Restart DSS

If this does not solve your issue, please report the issue to Dataiku support.
