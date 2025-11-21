API Endpoint Tool
##################

This tool allows interaction with any API endpoint deployed via Dataiku.

It requires a single input: an API Endpoint that has been deployed through Dataiku.

To use this tool, the following conditions must be met:

- Authorization to query via the deployer must be granted within the deployment settings.

- The endpoint must have an OpenAPI specification that defines the input schema and includes detailed documentation for each parameter. This is required for the underlying LLM to understand how to interact effectively with the endpoint.
