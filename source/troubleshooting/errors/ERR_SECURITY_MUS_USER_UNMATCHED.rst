ERR_SECURITY_MUS_USER_UNMATCHED: The DSS user is not configured to be matched onto a system user
################################################################################################

When DSS impersonates a user, it must have a rule to determine the system
user name which it is supposed to impersonate. This error means no rule
has been configured for this user.

Remediation
===========

This issue can only be fixed by a DSS Administrator.

Select an impersonation matching rule in the administration panel for the faulty user.
See :doc:`User Isolation Concepts </user-isolation/concepts>`
for more information about identity mapping.
