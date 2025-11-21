ERR_FSPROVIDER_CANNOT_CREATE_FOLDER_ON_DIRECTORY_UNAWARE_FS: Cannot create a folder on this type of file system
####################################################################################################################################

You are trying to create an empty folder on a system that does not support it.

For example, S3 is not an actual file system. It identifies objects with keys,
which may or may not look like a path on a file system. You can have a single
object with key ``a/b/c.txt``, which will be presented by many tools, DSS included,
as a folder ``a``, containing a folder ``b``, containing a file ``c.txt``.
But them, you cannot have an empty folder ``e/f/``, you need an actual file
``e/f/g.txt`` that will get presented as a folder ``e/f``.

