WARN_JVM_CONFIG_XMX_IN_RED_ZONE: Sub optimal Xmx value
######################################################

When configuring the Java Virtual Machine, it is important to consider the maximum heap size (Xmx option).
If the maximum heap size is set to a value between 32g and 48g, there is a potential issue with memory usage.
When the maximum heap size exceeds 32g, compressed references, which help reduce memory usage, are disabled.
This means that larger references are stored in memory, resulting in less available heap memory. If the additional
memory allocated does not absorb the extra space taken by the larger references, it can lead to a situation where
there is less overall heap memory available for the application to use. It is worth noting that there is no
specific threshold at which this issue stops occurring, as it depends on the usage of the memory, but 48g is
generally considered high enough to mitigate this problem.

Remediation
===========

Modify the `xmx` option in the `$DSS_HOME/install.ini` file so it doesn't lie between 32g and 48g. See :doc:`/operations/memory`.
