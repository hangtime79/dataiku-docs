ERR_MISC_ENOSPC: Out of disk space
##################################

DSS tries to do some operation for which it needs disk space, but the disk is full.
You may also see the message ``No space left on device``, which carries the same meaning.

Remediation
===========

This issue can only be fixed by a DSS administrator.

A DSS administrator needs to free up some disk space on the partition where the :doc:`DSS data directory </operations/datadir>` is located. 

.. warning::

	After such an error, you MUST restart DSS. Failure to do so may leave some functionality of DSS non-functional.
