Messaging Channels Permissions
##############################

.. contents::
    :local:

In the *Administration > Settings > Collaboration > Notifications & Integration* section, for each channel, you can add or remove users or groups allowed to use that channel. A special *All users* group allows you to allow any logged in user to use the channel.
By default, channels are not restricted, i.e. channels are initialized with this special *all users* group.

The channel permissions apply to:

- scenario *send message* steps and reporters
- agent tool *send message*
- public api usage of the send message route (including the corresponding python API method)

The channel permissions do not apply in the following channel usage:

- Any Dataiku built-in notification (welcome email, LLM cost control notifications, project integration notifications...)
- Unified monitoring notifications
- Govern instances


The permissions are verified considering the user who is running the action:

- for scenarios, the 'run as' user (may be different from the user who manually triggered the scenario, when applicable)
- for an Agent Tool based recipe, this is the user who started the recipe, or the 'run as' user of the scenario that triggered the recipe when applicable
- When authenticating through a personal API key, authorization to use the channel will be based on the relevant user
- project or global API keys will be allowed to use the channel if the special *all users* group is authorized.
