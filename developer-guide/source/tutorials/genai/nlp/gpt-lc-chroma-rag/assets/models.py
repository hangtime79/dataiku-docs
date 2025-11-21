from langchain.chat_models import ChatOpenAI
from gpt_utils.auth import get_api_key

def get_gpt_llm(secret_name: str):
    chat_params = {
        "model": "gpt-3.5-turbo-16k", # Bigger context window
        "openai_api_key": get_api_key(secret_name),
        "temperature": 0.5, # To avoid pure copy-pasting from docs lookup
        "max_tokens": 8192
    }
    llm = ChatOpenAI(**chat_params)
    return llm
