ERR_SECURITY_INVALID_PASSWORD: The password hash from the database is invalid
#############################################################################

The password hash retrieved from the database is not a valid hash.
The user password cannot be verified, the database may have been corrupted.

Remediation
===========

This issue can only be fixed by a DSS administrator.

If the ``DATA_DIR/config/users.json`` file has been modified manually,
restore the previous version.

Otherwise, use the administrator account to set a new password for the affected user.
If the admin account itself is corrupted, the API with may be used to do so.

