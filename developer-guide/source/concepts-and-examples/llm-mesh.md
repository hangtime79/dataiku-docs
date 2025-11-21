(llm-mesh)=

```{eval-rst}
..
  this code samples has been verified on DSS: 13.2.0
  Date of check: 24/09/2024

  this code samples has been verified on DSS: 14.2.0
  Date of check: 10/09/2025
```

# LLM Mesh


The LLM Mesh is the common backbone for Enterprise Generative AI Applications. For more details on the LLM Mesh features of Dataiku, please visit {doc}`refdoc:generative-ai/index`.

The LLM Mesh API allows you to:

* Send completion and embedding queries to all LLMs supported by the LLM Mesh
* Stream responses from LLMs that support it
* Query LLMs using multimodal inputs (image and text)
* Query the LLM Mesh from LangChain code
* Interact with knowledge banks, and perform semantic search
* Create a fine-tuned saved model

## Read LLM Mesh metadata

### List and get LLMs
By default, {meth}`~dataikuapi.dss.project.DSSProject.list_llms()` returns a list of {class}`~dataikuapi.dss.llm.DSSLLMListItem`.

```{code-block} python
:name: ce/llm-mesh/get-llm-id
:caption: List and get LLMs

import dataiku

client = dataiku.api_client()
project = client.get_default_project()
llm_list = project.list_llms()
for llm in llm_list:
    print(f"- {llm.description} (id: {llm.id})")
```

### List LLMs with a purpose
In addition, you can list LLM with a defined purpose.

```{code-block} python
:name: ce/llm-mesh/native-llm-list-with-purpose
:caption: List LLMs with a purpose

import dataiku

client = dataiku.api_client()
project = client.get_default_project()
llm_list = project.list_llms(purpose="TEXT_EMBEDDING_EXTRACTION")
for llm in llm_list:
    print(f"- {llm.description} (id: {llm.id})")
```

(ce-llm-mesh-native-llm-completion-on-queries)=
## Perform completion queries on LLMs

### Your first simple completion query

This sample receives an LLM and uses a completion query to ask the LLM to "write a haiku on GPT models."

```python
import dataiku

# Fill with your LLM id. For example, if you have an OpenAI connection called "myopenai", LLM_ID can be "openai:myopenai:gpt-4o"
# To get the list of LLM ids, you can use project.list_llms() (see above)
LLM_ID = ""

# Create a handle for the LLM of your choice
client = dataiku.api_client()
project = client.get_default_project()
llm = project.get_llm(LLM_ID)

# Create and run a completion query
completion = llm.new_completion()
completion.with_message("Write a haiku on GPT models")
resp = completion.execute()

# Display the LLM output
if resp.success:
    print(resp.text)

# GPT, a marvel,
# Deep learning's symphony plays,
# Thoughts dance, words unveil.
```


### Multi-turn and system prompts

You can have multiple messages in the `completion` object, with roles

```python
completion = llm.new_completion()

# First, put a system prompt
completion.with_message("You are a poetic assistant who always answers in haikus", role="system")

# Then, give an example, or send the conversation history
completion.with_message("What is a transformer", role="user")
completion.with_message("Transformers, marvels\nOf the deep learning research\nAttention, you need", role="assistant")

# Then, the last query of the user
completion.with_message("What's your name", role="user")

resp = completion.execute()
```

### Multimodal input

Multimodal input is supported on a subset of the LLMs in the LLM Mesh:

* OpenAI
* Bedrock Anthropic Claude
* Azure OpenAI
* Gemini Pro

```python
completion = llm.new_completion()

with open("myimage.jpg", "rb") as f:
    image = f.read()

mp_message = completion.new_multipart_message()
mp_message.with_text("The image represents an artwork. Describe it as it would be described by art critics")
mp_message.with_inline_image(image)

# Add it to the completion request
mp_message.add()

resp = completion.execute()
```

### Completion settings

You can set settings on the completion query


```python
completion = llm.new_completion()
completion.with_message("Write a haiku on GPT models")

completion.settings["temperature"] = 0.7
completion.settings["topK"] = 10
completion.settings["topP"] = 0.3
completion.settings["maxOutputTokens"] = 2048
completion.settings["stopSequences"] = [".", "\n"]
completion.settings["presencePenalty"] = 0.6
completion.settings["frequencyPenalty"] = 0.9
completion.settings["logitBias"] = {
  1489: 60,  # apply a logit bias of 60 on token value "1489"
}
completion.settings["logProbs"] = True
completion.settings["topLogProbs"] = 3

resp = completion.execute()
```

### Response streaming

```python
from dataikuapi.dss.llm import DSSLLMStreamedCompletionChunk, DSSLLMStreamedCompletionFooter

completion = llm.new_completion()
completion.with_message("Please explain special relativity")

for chunk in completion.execute_streamed():
    if isinstance(chunk, DSSLLMStreamedCompletionChunk):
        print("Received text: %s" % chunk.data["text"])
    elif isinstance(chunk, DSSLLMStreamedCompletionFooter):
        print("Completion is complete: %s" % chunk.data)
```

## Text embedding

```python
import dataiku

EMBEDDING_MODEL_ID = "" # Fill with your embedding model id, for example: openai:myopenai:text-embedding-3-small

# Create a handle for the embedding model of your choice
client = dataiku.api_client()
project = client.get_default_project()
emb_model = project.get_llm(EMBEDDING_MODEL_ID)

# Create and run an embedding query
txt = "The quick brown fox jumps over the lazy dog."
emb_query = emb_model.new_embeddings()
emb_query.add_text(txt)
emb_resp = emb_query.execute()

# Display the embedding output
print(emb_resp.get_embeddings())

# [[0.000237455,
#   -0.103262354,
#   ...
# ]]

```

