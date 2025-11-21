Continuous sync
###############

A continuous Sync recipe processes messages from a streaming endpoint and passes them either to another streaming endpoint, or stores them in a dataset. The main use is to capture a stream into a dataset, to perform analyses on it.

A continuous sync recipe offers exactly-once guarantees when the following conditions are met:

* the input streaming endpoint is replayable
* the output can be atomically checkpointed

A example of such a case is when the input is a Kafka streaming endpoint and the output a file-based dataset.

Partitioning
======================

If the output dataset is partitioned with a single time dimension, then the continuous sync recipe writes the messages in a partition corresponding to the time where the message was received from the streaming endpoint. For example, with an hourly partitioning, messages arriving between 2020-07-11 08:00:00 and 2020-07-11 08:59:59 will go into the 2020-07-11-08 partition.
