Split URL (into protocol, host, port, ...)
#############################################

This processor splits the elements of an URL into multiple columns

A valid URL is in the form
``scheme://hostname[:port][/path][?querystring][#anchor]``

The output values are produced in columns prefixed by the input column
name.

If the input does not contain a valid URL, no output value is produced.
# Examples \* ``http://www.google.com/search?q=query#results`` \*
``ftp://ftp.server.com/pub/downloads/myfile.tar.gz``


.. pristine
