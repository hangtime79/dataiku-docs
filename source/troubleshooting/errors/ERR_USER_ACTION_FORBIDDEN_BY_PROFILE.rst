ERR_USER_ACTION_FORBIDDEN_BY_PROFILE: Your user profile does not allow you to perform this action
#################################################################################################

User profiles define the types of actions your are allowed to do from a licensing perspective.

This error usually happens when, as a READER or DATA_ANALYST, you are trying to build a Visual Machine Learning model.
For example, if your profile is READER or DATA_ANALYST, this error will happen if you attempt to
build a Visual Machine Learning model.

This error may also happen if your DSS administrator updated the DSS license. Your user profile may not 
exist anymore in the new license.


Remediation
===========

To solve this issue ask the DSS administrator to update the user profile (note that DESIGNER is 
the unlimited profile in most licenses).


See also :doc:`/security/user-profiles`
