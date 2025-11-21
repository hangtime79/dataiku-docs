print("📚 .. imports ... ")
print("🤖 .. Python client for OpenAI API calls ...")
from openai import OpenAI

print("⏱ .. library for timing ...")
import time
import httpx # in case of self-signed certificates
print("\n\n")

# Specify the Dataiku OpenAI-compatible public API URL, e.g. http://my.dss/public/api/projects/PROJECT_KEY/llms/openai/v1/
BASE_URL = ""

# Use your Dataiku API key instead of an OpenAI secret
API_KEY = ""

# Fill with your LLM id - to get the list of LLM ids, you can use dataiku.api_client().project.list_llms()
LLM_ID = "" 

# Create an OpenAI client
open_client = OpenAI(
  base_url=BASE_URL,
  api_key=API_KEY,
  http_client=httpx.Client(verify=False)  # in case of self-signed certificates
)

print("🔑 .. client created, key set ...")


DEFAULT_TEMPERATURE = 0
DEFAULT_MAX_TOKENS = 1000

print("\n\n")

context = '''You are a capable ghost writer 
  who helps college applicants'''

content = '''Write a complete 500-word short essay 
  for a college application on the topic - 
  My first memories.'''

prompt = [
    {"role": "system", 
     "content": context}, 
    {'role': 'user',
     'content': content}
]


print(f"This is the prompt: {content}")
print("\n\n")  

print("⏲ .. Record the time before the request is sent ..")
start_time = time.time()

print("📤 .. Send a ChatCompletion request ...")
response = open_client.chat.completions.create(
    model=LLM_ID,
    stream=True,
    messages=prompt,
    temperature=DEFAULT_TEMPERATURE,
    max_tokens=DEFAULT_MAX_TOKENS
)


collected_chunks = []
collected_messages = []

# iterate through the stream of events
for chunk in response:
    chunk_time = time.time() - start_time  # calculate the time delay of the chunk
    collected_chunks.append(chunk)  # save the event response
    chunk_message = chunk.choices[0].delta  # extract the message
    collected_messages.append(chunk_message)  # save the message
    if hasattr(chunk_message, 'content'):
        print(chunk_message.content, end="")

print("\n\n\n")  

# print the time delay and text received
print(f"Full response received {chunk_time:.2f} seconds after request")
full_reply_content = ''.join([m.content for m in collected_messages if hasattr(m, 'content') and m.content is not None])