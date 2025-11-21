# Zero-shot text classification with the LLM Mesh

Generative AI offers powerful tools
that enable data scientists to integrate cutting-edge natural language processing (NLP) capabilities into their applications.
In particular, it exposes its latest large language models (LLM) for easy queries.
Combining these tools with the coder-oriented features of Dataiku further empowers the platform users to configure
and run NLP tasks in a project.

With Dataiku's LLM mesh capabilities,
you can leverage the power of various LLM types using a unified programmatic interface provided by the public API.
More specifically, the Python API client allows you to easily manipulate query and response objects you send to/get from your LLM.

In this tutorial, you will cover the basics of using the LLM Mesh within Dataiku
and apply it using an LLM for a text classification problem on movie reviews.  

## Prerequisites

* Dataiku >= 12.3 (or 13.1 if you want to use Langchain-compatible functions)
* Access to an existing project with the following permissions:
    * "Read project content"
    * "Write project content"
* A valid LLM connection 

## Getting the LLM 

The first step is to get the LLM ID you want. With the LLM Mesh, you can use any generative AI model provider;
Dataiku offers an abstraction over many LLM services.
You can easily find the desired LLM ID by running {ref}`Code 1<tutorials-genai-nlp-llm-zero-shot-getting-llm-id>`.

```{code-block} python
:name: tutorials-genai-nlp-llm-zero-shot-getting-llm-id
:caption: "Code 1: List existing LLM and their associated ID."

import dataiku

client = dataiku.api_client()
project = client.get_default_project()
llm_list = project.list_llms()
for llm in llm_list:
    print(f"- {llm.description} (id: {llm.id})")
```

Once you have identified which LLM you want to use, note the associated ID (`LLM_ID`)

### Initial tests

You can ask your LLM a simple question to test whether everything is OK.
This is done in {ref}`Code 2<tutorials-genai-nlp-llm-zero-shot-simple-question>`.

(tutorials-genai-nlp-llm-zero-shot-simple-question)=

`````{tabs}

````{group-tab} LLM Mesh

```{code-block} python
:caption: "Code 2: Asking a question to an LLM"

LLM_ID = "" #Fill with a valid LLM_ID
llm = project.get_llm(LLM_ID)
completion = llm.new_completion()
resp = completion.with_message("When was the movie Citizen Kane released?").execute()
if resp.success:
    print(resp.text)
else:
    print("Something went wrong. Check you have the permission to use the LLM")
    
# > 'Citizen Kane was released on September 5, 1941.'
```

````

````{group-tab} Langchain-compatible LLM

```{code-block} python
:caption: "Code 2: Asking a question to a Langchain-compatible LLM"

LLM_ID = "" #Fill with a valid LLM_ID
llm = project.get_llm(LLM_ID)
lcllm = llm.as_langchain_llm()
lcllmResp = lcllm.invoke("When was the movie Citizen Kane released?")
print(lcllmResp)

# > 'Citizen Kane was released on September 5, 1941.'
```
````

````{group-tab} Langchain-compatible chat LLM
```{code-block} python
:caption: "Code 2: Asking a question to a Langchain-compatible chat LLM"

LLM_ID = "" #Fill with a valid LLM_ID
llm = project.get_llm(LLM_ID)
chat = llm.as_langchain_chat_model()
chatResp = chat.invoke("When was the movie Citizen Kane released?")
print(chatResp.content)

# > Citizen Kane was released on September 5, 1941.

```
````

`````

You can tweak the prompt to be more flexible on the model input.
In practice, it translates into providing additional _context_ to the model about what it should know and how it should respond. 
{ref}`Code 3<tutorials-genai-nlp-llm-zero-shot-context-question>` shows how to add extra context to an LLM.

(tutorials-genai-nlp-llm-zero-shot-context-question)=

`````{tabs}
````{group-tab} LLM Mesh
```{code-block} python
:caption: "Code 3: Tweaking the prompt"

completion = llm.new_completion()

question = "When was the movie Citizen Kane released?"
system_msg = """You are an expert in the history of American cinema.
You always answer questions with a lot of passion and enthusiasm.
"""

resp = completion.with_message(role="system", message=system_msg).with_message(role="user", message=question).execute()
if resp.success:
    print(resp.text)
else:
    print("Something went wrong. Check you have the permission to use the LLM")
    
# > 'Ah, Citizen Kane! What a masterpiece of American cinema! It was released on
# September 5, 1941, and it completely revolutionized the film industry with its
# innovative storytelling techniques and groundbreaking cinematography. Directed
# by the legendary Orson Welles, Citizen Kane is a timeless classic that continues
# to captivate audiences with its rich narrative and complex characters. It truly
# is a must-see for anyone interested in the history of cinema!'
```
````
````{group-tab} Langchain-compatible LLM
```{code-block} python
:caption: "Code 3: Tweaking the prompt"

from langchain_core.messages import HumanMessage, SystemMessage

question = "When was the movie Citizen Kane released?"
system_msg = """You are an expert in the history of American cinema.
You always answer questions with a lot of passion and enthusiasm.
"""

messages = [
    SystemMessage(content=system_msg),
    HumanMessage(content=question)
]

lcllmResp = lcllm.invoke(messages)
print(lcllmResp)

# > "Oh, Citizen Kane! What a masterpiece of American cinema. It was released on
# September 5, 1941. Directed by Orson Welles, it is often considered one of the
# greatest films ever made. The innovative storytelling techniques and 
# groundbreaking cinematography truly set it apart from other films of its time.
# It's a must-watch for any film enthusiast!"
```
````
````{group-tab} Langchain-compatible chat LLM
```{code-block} python
:caption: "Code 3: Tweaking the prompt"

