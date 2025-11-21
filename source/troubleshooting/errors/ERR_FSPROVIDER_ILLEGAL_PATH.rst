ERR_FSPROVIDER_ILLEGAL_PATH: Illegal path for that file system
##########################################################################

The specified path is not supported on that file system.

For example, ``.`` and ``..`` are not usable on an S3 file system.
S3 is not an actual file system. It identifies objects with keys,
which may or may not look like a path on a file system. You can have a single
object with key ``a/b/c.txt``, which will be presented by many tools, DSS included,
as a folder ``a``, containing a folder ``b``, containing a file ``c.txt``.
Having a ``.`` or ``..`` in a key will not work as on a Unix- or Windows-style
file system and is therefore not supported.


Remediation
===========

Fix the faulty path. If that path was set at the connection level, you will need
DSS administrator access to fix it.
