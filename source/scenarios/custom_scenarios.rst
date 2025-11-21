Custom scenarios
#################

Instead of being simply step-based, custom scenarios are a full-fledged Python program which may execute everything that DSS scenarios can, while providing the user with full configurability and advanced logic capabilities.

What can a custom scenario do
===============================

A custom scenario can:

* Execute all steps that can be defined in a "step-based scenario". For more information, see :doc:`steps`.

* Read metadata about the executed steps, like:

	* Failure / Success
	* Count and types of warnings
	* Detailed list of built datasets, trained models, ...

* Read details about trained models (performance metrics, ...)

* Read detailed parameters of the trigger that initiated this scenario.

* Activate new versions of trained models

* Read metrics and checks status for datasets

* Read the build state: when was a dataset last built, a model last trained, ...

* Send custom messages through the reporters at any point of the scenario (not only at the beginning or end)


In addition, a custom scenario can use the whole internal and public Python API.

The details of the scenarios API can be found in :doc:`devguide:api-reference/python/scenarios`.

.. note::

        The scenario API cannot be used in a Python recipe/Jupyter notebook.

Examples
=========

Basic usage
------------

This custom scenario builds datasets and trains models. Note that a step-based scenario suffices for this usage.

.. code-block:: python

	from dataiku.scenario import Scenario

	# Create the main handle to interact with the scenario
	scenario = Scenario()

	# Build a dataset
	scenario.build_dataset("mydatasetname")

	# Build a partitioned data (this uses the partitions spec syntax)
	scenario.build_dataset("mydatasetname", partitions="partition1,partition2")

	# Train a model. The model id can be found in the URL of the model settings page
	scenario.train_model("epae130z")

Send custom reports
--------------------

Reports can be sent at any time of the scenario. You'll need to have a preconfigured messaging channel.

.. code-block:: python

	from dataiku.scenario import Scenario
	scenario = Scenario()

	message_sender = scenario.get_message_sender("channel-name")

	# You can then call send() with message params.
	# params are specific to each message channel types

	# SMTP mail example
	message_sender.send(sender="", recipient="", subject="", message="")

	# You can also call set_params to set params on the sender that will be reused for all subsequent 'send' calls
	message_sender.set_params(sender="dss@company.com", recipent="data-scientists@company.com")
	message_sender.send(subject="All is well", message="Scenario is working as expected")

	# Twilio SMS alert example
	message_sender.send(fromNumber="", toNumber="", message="")


You can also send message to Microsoft Teams. Here is an example where ``my-teams-channel`` is a preconfigured messaging channel:

.. code-block:: python

  from dataiku.scenario import Scenario
  scenario = Scenario()

  message_sender = scenario.get_message_sender("my-teams-channel")
  message_sender.send(message="Scenario is working as expected")

Here is another example that uses an ad-hoc channel:

.. code-block:: python

  from dataiku.scenario import Scenario
  scenario = Scenario()

  message_sender = scenario.get_message_sender(None, "msft-teams-scenario")
  message_sender.send(message="Scenario is working as expected", webhookUrl="Webhook URL of the Teams channel")

If you want to send an email message in HTML format, you can pass the parameter ``sendAsHTML=True`` in your send function. Here is an example where ``my-email-channel`` is a preconfigured messaging channel:

.. code-block:: python

  from dataiku.scenario import Scenario
  scenario = Scenario()

  message_sender = scenario.get_message_sender("my-email-channel")
  # some HTML-formatted text
  html_message = "<p style='color:orange'>Your scenario is running!</p><p>While waiting, check out this <a href='https://www.dataiku.com'>awesome website</a></p>"
  message_sender.send(subject="The scenario is doing well", message=html_message, sendAsHTML=True)
