import dataiku

GPT_35_LLM_ID = "" # Fill with your gpt-3.5-turbo LLM id

client = dataiku.api_client()
project = client.get_default_project()
llm = project.get_llm(GPT_35_LLM_ID)

compl = llm.new_completion()
q = compl.with_message("Write a one-sentence positive review for the Lord of The Rings movie trilogy.")
resp = q.execute()
if resp.success:
    print(resp.text)
else:
    raise Exception("LLM inference failed!")

# The Lord of the Rings is a thrilling epic adventure that follows a group of
# unlikely heroes as they journey through dangerous lands in order to destroy
# a powerful ring and save their world from eternal darkness.
