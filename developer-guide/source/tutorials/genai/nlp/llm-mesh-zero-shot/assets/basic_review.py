import dataiku

GPT_35_LLM_ID = "" # Fill with your gpt-3.5-turbo LLM id

client = dataiku.api_client()
project = client.get_default_project()
llm = project.get_llm(GPT_35_LLM_ID)

reviews = [
    {
        "sentiment": 0,
        "text": "This movie was horrible: bad actor performance, poor scenario and ugly CGI effects."
    },
    {
        "sentiment": 1,
        "text": "Beautiful movie with an original storyline and top-notch actor performance."
    }
]

compl = llm.new_completion()

sys_msg = """
You are a movie review expert.
Your task is to classify movie review sentiments in two categories: 0 for negative reviews,
1 for positive reviews. Do not answer anything else than 0 or 1."
"""

for r in reviews:
    q = compl \
        .with_message(role="system", message=sys_msg) \
        .with_message(f"Classify this movie review: {r['text']}")
    resp = q.execute()
    if resp.success:
        print(f"{r[r'text']}\n Inference: {resp.text}\n Ground truth: {r['sentiment']}\n{20*'---'}")
    else:
        raise Exception("LLM inference failed!")