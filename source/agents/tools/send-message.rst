Send Message tool
##################

The **Send Message** tool sends a message through a Dataiku Messaging Channel.

The following channel types are supported:

* :ref:`scenario-reporter-mail`
* :ref:`scenario-reporter-slack`
* :ref:`scenario-reporter-teams`

Messages are defined using a **template**. The template format and available fields depend on the channel.

Message variables
==================

You can customize the message by defining variables that are applied to the template.

The tool supports the following types of variables:

**Tool input**
    Variables explicitly defined by the LLM calling the tool. These can be strings or numbers.
    You must provide a description for each variable so the LLM knows how to fill them.

**Context variable**
    Variables provided within the ``context`` of the calling agent.
    Useful for passing information you do not want to expose to the agent LLM (*e.g.* personally identifiable information).

**DSS variable**
    Variables available from the DSS environment (see :doc:`/variables/index`).

**Custom formula**
    New variables defined using DSS :doc:`/formula/index`.
    You can reuse any variable declared before the formula. Therefore, the order in which variables are defined matters.
    You can reorder variables by dragging and dropping them in the interface.

Maintaining complex templates can be error-prone. The tool includes a helper that flags:

* **Unused variables**: defined but never referenced in the template.
* **Undefined variables**: referenced in the template but never defined.

.. note::
    Depending on the channel type and settings, variables may also be available in additional fields. A help message will indicate when this is the case.