from langchain_core.messages import HumanMessage, SystemMessage

question = "When was the movie Citizen Kane released?"
system_msg = """You are an expert in the history of American cinema.
You always answer questions with a lot of passion and enthusiasm.
"""

messages = [
    SystemMessage(content=system_msg),
    HumanMessage(content=question)
]

chatResp = chat.invoke(messages)
print(chatResp.content)

# > Oh, Citizen Kane! What a masterpiece of American cinema! It was released on
# September 5, 1941. Directed by the legendary Orson Welles, this film is often
# considered one of the greatest films ever made. The innovative storytelling
# techniques, groundbreaking cinematography, and powerful performances make it a
# timeless classic that continues to captivate audiences to this day. If you haven't
# seen it yet, I highly recommend watching it to experience the magic of this
# cinematic gem!
```
````
`````
While being fun, this example also unveils the potential of such models:
_with the proper instructions and context, they can perform a wide variety of tasks based on natural language!_
In the next section, you will use this versatility to customize your prompt and turn the LLM into a text classifier.

## Classifying movie reviews

The following example will rely on an extract from the
[Large Movie Review Dataset](https://ai.stanford.edu/~amaas/data/sentiment/).
Download the file [here](https://cdn.downloads.dataiku.com/public/website-additional-assets/data/IMDB_train.csv.gz) and use 
it to create a dataset in your project called `reviews`. In this dataset, there are two columns of interest:

- `text` contains the reviews to be analyzed
- `polarity` reflects the review sentiment: 0 for negative, 1 for positive

To test your function, you will run it on a small sample of the `reviews` dataset.
For that, create a Python recipe that outputs a single dataset called `reviews_sample_llm_scored` with 
{ref}`Code 4<tutorials-genai-nlp-llm-zero-shot-getting-testing>`.
Note that the system message was thoroughly customized to align the model with the task,
telling it exactly what to do and how to format the output. 
Crafting and iteratively adjusting the model's input to guide it toward the desired response is known as _prompt engineering_.

(tutorials-genai-nlp-llm-zero-shot-getting-testing)=
`````{tabs}
````{group-tab} LLM Mesh
```{literalinclude} assets/recipe.py
:language: python
:caption: "Code 4: Testing the classification"
```
````
````{group-tab} Langchain-compatible LLM
```{literalinclude} assets/recipe_lcllm.py
:language: python
:caption: "Code 4: Testing the classification"
```
````
````{group-tab} Langchain-compatible chat LLM
```{literalinclude} assets/recipe_chat.py
:language: python
:caption: "Code 4: Testing the classification"
```
````
`````



This recipe will read the input dataset line-by-line and iteratively send the review text to the LLM to retrieve:
- the inferred sentiment (0 or 1)
- a short explanation of why the review is good or bad

Once the output dataset is built, you can compare the values of the `polarity` and `llm_sentiment`,
which should match closely: your classifier is doing well!
The `llm_explanation` should also give you a quick insight into how the model understood the review.

This technique is called *zero-shot classification* since it relies on the model's ability to understand relationships 
between words and concepts without being specifically trained on labeled data. 

```{warning}
While LLMs show promising capabilities to understand and generate human-like text,
they can also sometimes create outputs with pieces of information or details that aren't accurate or factual.
These mistakes are known as _hallucinations_ and can arise due to the following:
- limitations and biases in the model's training data
- the inherent nature of the model to reproduce statistical patterns rather than proper language understanding or reasoning

To mitigate their impact, you should always review any model output that would be part of a critical decision-making process.
```

## Wrapping up 

Congratulations! You have completed this tutorial and gained valuable insights into basic coding features in Dataiku and the LLM Mesh.
By understanding the basic concepts of language-based generative AI and the relevant tools in Dataiku to leverage them,
you are now ready to tackle more complex use cases.

If you want to further experiment beyond this tutorial you can, for example:
- Change the value of `SSIZE` in the recipe to increase the sample size. 
  This should result in a decent-sized scored dataset on which you can adequately evaluate the predictive performance
  of your classifier with metrics such as accuracy, precision, or F1 Score.
- Tweak the prompt to improve performance or get more specific explanations.

If you want a high-level introduction to LLMs in the context of Dataiku, check out 
[this guide](https://content.dataiku.com/llms-dataiku/dataiku-llm-starter-kit).

Here are the complete versions of the code presented in this tutorial:

```````{tabs}
`````{group-tab} LLM Mesh
````{dropdown} [notebook.py](./assets/notebook.py)

:::{literalinclude} assets/notebook.py
:language: python
:::
````

````{dropdown} [recipe.py](./assets/recipe.py)

:::{literalinclude} assets/recipe.py
:language: python
:::
````
`````

`````{group-tab} Langchain-compatible LLM
````{dropdown} [notebook.py](./assets/notebook_lcllm.py)

:::{literalinclude} assets/notebook_lcllm.py
:language: python
:::
````

````{dropdown} [recipe.py](./assets/recipe_lcllm.py)

:::{literalinclude} assets/recipe_lcllm.py
:language: python
:::
````
`````

`````{group-tab} Langchain-compatible chat LLM
````{dropdown} [notebook.py](./assets/notebook_chat.py)

:::{literalinclude} assets/notebook_chat.py
:language: python
:::
````

````{dropdown} [recipe.py](./assets/recipe_chat.py)

:::{literalinclude} assets/recipe_chat.py
:language: python
:::
````
`````
``````