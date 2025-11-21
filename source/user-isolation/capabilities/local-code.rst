Local code isolation
######################

Local code isolation is the fundamental component of User Isolation Framework.

Each time a user submits code to be executed by DSS, DSS will use *sudo* to execute the code as this end-user. Standard UNIX permissions and isolation guarantee that the user cannot access any forbidden information in the DSS data dir.
