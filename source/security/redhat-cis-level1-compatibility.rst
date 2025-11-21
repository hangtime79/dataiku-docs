:orphan:

Compatibility of DSS with CIS Benchmark Level 1 on RHEL / CentOS / AlmaLinux / Rocky Linux / Oracle Linux 
##########################################################################################################

Dataiku DSS is compatible with all recommendations from the CIS CentOS / RedHat / AlmaLinux / Rocky Linux / Oracle Linux Benchmark Level 1, with the exceptions and cautions listed below.

Ensure noexec option set on /tmp partition
============================================

Enabling this option will interfere with the ability to compile Python and R packages. It will usually fully prevent using R, and will hinder the ability to leverage third-party Python packages that require compilation.

Ensure default user umask is 027 or more restrictive
=====================================================

If using this recommendation, and if DSS User Isolation is enabled, care must be taken to ensure that impersonated users can access both the installdir and datadir. This can be done by running chmod after untarring the DSS archive. Failure to do so would prevent most features of DSS from working.

Ensure users' home directories permissions are 750 or more restrictive
=======================================================================

If the Dataiku DSS datadir is in the DSS user's home directory, and if DSS User Isolation is enabled, care must be taken to ensure that impersonated users can access both the installdir and datadir. This can be done either by ensuring that impersonated users belong to the group of the homedir, or by changing the DSS user's homedir permissions to 751
