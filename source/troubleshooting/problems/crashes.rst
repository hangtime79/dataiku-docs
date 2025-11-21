DSS crashes / The "Disconnected" overlay appears
#################################################

This problem can present the following symptoms:

* During normal work, the "Disconnected" overlay suddenly appears, and disappears after a few dozens of seconds
* While DSS was running properly, trying to connect now yields a "Gateway error" issue

This generally indicates that the "backend" process of DSS has crashed. When this happens, the "supervisord" process automatically restarts the backend, and it is back up after 20-60 seconds depending on the size of your instance.

