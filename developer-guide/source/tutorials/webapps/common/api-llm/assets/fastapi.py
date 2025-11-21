import dataiku
from fastapi import Request, Response
from fastapi.responses import JSONResponse

LLM_ID = "openai:openai:gpt-3.5-turbo"
llm = dataiku.api_client().get_default_project().get_llm(LLM_ID)


@app.post("/query")
async def query(request: Request):
    content_type = request.headers.get("content-type")
    
    if content_type == "application/json":
        json_data = await request.json()
        user_message = json_data.get("message")

        if user_message:
            completion = llm.new_completion()
            completion.with_message(user_message)
            resp = completion.execute()

            msg = resp.text if resp.success else "Something went wrong"
        else:
            msg = "No message was found"

        return JSONResponse(content={"message": msg})
    else:
        return Response(content="Content-Type is not supported!", media_type="text/plain")