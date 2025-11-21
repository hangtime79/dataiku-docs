WARN_GIT_PROJECT_NOT_MIGRATED: Projects - Unmigrated Git branches
##################################################################

Some projects in your Dataiku instance contain local Git branches that were last migrated using an older DSS version. These branches may not be compatible with the current version of DSS and could lead to unexpected behavior when switching or working on them.

Remediation
===========

Review the affected projects and their branches. For each branch listed:

- Open the project in Dataiku.
- Go to the **Version Control** page (this is also where you can check out branches).
- Check out the listed branch.
- Follow the migration prompt that appears to upgrade the branch to the current DSS version.

If the branch is no longer needed, you can delete it instead to reduce maintenance and avoid confusion.