ERR_SQL_VERTICA_TOOMANYROS: Error in Vertica: too many ROS
############################################################

Your Vertica hit it limit of Read Optimized Stores (ROS) containers for a given projection.

Vertica organises data within projections, each of them based on data containers called ROS.
Vertica imposes a limit on the number of ROS that can be created for a given projection.

Vertica creates new ROS containers when ingesting data and periodically merges them
(an operation called "mergeout"). Inserting many times data before the mergeout happens
may lead to reaching the limit.

An important factor is also that DSS partitioning uses native Vertica partitioning and several
partitions will necessarily use several ROS. A large number of partitions may lead to
reaching the limit.

Remediation
===========

* Rerunning the failed recipe may work if the mergeout happened in the meantime
* You can avoid adding frequently data before the mergeout can happen
* Your database administrator can manually trigger the mergeout by running the SQL:
  ``SELECT DO_TM_TASK('mergeout');``
* If your dataset contains many small partitions, you can avoid this issue and improve
  performance by using less fine-grained partitioning schemes (for example by day rather than hour)
