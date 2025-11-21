from dataikuapi.dss.langchain import DKUChatModel
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
import json
from typing import Dict, List


def predict_sentiment(chat: DKUChatModel, review: str):
    system_msg = """
    You are an assistant that classifies reviews according to their sentiment. 
    Respond strictly with this JSON format: {"llm_sentiment": "xxx"} where xxx should only be either: 
    pos if the review is positive 
    ntr if the review is neutral or does not contain enough information 
    neg if the review is negative 
    No other value is allowed.
    """

    messages = [
        SystemMessage(content=system_msg),
        HumanMessage(content=f"""Review: {review}""")
    ]
    resp = chat.invoke(messages)
    return json.loads(resp.content)


def build_example_msg(rec: Dict) -> List[Dict]:
    example = [
        {"Review": rec['reviewText'], "llm_sentiment": rec['sentiment']}
    ]
    return example


def predict_sentiment_fs(chat: DKUChatModel, review: str, examples: List):
    system_msg = """
    You are an assistant that classifies reviews according to their sentiment. 
    Respond strictly with this JSON format: {"llm_sentiment": "xxx"} where xxx should only be either: 
    pos if the review is positive 
    ntr if the review is neutral or does not contain enough information 
    neg if the review is negative 
    No other value is allowed.
    """

    messages = [
        SystemMessage(content=system_msg),
    ]
    for ex in examples:
        messages.append(HumanMessage(ex.get('Review')))
        messages.append(AIMessage(ex.get('llm_sentiment')))

    messages.append(HumanMessage(content=f"""Review: {review}"""))

    resp = chat.invoke(messages)
    return {'llm_sentiment': resp.content}
