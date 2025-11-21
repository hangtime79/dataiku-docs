Local MCP
#########

The Local MCP tool allows a Model Context Protocol (MCP) server to be run locally, with its tools selectively made available to agents.

Prerequisites
=============

Configure a code environment with the following specifications:

* Python version `3.10` or higher
* The `fastmcp` package version `2.0` or higher
* Containerized execution and AlmaLinux 9 or higher are recommended. The **Agent MCP server** runtime addition installs `uvx` and `npx` to help start most MCP servers.

Configuration
=============

Create a tool with type "Local MCP". Then the configuration of the tool involves two main steps:

* Define the **command**, **arguments**, and **environment variables** used by the MCP server process in the tool's settings.

.. note::
    Most MCP servers provide a JSON configuration file/example. Fill the configuration automatically using the `Paste config` button.

* The **Load tools** button loads the list of tools exposed by the MCP server. Each tool can then be disabled individually.

Usage
=====

Add the Local MCP tool to an agent like any other tool. When running, the agent directly sees and uses each enabled MCP server tool as a regular standalone tool.

Security
========

The Local MCP tool runs under the querying user's identity (see :doc:`/user-isolation/index`) and therefore with that user's permissions / accesses.

An administrator may disable the creation/edition of Local MCP Server tools, or restrict it to only administrators in Administration > Settings > LLM Mesh.

Some MCP server runners, such as `uvx` and `npx`, download the server's code every time they start. To control updates, you can pin the version of the MCP server.
