Foreword
********

Developing a plugin can be a complex and time-consuming process.
Creating a dedicated instance solely for plugin development is recommended
to ensure that your plugin development is smooth and efficient.
Doing so allows you to test and refine the plugin without affecting other instances,
thus minimizing the risk of negative effects on other users.

When you develop a plugin on an instance, it becomes available to all users immediately.
Moreover, having a separate environment for plugin development will enable you
to prevent users from accessing an incomplete or in-progress plugin,
which can help you avoid any confusion or frustration on their part.
Any modifications made to the plugin will be immediately visible to all users on that instance.

In addition to these benefits,
having a separate environment for plugin development provides the added advantage of allowing you
to test new plugins and customizations without affecting the stability or uptime of your production environment.
This means that you can ensure that the plugin works as intended without any unintended consequences or
disruptions to your production environment.

In summary, creating a dedicated instance for plugin development is a best practice to help you avoid issues arising
from incomplete or untested plugins.
Following this practice, you can develop your plugins in a safe and stable environment and
ensure they work seamlessly before deploying them to your production environment.
We recommend setting up a dedicated instance,
and you will find more best practices in :doc:`this tutorial<./setup-a-dev-env/index>`.

Plugin visibility
=================

Since **Dataiku 14.2**, plugin visibility can be turned on on demand.
To do so, go to the Plugins page, select the plugin you want, click on the Settings tab, and then select Permissions,
as shown in :ref:`Fig. 1<plugins/tutorials/forewords/foreword-plugin-visibility>`. 

.. _plugins/tutorials/forewords/foreword-plugin-visibility:

.. figure:: assets/foreword-plugin-visibility.png
    :align: center
    :class: with-shadow image-popup
    :alt: Fig. 1: How to manage plugin visibility.

    Fig. 1: How to manage plugin visibility.


.. note::

    This is a UI feature that only impacts the visibility of items.
    It does not prevent users from creating the component using the API.

    As this is a UI feature, not all components are affected by this setting.
    Please refer to :doc:`the documentation<refdoc:plugins/permissions>` to see which components this setting impacts.

If you remove the **Default** permission, the plugin component will be visible only to you and the administrator.
You can also add a group to which the plugin will be visible.
Select a group in the dropdown and click the **Grant access to group** button to do so.

.. warning::

    Although this feature can hide a component in development, we still recommend having a dedicated instance. 