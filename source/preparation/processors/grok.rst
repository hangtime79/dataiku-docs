Extract with grok
#############################################

This processor extracts parts from a column using grok patterns and/or a set of regular expressions. The chunks to extract are delimited using named captures. 

Overview
==============

 * The processor comes with a list of integrated grok patterns. See `Supported grok patterns`_ below.
 * You can combine several grok patterns with regular expressions in the same processor.
 * You can use the Grok Editor window to write & preview the results of your regular expressions.

Syntax
==============

Named captures copy the matches into new columns.

With a grok pattern
-------------------

Syntax: ``%{Grok_Pattern_Name:named_capture}``

 * Example: 

  ``%{IP:clientIP}``

  .. image:: ../img/grok - 2.png
    :width: 400
    :alt: Alternative text

* Output: 

  +--------------+
  | clientIP     |
  +==============+
  | 83.149.9.216 |
  +--------------+

With a regular expression (regex)
---------------------------------

Syntax: ``(?<named_capture>custom_pattern)``

 * Example: 

  ``(?<firstWord>\w+)``

  .. image:: ../img/grok - 1.png
    :width: 400
    :alt: Alternative text

 * Output: 

  +-----------+
  | firstWord |
  +===========+
  | 2021      |
  +-----------+

.. note::
  Named captures only works with a full name (i.e: no ``“_”``, ``“-”`` or ``“ “`` allowed). 

Found column
==============

If you enable this option, a column named 'found' will contain a
boolean to indicate whether the pattern matched.

Some cases of application
==========================

1. Parsing DSS access logs:

 * Here is a data sample from DSS access.log:

