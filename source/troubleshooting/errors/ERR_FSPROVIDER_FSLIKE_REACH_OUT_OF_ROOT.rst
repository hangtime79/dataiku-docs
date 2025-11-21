ERR_FSPROVIDER_FSLIKE_REACH_OUT_OF_ROOT: Illegal attempt to access data out of connection root path
############################################################################################################

The configuration of a dataset or managed folder illegally tries to reach outside of its assigned root path, by using ``..`` in its path.


Remediation
===========

Check the settings of the dataset or managed folder.

In some cases, the configuration issue can be at the connection level, in which case it must be fixed by your administrator.
