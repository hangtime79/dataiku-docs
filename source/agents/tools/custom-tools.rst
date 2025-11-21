Writing your own tool
########################

In addition to the prebuilt tools, you can build your own, in two different ways:

1. Using an inline code tool in DSS
2. Writing a plugin

Inline code tool
=================

Custom Tools can be written inline in Python code within DSS.
They then become available for users who can leverage these tools without having to write or manage code.

Plugin tools
=============

Custom Tools can be written in plugins.
Like with all plugin components in Dataiku, this allows builders to write the code once and define the parameters.
They then become available as code-free interfaces for users who can leverage these tools without having to write or manage code.

We recommend that you look at our sample Google Search tool to get information on how to write a custom tool.
