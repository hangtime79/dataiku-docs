WARN_JVM_CONFIG_KERNEL_XMX_OVER_THRESHOLD: Xmx value for kernel over threshold
##############################################################################

If the maximum heap size (Xmx option) value for either kernel (JEK or FEK) is too big, it can lead to
potential memory exhaustion on the machine. This is because the allocated memory is multiplied by the
number of JEKs and FEKs. Therefore, it is advisable for users to avoid setting an excessively large
Xmx value for these kernels to prevent memory-related issues.

Remediation
===========

Modify the `fek.xmx` or `jek.xmx` option in the `$DSS_HOME/install.ini` file so it doesn't exceed 4g.
See :doc:`/operations/memory`.
