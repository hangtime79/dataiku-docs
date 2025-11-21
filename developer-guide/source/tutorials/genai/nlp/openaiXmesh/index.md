# Using standard OpenAI API calls via the LLM Mesh

An OpenAI-compatible API {doc}`Python client </concepts-and-examples/llm-mesh>` is available for text completion requests through the LLM Mesh. The LLM Mesh provides a governed way to access multiple providers. Instead of handling separate API keys and endpoints for each provider, you can use the LLM Mesh to:

- Access multiple models using OpenAI's standard Python format ..
- while maintaining centralized governance, monitoring and cost control ...
- and easily switching between different LLM providers


## Prerequisites

Before starting, ensure you have:

- Dataiku >= 13.2
- A valid Dataiku API key
- Project permissions for "Read project content" and "Write project content"
- An existing OpenAI LLM Mesh connection
- Python environment with the `openai` package installed (tested with version 1.3.0)

(tutorials/nlp/openAIXmesh/client)=
## OpenAI client for the LLM Mesh

Set up the OpenAI client by pointing to its LLM Mesh configuration. You will need several pieces of information for access and authentication:

- A public Dataiku URL to access the LLM Mesh API
- An API key for Dataiku
- The LLM ID

```python
from openai import OpenAI

# Specify the Dataiku OpenAI-compatible public API URL, e.g. http://my.dss/public/api/projects/PROJECT_KEY/llms/openai/v1/
BASE_URL = ""

# Use your Dataiku API key instead of an OpenAI secret
API_KEY = ""

# Fill with your LLM id - to get the list of LLM ids, you can use dataiku.api_client().project.list_llms()
LLM_ID = "" 

# Initialize the OpenAI client
client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY
)

# Default parameters
DEFAULT_TEMPERATURE = 0
DEFAULT_MAX_TOKENS = 500
```

```{tip}
In case you need find the `LLM ID`, there's a standard way to look up all available LLM Mesh configured APIs using the `dataiku` client. Use the `project.list_llms()` method and note down the OpenAI model you want to use. It will look something like `openai:CONNECTION-NAME:MODEL-NAME`.
```

## Making requests to OpenAI via LLM Mesh

Now you can make requests to the LLM just like you would with the standard OpenAI API:

```python

# Create a prompt

context = '''You are a capable ghost writer 
  who helps college applicants'''

content = '''Write a complete 350-word short essay 
  for a college application on the topic - 
  My first memories.'''


prompt = [
    {"role": "system", 
      "content": context}, 
    {'role': 'user',
      'content': content}
]

# Send the request
try:
    response = client.chat.completions.create(
        model=LLM_ID,
        messages=prompt,
        temperature=DEFAULT_TEMPERATURE,
        max_tokens=DEFAULT_MAX_TOKENS
    )
    
    print(response.choices[0].message.content)
except Exception as e:
    print(f"Error making request: {e}")
```

## Wrapping up

Now that you have the basic setup working, you can:

- Experiment with different prompts and parameters - here's what is [available](https://developer.dataiku.com/latest/concepts-and-examples/llm-mesh.html#openai-compatible-api)
- Use other LLM providers available through the LLM Mesh
- Try chunking longer responses by using the `stream` parameter as shown in {ref}`Code 1<tutorials-genai-nlp-openaiXmesh-code-streaming>`

````{dropdown} [streaming.py](assets/streaming.py)
:open:
```{literalinclude} assets/streaming.py
:language: python
:caption: Code 1 -- Longer code block with streaming example
:name: tutorials-genai-nlp-openaiXmesh-code-streaming
```
````

Remember that all requests go through the LLM Mesh, which provides monitoring and governing capabilities while maintaining the familiar OpenAI API interface.