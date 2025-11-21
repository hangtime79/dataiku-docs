WARN_JOBS_NO_LIMIT: Jobs - No limits set
########################################

There is no limit in the number of jobs. This may reduce performance if too many jobs run concurrently and if the instance is not correctly sized.

Remediation
===========

To improve global performance, size the number of jobs according to how many can run concurrently on the instance (depending on the RAM and CPU available).
This may require some testing to have a good value.
