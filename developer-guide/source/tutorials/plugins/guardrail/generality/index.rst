Creating a custom guardrail
***************************

When using an agent, your company may want to control the LLM.
There are various ways to do this.
Custom guardrails are plugin components that allow the user to control the LLM.
Custom Guardrails can, for example:

* Rewrite the query before submitting it to the LLM.
* Rewrite the response after having an answer from the LLM.
* Ask an LLM to retry or rewrite its answer by providing additional context/instructions.
* Add information into the trace of the LLM or in the audit log.
* Act on a query to take action before calling the LLM.

This tutorial presents a simple use case for implementing a custom guardrail but explains how to implement other use cases.

Prerequisite
============

* Dataiku >= 13.4  (13.4.4 if you want to create your guardrail visually)
* develop plugin permission
* A connection to an LLM, preferably an OpenAi connection
* Python >= 3.9

Introduction
============
A custom guardrail is a plugin component that provides additional capability to an LLM.
Depending on the context, there are four main ways to act, each configurable separately.
In this tutorial, you will learn how to create a custom guardrail,
configure it to tailor it to fit your needs and code the behavior.

To develop a Custom Guardrail, you must first create a plugin (or use an existing one).
Go to the main menu, click the **Plugins** menu, and select the **Write your own** from the **Add plugin** button.
Then, choose a meaningful name, such as ``toolbox``.
Once the plugin is created, click the **Create a code environment** button and select Python as the default language.
Once you have saved the modification, go to the **Summary** tabs to build the plugin code environment.
The custom guardrail will use this code environment when it is used.

Click the **+ New component** button, and choose the **LLM Guardrail** component in the provided list,
as shown in :ref:`Figure 1<tutorials-plugins-guard-rail-new-component-image>`.
Then, complete the form by choosing a meaningful **Identifier** and clicking the **Add** button.

.. _tutorials-plugins-guard-rail-new-component-image:

.. figure:: ./assets/new-guard-rail-component.png
    :align: center
    :class: with-shadow image-popup
    :alt: Figure 1: New Guardrail component.

    Figure 1: New Guardrail component.



Alternatively, you can select the **Edit** tab and, under the ``toolbox`` directory,
create a folder named ``python-guardrails``.
This directory is where you will find and create your custom guardrail.
Under this directory, create a directory with a meaningful name representing your Guardrail component.

Creating the Guardrail
=======================

A Guardrail is created by creating two files: ``guardrail.py`` and ``guardrail.json``.
The JSON file contains the configuration file, and the Python file is where you will code the behavior of the Guardrail.

Configuring the LLM Guardrail
------------------------------

:ref:`Code 1<tutorials-plugins-guard-rail-generality-default-configuration-code>` shows the global shape of the configuration file;
highlighted lines are specific to the Guardrail component.

.. literalinclude:: ./assets/default.json
    :language: json
    :caption: Code 1: default configuration file -- ``guardrail.json``
    :name: tutorials-plugins-guard-rail-generality-default-configuration-code
    :emphasize-lines: 7-14


All these four parameters are booleans.

Setting the ``operatesOnQuery`` parameter to ``true`` will trigger this guardrail on every input query before it is fed to the LLM.

Setting the ``operatesOnResponses`` parameter to ``true`` will trigger this guardrail on every response after the LLM inference happens.

Setting the ``mayRespondDirectlyToQueries`` parameter to ``true`` will indicate that the guardrail can respond directly to queries, skipping the rest of the pipeline.

Setting the ``mayRequestRetryOnResponses`` parameter to ``true`` will indicate that the guardrail can retry the processing of responses after a failure.

These parameters can also be configured via strings with two options ``BasedOnParameterName`` and ``BasedOnParameterValue``.
For example, you can set ``operatesOnQueriesBasedOnParameterName`` and ``operatesOnQueriesBasedOnParameterValue``.
Possible values for ``operatesOnQueriesBasedOnParameterName`` come from the ``param`` section.

In this tutorial, you will create a simple guardrail that can:

