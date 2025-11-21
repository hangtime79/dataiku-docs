ERR_SQL_POSTGRESQL_TOOMANYSESSIONS: too many sessions open concurrently
#######################################################################

Your Postgres database has too many active sessions simultaneously accessing it.
The database imposes a fixed maximum on the number of simultaneous uses.

This maximum number of simultaneous connections might be too low or you may need
to run fewer connections in parallel.
Note in particular that building several partitions of a Postgres dataset in DSS
will result in the corresponding number of connections to the database.

Remediation
===========

You can reduce the number of connections used simultaneously by running fewer recipes
at the same time. For instance, you may want to schedule recipes at different times of
the day rather than starting many computations at the same moment.

Your DSS administrator can limit the number of concurrent activities on that Postgres
connection (in Administration > Connection, in the Connection's "Usage params") so
that additional activities will wait instead of failing with this error.

You can also ask your database administrator to increase the parameter controlling the
maximum number of simultaneous sessions. Refer to the
`postgres documentation <https://www.postgresql.org/docs/9.5/static/runtime-config-connection.html>`_
(choose according to your version) for how to change the maximum number of simultaneous connections.
