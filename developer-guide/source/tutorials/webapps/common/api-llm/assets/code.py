from dash import html

import dataiku
from flask import request, make_response

LLM_ID = "openai:openai:gpt-3.5-turbo"
llm = dataiku.api_client().get_default_project().get_llm(LLM_ID)


@app.server.route('/query', methods=['POST'])
def query():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        json = request.json
        user_message = json.get('message', None)
        if user_message:
            completion = llm.new_completion()
            completion.with_message(user_message)
            resp = completion.execute()

            if resp.success:
                msg = resp.text
            else:
                msg = "Something went wrong"
        else:
            msg = "No message was found"

        response = make_response(msg)
        response.headers['Content-type'] = 'application/json'
        return response
    else:
        return 'Content-Type is not supported!'


# We need to have a layout (even if we don't use it)
# In case we don't set a layout dash application won't start
app.layout = html.Div("HeadLess WebAPP. No Interface")