* Add an instruction before calling the LLM.
* Act on an LLM's response and rewrite it before sending the response to the user.

Your guardrail will have two dedicated parameters: ``instruction`` for the first case,
``LLM`` for rewriting the response, and an ``extraFormatting`` parameter for the second use case.
:ref:`Code 2<tutorials-plugins-guard-rail-generality-configuration-code>` shows the guardrail's configuration.

.. literalinclude:: ./assets/guardrail.json
    :language: json
    :caption: Code 2: configuration file -- ``guardrail.json``
    :name: tutorials-plugins-guard-rail-generality-configuration-code

Coding the Guardrail
---------------------

To code a guardrail, you must create a class derived from the ``BaseGuardRail`` class.
In this new class, the only mandatory function is ``process``.
This is where you will code your guardrail.
You can access the plugin's configuration by creating the ``set_config`` function.
:ref:`Code 3<tutorials-plugins-guard-rail-generality-set-config-code>` shows how to deal with these configuration parameters.

.. literalinclude:: ./assets/guardrail.py
    :language: python
    :caption: Code 3: Processing the configuration -- ``guardrail.py``
    :name: tutorials-plugins-guard-rail-generality-set-config-code
    :lines: 8-13


:ref:`Code 4<tutorials-plugins-guard-rail-generality-guardrail-code>` shows a way to implement a guardrail, considering the configuration.
Suppose you want to reduce the cost of an agent;
you can activate the **operatesOnQueries** parameter and add "Please answer in one sentence" to each query sent to the LLM,
as shown in :ref:`Figure 2<tutorials-plugins-guard-rail-generality-reduce-the-cost-image>`.

.. literalinclude:: ./assets/guardrail.py
    :language: python
    :caption: Code 4:  Guardrail code -- ``guardrail.py``
    :name: tutorials-plugins-guard-rail-generality-guardrail-code

.. _tutorials-plugins-guard-rail-generality-reduce-the-cost-image:

.. figure:: ./assets/format-answer.png
    :align: center
    :class: with-shadow image-popup
    :alt: Figure 2: Option for changing the initial query.

    Figure 2: Option for changing the initial query.

Suppose you want to ensure that your agent will respond using a JSON format;
you can configure it,
as shown in :ref:`Figure 3<tutorials-plugins-guard-rail-generality-format-answer-image>`.

.. _tutorials-plugins-guard-rail-generality-format-answer-image:

.. figure:: ./assets/format-answer.png
    :align: center
    :class: with-shadow image-popup
    :alt: Figure 3: Option for formatting the answer.

    Figure 3: Option for formatting the answer.

If you want to see your guardrail in action,
you can create a code agent (or a visual one if you prefer) with the code provided
in :ref:`Code 5<tutorials-plugins-guard-rail-generality-code-agent-code>`.
Then, add your guardrail in your agent's **Settings** tab.
Using the **Quick test** tab, you will see your guardrail modifying the query and the answer according to your settings.

.. dropdown:: :download:`code-agent.py<./assets/code-agent.py>`

    .. literalinclude:: ./assets/code-agent.py
        :language: python
        :caption: Code 5:  Code agent
        :name: tutorials-plugins-guard-rail-generality-code-agent-code

Conclusion
==========

Congratulations on finishing the tutorial on creating a custom guardrail in Dataiku.
Creating a custom guardrail for a language model (LLM) greatly improves your ability to customize
and refine responses based on your unique needs.
Start by applying these specific guardrails to enhance your interactions with the LLM.
This method ensures your queries remain precise and accurate, leading to responses that meet your expectations.
The various configuration options allow for flexibility across different applications,
enabling you to instruct the LLM to be brief or to follow particular formatting rules.

Here is the complete code of this tutorial:

.. dropdown:: :download:`guardrail.json<./assets/guardrail.json>`
    :open:

    .. literalinclude:: ./assets/guardrail.json
        :language: json

.. dropdown:: :download:`guardrail.py<./assets/guardrail.py>`
    :open:

    .. literalinclude:: ./assets/guardrail.py
        :language: python


