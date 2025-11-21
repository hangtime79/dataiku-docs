from typing import Dict
from dataikuapi.dss.llm import DSSLLM


def zshot_clf(model: DSSLLM, row: Dict[str,str]) -> Dict[str,str]:
    
    sys_msg = """
    You are a movie review expert.
    Your task is to classify movie review sentiments in two categories: 0 for negative reviews,
    1 for positive reviews. Answer only with one character that is either 0 or 1.
    """

    compl = model.new_completion()
    q = compl \
        .with_message(role="system", message=sys_msg) \
        .with_message(f"Classify this movie review: {row['text']}")
    resp = q.execute()
    if resp.success:
        out_row = dict(row)
        out_row["prediction"] = str(resp.text)
        out_row["llm_id"] = model.llm_id
        return out_row
    else:
        raise Exception(f"LLM inference failed for input row:\n{row}")