(llm-mesh-tool-calls)=
## Tool calls

Tool calls (sometimes referred to as "function calling") allow you to augment a LLM with "tools",
functions that it can call and provide the arguments. Your client code can then perform those calls,
and provide the output back to the LLM so that it can generate the next response.

Tool calls are supported on the compatible completion models of some LLM connections:

* OpenAI
* Azure OpenAI
* Azure LLM
* Anthropic Claude
* Anthropic Claude models on AWS Bedrock connections
* MistralAI

### Define tools

You can define tools as settings in the completion query. Tool parameters are defined as JSON Schema objects.
See the [JSON Schema reference](https://json-schema.org/understanding-json-schema/) for documentation about the format.

Tools can also be automatically prepared and invoked from Python code, _e.g._ [using Langchain](llm-mesh-langchain-using-tool-calls).

```python
completion = llm.new_completion()
completion.settings["tools"] = [
  {
    "type": "function",
    "function": {
      "name": "multiply",
      "description": "Multiply integers",
      "parameters": {
        "type": "object",
        "properties": {
          "a": {
            "type": "integer",
            "description": "The first integer to multiply",
          },
          "b": {
            "type": "integer",
            "description": "The other integer to multiply",
          },
        },
        "required": ["a", "b"],
      }
    }
  }
]

completion.with_message("What is 3 * 6 ?")
resp = completion.execute()

print(resp.tool_calls)

# [{'type': 'function',
# 'function': {'name': 'multiply', 'arguments': '{"a":3,"b":6}'},
#   'id': 'call_gEB9fOdroydyxYuRs0Ge6Izg'}]
```

### Response streaming with tool calls

LLM responses which include tool calls can also leverage streaming. Depending on the LLM, response chunks may
include **either complete tool calls or partial tool calls**. When the LLM sends partial tool calls, the
streamed chunk contains an extra field `index` allowing to reconstruct the whole LLM response.

```python
for chunk in completion.execute_streamed():
    if isinstance(chunk, DSSLLMStreamedCompletionChunk):
        if "text" in chunk.data:
            print("Received text: %s" % chunk.data["text"])
        if "toolCalls" in chunk.data:
            print("Received tool call: %s" % chunk.data["toolCalls"])

    elif isinstance(chunk, DSSLLMStreamedCompletionFooter):
        print("Completion is complete: %s" % chunk.data)
```

### Provide tool outputs

Tool calls can then be parsed and executed. In order to provide the tool response in the chat messages, use the following methods:

```python
import json

# Function to handle the tool call
def multiply(llm_arguments):
    try:
        json_arguments = json.loads(llm_arguments)
        a = json_arguments["a"]
        b = json_arguments["b"]
        return str(a * b)
    except Exception as e:
        return f"Cannot call the 'multiply' tool: {str(e)}"

tool_calls = resp.tool_calls
call_id = tool_calls[0]["id"]
llm_arguments = tool_calls[0]["function"]["arguments"]
result = multiply(llm_arguments)

completion.with_tool_calls(tool_calls)
completion.with_tool_output(result, tool_call_id=call_id)

resp = completion.execute()

print(resp.text)

# 3 multiplied by 6 is 18.
```

### Control tool usage

Tool usage can be constrained in the completion settings:

```python
completion = llm.new_completion()

# Let the LLM decide whether to call a tool
completion.settings["toolChoice"] = {"type": "auto"}

# The LLM must call at least one tool
completion.settings["toolChoice"] = {"type": "required"}

# The LLM must not call any tool
completion.settings["toolChoice"] = {"type": "none"}

# The LLM must call the tool with name 'multiply'
completion.settings["toolChoice"] = {"type": "tool_name", "name": "multiply"}
```

## Knowledge Banks (KB)

### List and get KBs

To list the KB present in a project:

```{code-block} python
:name: llm-mesh-get-kbs
:caption: List and get KBs

import dataiku
client = dataiku.api_client()
project = client.get_default_project()
kb_list = project.list_knowledge_banks()
```

By default, {meth}`~dataikuapi.dss.project.DSSProject.list_knowledge_banks()` returns a list of {class}`~dataikuapi.dss.knowledgebank.DSSKnowledgeBankListItem`.
To get more details:

```python
for kb in kb_list:
    print(f"{kb.name} (id: {kb.id})")
```

To get a "core handle" on the KB (i.e. to retrieve a {class}`~dataiku.KnowledgeBank` object) :

```python
KB_ID = "" # Fill with your KB id
kb_public_api = project.get_knowledge_bank(KB_ID)
kb_core = kb_public_api.as_core_knowledge_bank()
```

(ce-llm-mesh-langchain-integration)=
## LangChain integration

Dataiku LLM model objects can be turned into langchain-compatible objects, making it easy to:
- stream responses
- run asynchronous queries
- batch queries
- chain several models and adapters
- integrate with the wider langchain ecosystem

### Transforming LLM handles to LangChain model

```python
# In this sample, llm is the result of calling project.get_llm() (see above)

# Turn a regular LLM handle into a langchain-compatible one
langchain_llm = llm.as_langchain_llm()

# Run a single completion query
langchain_llm.invoke("Write a haiku on GPT models")

# Run a batch of completion queries
langchain_llm.batch(["Write a haiku on GPT models", "Write a haiku on GPT models in German"])

# Run a completion query and stream the response
for chunk in langchain_llm.stream("Write a haiku on GPT models"):
    print(chunk, end="", flush=True)
```

See the [langchain documentation](https://python.langchain.com/docs/tutorials/llm_chain/) for more details.

You can also turn it into a langchain "chat model", a specific type of LLM geared towards conversation:

```python
# In this sample, llm is the result of calling project.get_llm() (see above)

# Turn a regular LLM handle into a langchain-compatible one
langchain_llm = llm.as_langchain_chat_model()

# Run a simple query
langchain_llm.invoke("Write a haiku on GPT models")

# Run a chat query
from langchain_core.messages import HumanMessage, SystemMessage

messages = [
    SystemMessage(content="You're a helpful assistant"),
    HumanMessage(content="What is the purpose of model regularization?"),
]
langchain_llm.invoke(messages)

# Streaming and chaining
from langchain.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template("Tell me a joke about {topic}")
chain = prompt | langchain_llm
for chunk in chain.stream({"topic": "parrot"}):
    print(chunk.content, end="", flush=True)
```

See the [langchain documentation](https://python.langchain.com/docs/tutorials/llm_chain/) for more details.

### Creating Langchain models directly

If running from inside DSS, you can also directly create the Langchain model:

```python
from dataiku.langchain.dku_llm import DKULLM, DKUChatModel

langchain_llm = DKUChatModel(llm_id="your llm id") # For example: openai:myopenai:gpt-4o
```

### Response streaming

The LangChain adapter `DKUChatModel` also support streaming of answer:

```python
from dataiku.langchain.dku_llm import DKULLM, DKUChatModel
from langchain_core.messages import HumanMessage, SystemMessage

langchain_llm = DKUChatModel(llm_id="your llm id") # For example: openai:myopenai:gpt-4o

messages = [
    SystemMessage(content="You're a helpful assistant"),
    HumanMessage(content="What is the purpose of model regularization?"),
]

for gen in langchain_llm.stream(messages):
    print(gen)
```


### Using knowledge banks as LangChain objects

Core handles allow users to leverage the Langchain library and, through it: 

* query the KB for semantic similarity search
* combine the KB with an LLM to form a *chain* and perform complex workflows
  such as *retrieval-augmented generation* (RAG).

In practice, core handles expose KBs as a Langchain-native 
[vector store](https://python.langchain.com/docs/how_to/#vector-stores)
through two different methods:

* {meth}`~dataiku.KnowledgeBank.as_langchain_retriever()` returns a generic {class}`~langchain.vectorstores.base.VectorStoreRetriever`
object

* {meth}`~dataiku.KnowledgeBank.as_langchain_vectorstore()` returns an object whose class corresponds to the KB type. 
For example, for a FAISS-based KB, you will get a
`langchain.vectorstores.faiss.FAISS` object.

```python
import dataiku
client = dataiku.api_client()
project = client.get_default_project()
kb_core = project.get_knowledge_bank(KB_ID).as_core_knowledge_bank()

# Return a langchain.vectorstores.base.VectorStoreRetriever
lc_generic_vs= kb_core.as_langchain_retriever()

# Return an object which type depends on the KB type
lc_vs = kb_core.as_langchain_vectorstore()

# [...] Move forward with similarity search or RAG 
```


#### Writing documents to a knowledge bank

Core handles allow users to leverage the LangChain library to write documents
to the underlying vector store.

In practice, core handles expose the method
{meth}`~dataiku.KnowledgeBank.get_writer()` which allows to get a writer on the
said knowledge bank, as a context manager. Such a writer can be used to build a
LangChain [vector store](https://python.langchain.com/docs/how_to/#vector-stores)
that inserts documents into the knowledge bank. The writer will synchronize the
vector store content to the knowledge bank automatically upon closing. Make
sure you have the `langchain_community` package in your code environment.

```python
import dataiku
from langchain_core.documents import Document

client = dataiku.api_client()
project = client.get_default_project()
dss_kb = project.get_knowledge_bank(KB_ID)
kb_core = dss_kb.as_core_knowledge_bank()

document = Document(page_content="I can write to a knowledge bank!")

with kb_core.get_writer() as writer:
    print(f"Start from folder {writer.folder_path}")
    # writer.clear()  # uncomment to clear the knowledge bank

    langchain_vs = writer.as_langchain_vectorstore()
    langchain_vs.add_documents([document])
```

#### Saving knowledge bank metadata

When inserting documents into a vector store, it is possible to specify
metadata that can be retrieved later on. To leverage this metadata during
retrieval in Dataiku, it is necessary to set the metadata schema in the
knowledge bank settings.

```python
kb_settings = dss_kb.get_settings()
kb_settings.set_metadata_schema({
    "source": "string",
    "start_index": "int"
})

kb_settings.save()

document = Document(
    page_content="I can set metadata",
    metadata={
      "source": "developer-guide",
      "start_index": 1
    }
)

with kb_core.get_writer() as writer:
    langchain_vs = writer.as_langchain_vectorstore()
    langchain_vs.add_documents([document])
```

#### Setting retrieval content in the document metadata

The write API allows to format retrieval content in the document metadata, so
that the knowledge bank can be used for multimodal retrieval.

The image folder of the knowledge bank can be configured in the knowledge bank
settings:

```python
images_folder = dataiku.Folder(IMAGE_FOLDER_ID)
images_folder_full_id = f"{images_folder.project_key}.{images_folder.get_id()}"

kb_settings = dss_kb.get_settings()
kb_settings.set_images_folder(images_folder_full_id)
kb_settings.save()
```

The retrieval content can be formatted using the knowledge bank writer:

```python
from dataikuapi.dss.document_extractor import ManagedFolderDocumentRef

# assumption: the document has only one page
original_document_ref = ManagedFolderDocumentRef("/path/to/file.pdf", ORIGINAL_DOCUMENT_FOLDER_ID)

with kb_core.get_writer() as writer:
    document = Document(page_content="Summarized text from VLM extraction")

    document = (
        writer.get_metadata_formatter()
            .with_original_document_ref(original_document_ref)
            .with_original_document_page_range(1, 1)  # one page
            .with_retrieval_content(image_paths=[
                "/path/to/screenshot/in/image/folder.jpg"
            ])
            .format_metadata(document)
    )

    # writer.clear()  # uncomment to clear the knowledge bank
    langchain_vs = writer.as_langchain_vectorstore()
    langchain_vs.add_documents([document])
```

### Hybrid Search

Combines both similarity search (default behaviour) and keyword search to retrieve more relevant documents. Only supported by Azure AI Search and Elasticsearch; and not compatible with the diversity option.

Additionally, both vector store offer advanced reranking capabilities, to enhance the mix of documents retrieved. Each has its own specific configuration.

#### Azure AI Search

```python
import dataiku
client = dataiku.api_client()
project = client.get_default_project()
kb_core = project.get_knowledge_bank(KB_ID).as_core_knowledge_bank()

# 1 using as_langchain_retriever
azure_classic_retriever = kb_core.as_langchain_retriever(search_type="similarity")
azure_hybrid_retriever = kb_core.as_langchain_retriever(search_type="hybrid")
azure_hybrid_advanced_retriever = kb_core.as_langchain_retriever(search_type="semantic_hybrid")

# 2 using as_langchain_vectorstore to get retriever
azure_classic_retriever = kb_core.as_langchain_vectorstore().as_retriever(
  search_type="similarity")
azure_hybrid_retriever = kb_core.as_langchain_vectorstore().as_retriever(
  search_type="hybrid")
azure_hybrid_advanced_retriever = kb_core.as_langchain_vectorstore().as_retriever(
  search_type="semantic_hybrid")

# 3 using as_langchain_vectorstore to perform query
query = "A text to match some doccuments"
azure_classic_result = kb_core.as_langchain_vectorstore().similarity_search(query)
azure_hybrid_result = kb_core.as_langchain_vectorstore().hybrid_search(query)
azure_hybrid_advanced_result = kb_core.as_langchain_vectorstore().semantic_hybrid_search(query)
```

#### ElasticSearch

For elastic search, since we need the info at db instantiation time, thats why we need to use `vectorstore_kwargs`.

Only `similarity` search type is allowed when using a hybrid strategy.

```python
import dataiku
from elasticsearch.helpers.vectorstore import DenseVectorStrategy

client = dataiku.api_client()
project = client.get_default_project()
kb_core = project.get_knowledge_bank(KB_ID).as_core_knowledge_bank()

hybrid_strategy = DenseVectorStrategy(hybrid=True)
hybrid_advanced_strategy = DenseVectorStrategy(hybrid=True, rrf=True)

# 1 using as_langchain_retriever
elastic_classic = kb_core.as_langchain_retriever()
elastic_hybrid = kb_core.as_langchain_retriever(
  vectorstore_kwargs={"strategy": hybrid_strategy})
elastic_hybrid_advanced = kb_core.as_langchain_retriever(
  vectorstore_kwargs={"strategy": hybrid_advanced_strategy})

# 2 using as_langchain_vectorstore
elastic_classic = kb_core.as_langchain_vectorstore().as_retriever()
elastic_hybrid = kb_core.as_langchain_vectorstore(
  strategy=hybrid_strategy).as_retriever(search_type="similarity")
elastic_hybrid_advanced = kb_core.as_langchain_vectorstore(
  strategy=hybrid_advanced_strategy).as_retriever(search_type="similarity")
```

(llm-mesh-langchain-using-tool-calls)=
### Using tool calls

The LangChain chat model adapter supports tool calling, assuming that the underlying LLM supports it too.

```python
import dataiku

from langchain_core.tools import tool
from langchain_core.messages import HumanMessage

# Define tools

@tool
def add(a: int, b: int) -> int:
    """Adds a and b."""
    return a + b

@tool
def multiply(a: int, b: int) -> int:
    """Multiplies a and b."""
    return a * b

tools_by_name = {"add": add, "multiply": multiply}
tools = [add, multiply]
tool_choice = {"type": "auto"}

# Get the LangChain chat model, bind it to the tools
client = dataiku.api_client()
project = client.get_default_project()
llm_id = "<your llm id>"  # For example: "openai:myopenai:gpt-4o"
llm = project.get_llm(llm_id).as_langchain_chat_model()
llm_with_tools = llm.bind_tools(tools, tool_choice=tool_choice)

# Ask your question
messages = [HumanMessage("What is 3 * 12? and 6 + 4?")]
ai_msg = llm_with_tools.invoke(messages)
messages.append(ai_msg)

# Retrieve tool calls, run them and put the results in the chat messages
for tool_call in ai_msg.tool_calls:
    tool_name = tool_call["name"]
    selected_tool = tools_by_name[tool_name]
    tool_msg = selected_tool.invoke(tool_call)
    messages.append(tool_msg)

# Get the final response
ai_msg = llm.invoke(messages)
ai_msg.content
# '3 * 12 is 36, and 6 + 4 is 10.'
```



(concept-and-examples-llm-mesh-fine-tuning)=

## Fine-tuning

### Create a Fine-tuned LLM Saved Model version

:::{note}
{doc}`Visual model fine-tuning<refdoc:generative-ai/fine-tuning>` is also available to customers with the _Advanced LLM Mesh_ add-on.
:::

With a Python recipe or notebook, it is possible to fine-tune an LLM from the
HuggingFace Hub and save it as a Fine-tuned LLM Saved Model version.
This is done with the {meth}`~dataiku.Model.create_finetuned_llm_version()` method, which takes an LLM Mesh connection name as input.
Settings on this connection like usage permission, guardrails, code environment, or
container configuration, will apply at inference time.

The above method must be called on an existing Saved Model. Create one
either programmatically (if you are in a notebook and don't have one yet) with
{meth}`~dataikuapi.dss.project.DSSProject.create_finetuned_llm_saved_model`
or visually from the Agents & GenAI models list via **+New GenAI Model > Create Fine-tuned LLM**
(if you want to do this in a python recipe, its output Saved Model must exist to create the recipe).

Here we fine-tune using several open-source frameworks from HuggingFace:
[transformers](https://huggingface.co/docs/transformers/en/index), [trl](https://huggingface.co/docs/trl/index) & [peft](https://huggingface.co/docs/peft/index). 

```{attention}
Note that fine-tuning a local LLM requires significant computational resources (GPU). 
The code samples below show state-of-the-art techniques to optimize memory usage and processing time,
but this depends on your setup and might not always work.
Also, beware that the size of your training (and optionally validation) dataset(s) greatly impacts the memory use and storage during fine-tuning.
```

`````{tabs}
````{group-tab} Microsoft Phi3 Mini 4k

One can fine-tune a smaller LLM with a small GPU available.
[Phi3 Mini](https://huggingface.co/microsoft/Phi-3-mini-4k-instruct) is a good example, with "only" 3.8B parameters. 

There are many techniques available to reduce memory usage and speed up computation.
One of them is called [Low-Rank Adaptation](https://arxiv.org/abs/2106.09685).
It consists in freezing the weights from the base model and adding new,
trainable matrices to the Transformer architecture. 
It drastically reduces the number of trainable parameters and, hence, the GPU memory requirement. 

```{literalinclude} ./examples/llm/fine-tuning/phi3mini4k_ft_lora.py
```
````

````{group-tab} Mistral 7B V0.2

It is also possible to fine-tune larger models, for instance, Mistral 7B.
In that case, quantization can help further reducing the memory footprint.
A paper called [QLoRA](https://arxiv.org/abs/2305.14314) shows how the LoRA technique
can efficiently fine-tune quantized LLMs while limiting the performance loss.

```{literalinclude} ./examples/llm/fine-tuning/mistral7BV02_ft_lora_quantized.py
```
````

% TODO test & add multi-GPU example with Accelerate
% ````{group-tab} Llama3.1 8B on multiple GPUs
% 
% If the setup allows, one could try fine-tuning larger models on multiple GPUs.
% HuggingFace provides the great [Accelerate](https://huggingface.co/docs/accelerate/index)
% package to help with set up the training across a distributed configuration. 
% 
% Here is an example with Llama3.1 8B, fine-tuned on 2 GPUs. 
% ````
````{group-tab} DPO
Direct Preference Optimization (DPO) is a stable, efficient, and lightweight way to fine-tune LLMs using preference data. 
It was introduced in 2023 as a simpler alternative to complex reinforcement learning algorithms. 

Instead of training a separate reward model,
DPO uses a simple cross-entropy loss function to directly teach the LLM to assign high probability to preferred responses. 

In this example, we leverage DPO with both quantization and low-rank adapters (LoRA) from the PEFT framework. 

For more on DPO, see the [original paper](https://arxiv.org/abs/2305.18290)
and [TRL implementation](https://huggingface.co/docs/trl/main/en/dpo_trainer).
Other RLHF alternatives are also supported, like IPO or [KTO](https://huggingface.co/docs/trl/main/en/kto_trainer).
For traditional reinforcement learning algorithms,
see [PPO](https://huggingface.co/docs/trl/main/en/ppo_trainer). 

```{note}
Requirements to run this notebook:
- Create an updated `INTERNAL_huggingface_local_vX` code environment with:

      trl==0.13.0
      datasets==2.21.0

- Use this code env for training & in the selected **HuggingFace Local** connection.
```
```{literalinclude} ./examples/llm/fine-tuning/dpo.py
````
`````

In these examples, we used popular techniques to optimize memory usage and processing time, like LoRA, quantization or gradient checkpointing. Note that the research and open source community is constantly coming up with new ways to make fine-tuning more accessible, while trying to avoid too much performance loss. For more information on other techniques you could try, see for instance the [`Transformers`](https://huggingface.co/docs/transformers/v4.43.3/performance) or [`PEFT`](https://huggingface.co/docs/peft/conceptual_guides/adapter) documentations. 

## OpenAI-compatible API
The OpenAI-compatible API provides an easy way to query the LLM Mesh as it is built on top of the LLM Mesh API and implements the most used parts of OpenAI's API for text completion.

The OpenAI-compatible API allows you to send chat completion queries to all LLMs supported by the LLM Mesh, using a standard OpenAI format. This includes, for models that support it:

* Streamed chat completion responses
* Multimodal inputs (image and text)
* Tool calls
* JSON output mode

```{attention}
Some arguments from the OpenAI's API reference are not supported. 

Chat completion request:

* n
* response_format
* seed
* service_tier
* parallel_tool_calls
* user
* function_call (deprecated)
* functions (deprecated)

Chat completion response:

* choices.message.refusal
* choices.logprobs.refusal
* created
* service_tier
* system_fingerprint
* usage.completion_tokens_details

```

### Your first OpenAI completion query

`````{tabs}
````{group-tab} Simple chat completion

```python
from openai import OpenAI

# Specify the DSS OpenAI-compatible public API URL, e.g. http://my.dss/public/api/projects/PROJECT_KEY/llms/openai/v1/
BASE_URL = ""
# Fill with your DSS API Key
API_KEY = ""

# Fill with your LLM id. For example, if you have a HuggingFace connection called "myhf", LLM_ID can be "huggingfacelocal:myhf:meta-llama/Meta-Llama-3.1-8B-Instruct:TEXT_GENERATION_LLAMA_2:promptDriven=true"
# To get the list of LLM ids, you can use openai_client.models.list() or project.list_llms() through the dataiku client 
LLM_ID = ""

# Create an OpenAI client
openai_client = OpenAI(
  base_url=BASE_URL,
  api_key=API_KEY
)

resp = openai_client.chat.completions.create(
  model=LLM_ID,
  messages=[{"role": "user", "content": "Write a haiku on GPT models" }],
)

if resp and resp.choices:
  print(resp.choices[0].message.content)

# GPT, a marvel,
# Deep learning's symphony plays,
# Thoughts dance, words unveil.
```
````

````{group-tab} Streaming chat completion

```python
from openai import OpenAI

# Specify the DSS OpenAI-compatible public API URL, e.g. http://my.dss/public/api/projects/PROJECT_KEY/llms/openai/v1/
BASE_URL = ""
# Fill with your DSS API Key
API_KEY = ""

# Fill with your LLM id. For example, if you have a HuggingFace connection called "myhf", LLM_ID can be "huggingfacelocal:myhf:meta-llama/Meta-Llama-3.1-8B-Instruct:TEXT_GENERATION_LLAMA_2:promptDriven=true"
# To get the list of LLM ids, you can use openai_client.models.list() or project.list_llms() through the dataiku client 
LLM_ID = ""

# Create an OpenAI client
openai_client = OpenAI(
  base_url=BASE_URL,
  api_key=API_KEY
)

resp = openai_client.chat.completions.create(
  model=LLM_ID,
  messages=[{"role": "user", "content": "Write a haiku on GPT models" }],
  stream=True
)

for chunk in resp:
    if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content)

# Words
#  weave
#  through
#  the
#  code
# ,
# 
#
# Silent
#  thoughts
#  brought
#  into
#  light
# ,
  

# M
# inds
#  connect
#  in
#  spark
# .
```
````
`````

## Image generation using the LLM Mesh

### Your first image-generation query

This sample shows how to send an image generation query with the LLM Mesh to ask the image generation model to generate an image of a blue bird.

```python
import dataiku

client = dataiku.api_client()
project = client.get_default_project()

# To list the image generation model ids, you can use project.list_llms(purpose="IMAGE_GENERATION")
IMAGE_GENERATION_MODELS = project.list_llms(purpose="IMAGE_GENERATION")

IMAGE_GENERATION_MODEL_ID = "" # Fill with your image generation model id, for example: openai:my_openai_connection:dall-e-3

# Create a handle for the image generation model of your choice
img_gen_model = project.get_llm(IMAGE_GENERATION_MODEL_ID)

prompt_text = "Vibrant blue bird in a serene scene on a blooming cherry blossom branch. Tranquil morning sky background with soft pastel colors of dawn, gently blending pinks, purples, and soft oranges. Distant view of a calm lake reflecting the colors of the sky and surrounded by lush greenery."

img_gen_query = img_gen_model.new_images_generation()
img_gen_query.with_prompt(prompt_text)
img_gen_resp = img_gen_query.execute()
image_data = img_gen_resp.first_image()

# You can display the image in your notebook
from IPython.display import Image, display
if img_gen_resp.success:
    display(Image(image_data))

# Or you can save the image to a managed folder
FOLDER_ID = ""  # Enter your managed folder id here
my_images_folder = dataiku.Folder(FOLDER_ID)
with my_images_folder.get_writer("blue_bird.png") as writer:
    writer.write(image_data)
```

You can parameterize the query to impact the resulting image or generate more images.

The LLM Mesh maps each parameter to the corresponding parameter for the underlying model provider. Support varies across models/providers, and in particular not all models can generate more than one image.

If you want to generate multiple images with different prompts, you must query the LLM Mesh multiple times.

```python
import dataiku

IMAGE_GENERATION_MODEL_ID = "" # Fill with your image generation model id

# Create a handle for the image generation model of your choice
client = dataiku.api_client()
project = client.get_default_project()
img_gen_model = project.get_llm(IMAGE_GENERATION_MODEL_ID)
generation = img_gen_model.new_images_generation()
generation.height = 1024
generation.width = 1024
generation.seed = 3
# If the underlying model supports weighted prompts they will be passed with
# their specified weight, otherwise they will just be merged and sent as a single prompt.
generation.with_prompt("meat pizza", weight=0.8).with_prompt("rustic wooden table", weight=0.6)

# Not all models or providers support more than one
generation.images_to_generate = 1

# Regardless of what parameter the underlying provider expects for the image dimensions,
# when using the LLM Mesh API you can specify either the height and width or the aspect_ratio.
# The LLM Mesh will do the translation between its API and the underlying provider.
# Not all models support the same dimensions.
generation.aspect_ratio = 21 / 9

# The following parameters are not relevant for all models
generation.with_negative_prompt("tomatoes, basil, green leaf", weight=1)
generation.fidelity = 0.5 # from 0.1 to 1, how strongly to adhere to prompt
# valid values depend on the targeted model
generation.quality = "hd"
generation.style = "anime"

resp = generation.execute()
```

### Image-to-image query

Some models can generate an image from another image, see {doc}`this documentation <refdoc:generative-ai/multimodal>`.
- Mask-free variation generates another image guided by a prompt
- Some models can generate unprompted variations
- Inpainting uses a mask (either black pixels in a second input image, or transparent pixels on the original image) to fill the corresponding pixels of the input image

`````{tabs}
````{group-tab} Prompted variation

In this example, we ask the model for an image variation by passing an image and a prompt using the `MASK_FREE` mode.

```python
import dataiku

IMAGE_GENERATION_MODEL_ID = "" # Fill with your image generation model id

img_gen_model = dataiku.api_client().get_default_project().get_llm(IMAGE_GENERATION_MODEL_ID)

# Your image to use as an input.
# Here we're retrieving it from a managed folder but it could also be an image from a previous generation
my_images_folder = dataiku.Folder("my_folder_id")
with my_images_folder.get_download_stream("cat_on_the_beach.png") as img_file:
    input_img_data = img_file.read()

# Create the generation query
generation = img_gen_model.new_images_generation()
generation.with_original_image(input_img_data, mode="MASK_FREE", weight=0.3)
generation.with_prompt("dog on the beach")
resp = generation.execute()
```

Image-to-image generation with a prompt can also be used with the `CONTROLNET_STRUCTURE` and `CONTROLNET_SKETCH` modes.

````

````{group-tab} Unprompted variation

In this example, we ask the model for an image variation by sending an image without a prompt.

```python
import dataiku

IMAGE_GENERATION_MODEL_ID = "" # Fill with your image generation model id

img_gen_model = dataiku.api_client().get_default_project().get_llm(IMAGE_GENERATION_MODEL_ID)

# Your image to use as an input.
# Here we're retrieving it from a managed folder but it could also be an image from a previous generation
my_images_folder = dataiku.Folder("my_folder_id")
with my_images_folder.get_download_stream("cat_on_the_beach.png") as img_file:
    input_img_data = img_file.read()

# Create the generation query
generation = img_gen_model.new_images_generation()
generation.with_original_image(input_img_data, mode="VARY", weight=0.3)
resp = generation.execute()
```
````

````{group-tab} Inpainting: mask image

When using the `MASK_IMAGE_BLACK` mask mode, you need to specify a mask with black pixels to fill.

```python
import dataiku

IMAGE_GENERATION_MODEL_ID = "" # Fill with your image generation model id

img_gen_model = dataiku.api_client().get_default_project().get_llm(IMAGE_GENERATION_MODEL_ID)

# Your image to use as an input.
# Here we're retrieving it from a managed folder but it could also be an image from a previous generation
my_images_folder = dataiku.Folder("my_folder_id")
with my_images_folder.get_download_stream("cat_on_the_beach.png") as img_file:
    input_img_data = img_file.read()
with my_images_folder.get_download_stream("cat_black_mask.png") as img_file:
    black_mask_image_data = img_file.read()


# Create the generation query
generation = img_gen_model.new_images_generation()
generation.with_original_image(input_img_data, mode="INPAINTING", weight=0.1)
generation.with_mask("MASK_IMAGE_BLACK", image=black_mask_image_data)
generation.with_prompt("dog")
resp = generation.execute()
```
````

````{group-tab} Inpainting: mask pixels

When using the `ORIGINAL_IMAGE_ALPHA` you do not need to specify a mask image. The model will fill the transparent pixels from the original image.

```python
import dataiku

IMAGE_GENERATION_MODEL_ID = "" # Fill with your image generation model id

img_gen_model = dataiku.api_client().get_default_project().get_llm(IMAGE_GENERATION_MODEL_ID)

# Your image to use as an input.
my_images_folder = dataiku.Folder("my_folder_id")
with my_images_folder.get_download_stream("cat_transparent_background.png") as img_file:
    input_img_data = img_file.read()

# Create the generation query
generation = img_gen_model.new_images_generation()
generation.with_original_image(input_img_data, mode="INPAINTING", weight=0.1)
generation.with_mask("ORIGINAL_IMAGE_ALPHA")
generation.with_prompt("Beach scene at sunset, with golden sands, gentle waves at the shore.")
resp = generation.execute()
```
````
`````

## Reference documentation

### Classes

```{eval-rst}
.. autosummary:: 
    dataiku.KnowledgeBank 
    dataiku.core.vector_stores.data.metadata.DocumentMetadataFormatter
    dataiku.core.vector_stores.data.writer.VectorStoreWriter
    dataikuapi.dss.document_extractor.ManagedFolderDocumentRef  
    dataikuapi.dss.llm.DSSLLM
    dataikuapi.dss.llm.DSSLLMListItem
    dataikuapi.dss.llm.DSSLLMCompletionQuery
    dataikuapi.dss.llm.DSSLLMCompletionsQuery
    dataikuapi.dss.llm.DSSLLMCompletionsQuerySingleQuery
    dataikuapi.dss.llm.DSSLLMCompletionQueryMultipartMessage
    dataikuapi.dss.llm.DSSLLMCompletionResponse
    dataikuapi.dss.llm.DSSLLMEmbeddingsQuery
    dataikuapi.dss.llm.DSSLLMEmbeddingsResponse
    dataikuapi.dss.knowledgebank.DSSKnowledgeBank
    dataikuapi.dss.knowledgebank.DSSKnowledgeBankListItem
    dataikuapi.dss.knowledgebank.DSSKnowledgeBankSettings
    dataikuapi.dss.langchain.DKUChatModel
    dataikuapi.dss.langchain.DKULLM
    dataikuapi.dss.langchain.DKUEmbeddings
    dataikuapi.dss.project.DSSProject
```

### Functions
```{eval-rst}
.. autosummary::
    ~dataikuapi.dss.llm.DSSLLMCompletionQueryMultipartMessage.add
    ~dataikuapi.dss.llm.DSSLLMEmbeddingsQuery.add_text
    ~dataikuapi.dss.knowledgebank.DSSKnowledgeBank.as_core_knowledge_bank
    ~dataikuapi.dss.llm.DSSLLMImageGenerationQuery.aspect_ratio
    ~dataikuapi.dss.langchain.DKUChatModel.bind_tools
    ~dataikuapi.dss.llm.DSSLLM.as_langchain_chat_model
    ~dataikuapi.dss.llm.DSSLLM.as_langchain_llm
    ~dataikuapi.dss.llm.DSSLLMListItem.description
    ~dataikuapi.dss.llm.DSSLLMCompletionQuery.execute
    ~dataikuapi.dss.llm.DSSLLMEmbeddingsQuery.execute
    dataikuapi.dss.llm.DSSLLMImageGenerationQuery.execute
    ~dataikuapi.dss.llm.DSSLLMCompletionQuery.execute_streamed
    ~dataikuapi.dss.llm.DSSLLMImageGenerationQuery.fidelity
    ~dataikuapi.dss.llm.DSSLLMImageGenerationResponse.first_image
    ~dataiku.core.vector_stores.data.metadata.DocumentMetadataFormatter.format_metadata
    ~dataikuapi.dss.llm.DSSLLMEmbeddingsResponse.get_embeddings
    ~dataikuapi.dss.project.DSSProject.get_knowledge_bank
    ~dataikuapi.dss.project.DSSProject.get_llm
    ~dataiku.core.vector_stores.data.writer.VectorStoreWriter.get_metadata_formatter
    ~dataikuapi.dss.knowledgebank.DSSKnowledgeBank.get_settings
    ~dataiku.KnowledgeBank.get_writer
    ~dataikuapi.dss.llm.DSSLLMListItem.id
    ~dataikuapi.dss.llm.DSSLLMImageGenerationQuery.images_to_generate
    ~dataikuapi.dss.project.DSSProject.list_knowledge_banks
    ~dataikuapi.dss.project.DSSProject.list_llms
    ~dataikuapi.dss.llm.DSSLLM.new_completion
    ~dataikuapi.dss.llm.DSSLLM.new_embeddings
    ~dataikuapi.dss.llm.DSSLLM.new_images_generation
    ~dataikuapi.dss.llm.DSSLLMCompletionQuery.new_multipart_message
    ~dataikuapi.dss.llm.DSSLLMImageGenerationQuery.quality
    ~dataikuapi.dss.knowledgebank.DSSKnowledgeBankSettings.save
    ~dataikuapi.dss.knowledgebank.DSSKnowledgeBankSettings.set_images_folder
    ~dataikuapi.dss.knowledgebank.DSSKnowledgeBankSettings.set_metadata_schema
    ~dataikuapi.dss.llm.DSSLLMCompletionQuery.settings
    ~dataikuapi.dss.llm.DSSLLMImageGenerationQuery.style
    ~dataikuapi.dss.llm.DSSLLMCompletionResponse.success
    ~dataikuapi.dss.llm.DSSLLMCompletionResponse.text
    ~dataikuapi.dss.llm.DSSLLMCompletionResponse.tool_calls
    ~dataikuapi.dss.llm.DSSLLMCompletionQueryMultipartMessage.with_inline_image
    ~dataikuapi.dss.llm.DSSLLMCompletionQuery.with_message
    ~dataiku.core.vector_stores.data.metadata.DocumentMetadataFormatter.with_original_document_page_range
    ~dataiku.core.vector_stores.data.metadata.DocumentMetadataFormatter.with_original_document_ref
    ~dataikuapi.dss.llm.DSSLLMImageGenerationQuery.with_original_image
    ~dataikuapi.dss.llm.DSSLLMImageGenerationQuery.with_mask
    ~dataikuapi.dss.llm.DSSLLMImageGenerationQuery.with_negative_prompt
    ~dataikuapi.dss.llm.DSSLLMImageGenerationQuery.with_prompt
    ~dataiku.core.vector_stores.data.metadata.DocumentMetadataFormatter.with_retrieval_content
    ~dataikuapi.dss.llm.DSSLLMCompletionQueryMultipartMessage.with_text
    ~dataikuapi.dss.llm.DSSLLMCompletionQuery.with_tool_calls
    ~dataikuapi.dss.llm.DSSLLMCompletionQuery.with_tool_output
```