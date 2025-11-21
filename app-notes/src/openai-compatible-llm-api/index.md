# Setting up a connection to an OpenAI-compatible LLM API

Some LLM providers offer an API compatible with OpenAI's.
When such a provider is not natively supported by DSS,
it may work to use the OpenAI or the Azure LLM connection to leverage that provider.
The Open AI connection may be useful for services offering multiple models accessible with a single endpoint & API key.
The Azure LLM connection may be useful for services offering multiple endpoints, each with one model ;
the API key can be specified either on the whole Azure LLM connection (default API key), or per endpoint.

## How-to

### Using an OpenAI connection

- Create a new OpenAI connection
- Specify as “Custom URL” the URL that exposes an OpenAI-compatible API (typically ending in `…/v1`)
- Disable all models that may have been automatically suggested
- Add custom models using the ID of the models you want to address, as specified by the provider
- Test the connection

### Using an Azure LLM connection

- Create a new Azure LLM connection
- Specify as "Target URI" the URL that exposes an OpenAI-compatible API *not* including the `…/v1`
- Enter the API key for the endpoint or the default API key
- Test the connection

## Example services

Services that have been observed to work using this setup:
- [Ollama](https://ollama.com), see [OpenAI compatibility](https://github.com/ollama/ollama/blob/main/docs/openai.md), using an OpenAI connection with a single custom URL.
- [OVHcloud](https://www.ovhcloud.com/) (in alpha phase), see
  [AI endpoints](https://blog.ovhcloud.com/enhance-your-applications-with-ai-endpoints/), using an Azure LLM connection with one endpoint per AI endpoint.

## Limitations

- Such a connection is portrayed throughout DSS as an OpenAI or an Azure LLM connection
- The API of the provider must be actually compatible.
  Some providers claim compatibility but actually require additional HTTP headers,
  use a different authentication mechanism, don't support token streaming, etc.
  Such setups may break in unpredictable ways. In particular, DSS follows the
  official OpenAI API and assumes the API abides by it. If the provider fails
  to keep up with the evolution of the API, it may break at some point.
- The [support tier](https://doc.dataiku.com/dss/latest/troubleshooting/support-tiers.html)
  for such a setup is [Not Supported](https://doc.dataiku.com/dss/latest/troubleshooting/support-tiers.html#not-supported).

