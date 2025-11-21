Remote MCP
##########

The Remote MCP tool allows using a Model Context Protocol (MCP) server, with its tools selectively made available to agents.

Prerequisites
=============

Create a Remote MCP connection with the server URL set to the remote MCP server URL.

Authentication
~~~~~~~~~~~~~~

Most MCP servers require authentication through OAuth. To help configure OAuth, the Remote MCP connection page offers:

- OAuth configuration discovery: use this to easily setup endpoints, authentication method and scopes
- OAuth dynamic client registration: use this to register a client, this is especially useful if the OAuth provider doesn't have an interface to create OAuth clients

Users will have to go through the OAuth authorization flow the first time they use this connection through a Remote MCP tool.

Some OAuth providers return a new refresh token with every new access token. Enable "Rotate refresh tokens" in that case.

Configuration
=============

Create a tool with type "Remote MCP" and select the Remote MCP connection to use.

All tools are disabled by default. Each tool must be enabled individually to be made available to agents.

Usage
=====

Add the Remote MCP tool to an agent. When running, the agent sees and uses each enabled MCP server tool as a regular standalone tool.
