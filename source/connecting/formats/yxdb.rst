YXDB
#####################

YXDB (.yxdb) is a file storage format produced by Alteryx products.

Dataiku can natively detect and read YXDB files and process them.

YXDB can contain fields of type Date and Date/Time. These fields do not hold any time-zone information. By default, these fields are read as strings but they can also be read as DSS dates by providing a time-zone.  
