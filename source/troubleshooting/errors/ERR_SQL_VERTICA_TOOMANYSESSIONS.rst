ERR_SQL_VERTICA_TOOMANYSESSIONS: Error in Vertica: too many sessions open concurrently
######################################################################################

Your Vertica database has too many active sessions simultaneously accessing it.
The database imposes a fixed maximum on the number of simultaneous uses.

This maximum number of simultaneous connections might be too low or you may need
to run fewer connections in parallel.
Note in particular that building several partitions of a Vertica dataset in DSS
will result in the corresponding number of connections to the database.


Remediation
===========

You can reduce the number of connections used simultaneously by running fewer recipes
at the same time. For instance, you may want to schedule recipes at different times of
the day rather than starting many computations at the same moment.

Your DSS administrator can limit the number of concurrent activities on that Vertica
connection (in Administration > Connection, in the Connection's "Usage params") so
that additional activities will wait instead of failing with this error.

You can also ask your database administrator to increase the parameter controlling the
maximum number of simultaneous sessions (``MaxClientSessions`` in Vertica), it typically
defaults to 50. See the Vertica documentation for the steps to follow.