+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Line                                                                                                                                                                                                                                                                                |
+=====================================================================================================================================================================================================================================================================================+
| "127.0.0.1 - - [15/Oct/2020:07:31:29 +0200] ""GET /bower_components/jquery/dist/jquery.min.js HTTP/1.1"" 200 34847 ""http://localhost:11200/home/"" ""Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36"""   |
+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| "127.0.0.1 - - [15/Oct/2020:07:31:29 +0200] ""GET /static/dataiku/css/style.css HTTP/1.1"" 200 341166 ""http://localhost:11200/home/"" ""Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36"""                |
+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| "127.0.0.1 - - [15/Oct/2020:07:31:29 +0200] ""GET /static/dataiku/css/style.css HTTP/1.1"" 200 341166 ""http://localhost:11200/home/"" ""Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36"""                |
+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

 * Regular expression: 
        .. code-block:: 
        
                %{IP:ip} - - \[%{HTTPDATE:HTTPDate}\]
                ""%{WORD:method} %{URIPATH:resourceURI} %{WORD}/%{NUMBER}"" 
                %{NUMBER:statusCode} %{NUMBER:noIdea} ""http:%{URIPATH}""
                ""%{GREEDYDATA:userAgent}"""


 * Output: 

  .. image:: ../img/grok-3.png
    :width: 800
    :alt: Alternative text


2. Parsing backend logs timestamp:

 * Here is a data sample from DSS backeng.log:

+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Line                                                                                                                                                                                                                          |
+===============================================================================================================================================================================================================================+
| [2021/09/15-15:12:09.776] [qtp1429351083-884] [DEBUG] [dku.tracing]  - [ct: 2] Start call: /api/discussions/get-discussion-counts [GET] user=admin [projectKey=S3DSSVSELK objectType=PROJECT objectId=S3DSSVSELK]             |
+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+ 
| [2021/09/15-15:12:09.811] [qtp1429351083-884] [DEBUG] [dku.db.internal]  - [ct: 37] Created DSSDBConnection dssdb-h2-discussions-WboYz62                                                                                      |
+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| [2021/09/15-15:12:09.818] [qtp1429351083-884] [DEBUG] [dku.tracing]  - [ct: 44] Done call: /api/discussions/get-discussion-counts [GET] time=44ms user=admin [projectKey=S3DSSVSELK objectType=PROJECT objectId=S3DSSVSELK]   |
+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

 * Regular expression:

``(?<Timestamp>%{YEAR}[/-]%{MONTHNUM}[/-]%{MONTHDAY}[/-]%{HOUR}:?%{MINUTE}?:%{SECOND})``

 * Output:

.. image:: ../img/grok-4.png
  :width: 400
  :alt: Alternative text

Supported grok patterns
========================

.. code::

    USERNAME [a-zA-Z0-9._-]+
    USER %{USERNAME:UNWANTED}
    INT (?:[+-]?(?:[0-9]+))
    BASE10NUM (?<![0-9.+-])(?>[+-]?(?:(?:[0-9]+(?:\.[0-9]+)?)|(?:\.[0-9]+)))
    NUMBER (?:%{BASE10NUM:UNWANTED})
    BASE16NUM (?<![0-9A-Fa-f])(?:[+-]?(?:0x)?(?:[0-9A-Fa-f]+))
    BASE16FLOAT \b(?<![0-9A-Fa-f.])(?:[+-]?(?:0x)?(?:(?:[0-9A-Fa-f]+(?:\.[0-9A-Fa-f]*)?)|(?:\.[0-9A-Fa-f]+)))\b

    POSINT \b(?:[1-9][0-9]*)\b
    NONNEGINT \b(?:[0-9]+)\b
    WORD \b\w+\b
    NOTSPACE \S+
    SPACE \s*
    DATA .*?
    GREEDYDATA .*
    #QUOTEDSTRING (?:(?<!\\)(?:"(?:\\.|[^\\"])*"|(?:'(?:\\.|[^\\'])*')|(?:`(?:\\.|[^\\`])*`)))
    QUOTEDSTRING (?>(?<!\\)(?>"(?>\\.|[^\\"]+)+"|""|(?>'(?>\\.|[^\\']+)+')|''|(?>`(?>\\.|[^\\`]+)+`)|``))
    UUID [A-Fa-f0-9]{8}-(?:[A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12}

    # Networking
    MAC (?:%{CISCOMAC:UNWANTED}|%{WINDOWSMAC:UNWANTED}|%{COMMONMAC:UNWANTED})
    CISCOMAC (?:(?:[A-Fa-f0-9]{4}\.){2}[A-Fa-f0-9]{4})
    WINDOWSMAC (?:(?:[A-Fa-f0-9]{2}-){5}[A-Fa-f0-9]{2})
    COMMONMAC (?:(?:[A-Fa-f0-9]{2}:){5}[A-Fa-f0-9]{2})
    IPV6 ((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?
    IPV4 (?<![0-9])(?:(?:25[0-5]|2[0-4][0-9]|[0-1]?[0-9]{1,2})[.](?:25[0-5]|2[0-4][0-9]|[0-1]?[0-9]{1,2})[.](?:25[0-5]|2[0-4][0-9]|[0-1]?[0-9]{1,2})[.](?:25[0-5]|2[0-4][0-9]|[0-1]?[0-9]{1,2}))(?![0-9])
    IP (?:%{IPV6:UNWANTED}|%{IPV4:UNWANTED})
    HOSTNAME \b(?:[0-9A-Za-z][0-9A-Za-z-]{0,62})(?:\.(?:[0-9A-Za-z][0-9A-Za-z-]{0,62}))*(\.?|\b)
    HOST %{HOSTNAME:UNWANTED}
    IPORHOST (?:%{HOSTNAME:UNWANTED}|%{IP:UNWANTED})
    HOSTPORT (?:%{IPORHOST}:%{POSINT:PORT})

    # paths
    PATH (?:%{UNIXPATH}|%{WINPATH})
    UNIXPATH (?>/(?>[\w_%!$@:.,~-]+|\\.)*)+
    #UNIXPATH (?<![\w\/])(?:/[^\/\s?*]*)+
    TTY (?:/dev/(pts|tty([pq])?)(\w+)?/?(?:[0-9]+))
    WINPATH (?>[A-Za-z]+:|\\)(?:\\[^\\?*]*)+
    URIPROTO [A-Za-z]+(\+[A-Za-z+]+)?
    URIHOST %{IPORHOST}(?::%{POSINT:port})?
    # uripath comes loosely from RFC1738, but mostly from what Firefox
    # doesn't turn into %XX
    URIPATH (?:/[A-Za-z0-9$.+!*'(){},~:;=@#%_\-]*)+
    #URIPARAM \?(?:[A-Za-z0-9]+(?:=(?:[^&]*))?(?:&(?:[A-Za-z0-9]+(?:=(?:[^&]*))?)?)*)?
    URIPARAM \?[A-Za-z0-9$.+!*'|(){},~@#%&/=:;_?\-\[\]]*
    URIPATHPARAM %{URIPATH}(?:%{URIPARAM})?
    URI %{URIPROTO}://(?:%{USER}(?::[^@]*)?@)?(?:%{URIHOST})?(?:%{URIPATHPARAM})?

    # Months: January, Feb, 3, 03, 12, December
    MONTH \b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\b
    MONTHNUM (?:0?[1-9]|1[0-2])
    MONTHNUM2 (?:0[1-9]|1[0-2])
    MONTHDAY (?:(?:0[1-9])|(?:[12][0-9])|(?:3[01])|[1-9])

    # Days: Monday, Tue, Thu, etc...
    DAY (?:Mon(?:day)?|Tue(?:sday)?|Wed(?:nesday)?|Thu(?:rsday)?|Fri(?:day)?|Sat(?:urday)?|Sun(?:day)?)

    # Years?
    YEAR (?>\d\d){1,2}
    # Time: HH:MM:SS
    #TIME \d{2}:\d{2}(?::\d{2}(?:\.\d+)?)?
    # I'm still on the fence about using grok to perform the time match,
    # since it's probably slower.
    # TIME %{POSINT<24}:%{POSINT<60}(?::%{POSINT<60}(?:\.%{POSINT})?)?
    HOUR (?:2[0123]|[01]?[0-9])
    MINUTE (?:[0-5][0-9])
    # '60' is a leap second in most time standards and thus is valid.
    SECOND (?:(?:[0-5]?[0-9]|60)(?:[:.,][0-9]+)?)
    TIME (?!<[0-9])%{HOUR}:%{MINUTE}(?::%{SECOND})(?![0-9])
    # datestamp is YYYY/MM/DD-HH:MM:SS.UUUU (or something like it)
    DATE_US %{MONTHNUM}[/-]%{MONTHDAY}[/-]%{YEAR}
    DATE_EU %{MONTHDAY}[./-]%{MONTHNUM}[./-]%{YEAR}
    ISO8601_TIMEZONE (?:Z|[+-]%{HOUR}(?::?%{MINUTE}))
    ISO8601_SECOND (?:%{SECOND}|60)
    TIMESTAMP_ISO8601 %{YEAR}-%{MONTHNUM}-%{MONTHDAY}[T ]%{HOUR}:?%{MINUTE}(?::?%{SECOND})?%{ISO8601_TIMEZONE}?
    DATE %{DATE_US}|%{DATE_EU}
    DATESTAMP %{DATE}[- ]%{TIME}
    TZ (?:[PMCE][SD]T|UTC)
    DATESTAMP_RFC822 %{DAY} %{MONTH} %{MONTHDAY} %{YEAR} %{TIME} %{TZ}
    DATESTAMP_RFC2822 %{DAY}, %{MONTHDAY} %{MONTH} %{YEAR} %{TIME} %{ISO8601_TIMEZONE}
    DATESTAMP_OTHER %{DAY} %{MONTH} %{MONTHDAY} %{TIME} %{TZ} %{YEAR}
    DATESTAMP_EVENTLOG %{YEAR}%{MONTHNUM2}%{MONTHDAY}%{HOUR}%{MINUTE}%{SECOND}

    # Syslog Dates: Month Day HH:MM:SS
    SYSLOGTIMESTAMP %{MONTH} +%{MONTHDAY} %{TIME}
    PROG (?:[\w._/%-]+)
    SYSLOGPROG %{PROG:program}(?:\[%{POSINT:pid}\])?
    SYSLOGHOST %{IPORHOST}
    SYSLOGFACILITY <%{NONNEGINT:facility}.%{NONNEGINT:priority}>
    HTTPDATE %{MONTHDAY}/%{MONTH}/%{YEAR}:%{TIME} %{INT}

    # Shortcuts
    QS %{QUOTEDSTRING:UNWANTED}

    # Log formats
    SYSLOGBASE %{SYSLOGTIMESTAMP:timestamp} (?:%{SYSLOGFACILITY} )?%{SYSLOGHOST:logsource} %{SYSLOGPROG}:

    MESSAGESLOG %{SYSLOGBASE} %{DATA}

    COMMONAPACHELOG %{IPORHOST:clientip} %{USER:ident} %{USER:auth} \[%{HTTPDATE:timestamp}\] "(?:%{WORD:verb} %{NOTSPACE:request}(?: HTTP/%{NUMBER:httpversion})?|%{DATA:rawrequest})" %{NUMBER:response} (?:%{NUMBER:bytes}|-)
    COMBINEDAPACHELOG %{COMMONAPACHELOG} %{QS:referrer} %{QS:agent}
    COMMONAPACHELOG_DATATYPED %{IPORHOST:clientip} %{USER:ident;boolean} %{USER:auth} \[%{HTTPDATE:timestamp;date;dd/MMM/yyyy:HH:mm:ss Z}\] "(?:%{WORD:verb;string} %{NOTSPACE:request}(?: HTTP/%{NUMBER:httpversion;float})?|%{DATA:rawrequest})" %{NUMBER:response;int} (?:%{NUMBER:bytes;long}|-)


    # Log Levels
    LOGLEVEL ([A|a]lert|ALERT|[T|t]race|TRACE|[D|d]ebug|DEBUG|[N|n]otice|NOTICE|[I|i]nfo|INFO|[W|w]arn?(?:ing)?|WARN?(?:ING)?|[E|e]rr?(?:or)?|ERR?(?:OR)?|[C|c]rit?(?:ical)?|CRIT?(?:ICAL)?|[F|f]atal|FATAL|[S|s]evere|SEVERE|EMERG(?:ENCY)?|[Ee]merg(?:ency)?)

