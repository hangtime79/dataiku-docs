import json
from pydantic import BaseModel, Field
from typing import List
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain.prompts import ChatPromptTemplate
from langchain.prompts import HumanMessagePromptTemplate
from langchain.prompts import SystemMessagePromptTemplate
from langchain.chat_models.base import BaseChatModel
from langchain.schema import BaseOutputParser
from langchain.chains.base import Chain
from langchain.chains.question_answering import load_qa_chain


TOPICS = {
    "environment": "environmental sustainability and measures against climate change",
    "economy": "economic growth and development",
    "society": "poverty and inequality reduction"
}


class RegionOutlook(BaseModel):
    region_name: str = Field(description='The name of the region of interest')
    environment: str = Field(description=TOPICS["environment"])
    economy: str = Field(description=TOPICS["economy"])
    society: str = Field(description=TOPICS["society"])


class RegionOutlookList(BaseModel):
    items: List[RegionOutlook] = Field(description="The list of region states")

        
def build_qa_chain(llm: type[BaseChatModel],
                   parser: type[BaseOutputParser]) -> type[Chain]:

    # -- Create system prompt template
    sys_tpl = "You are a helpful assistant with expertise in trade and international economics."
    sys_msg_pt = SystemMessagePromptTemplate.from_template(sys_tpl)

    usr_pt = PromptTemplate(template="{context}\n{question}\n{fmt}",
                            input_variables=["context", "question"],
                            partial_variables={"fmt": parser.get_format_instructions()})
    usr_msg_pt = HumanMessagePromptTemplate(prompt=usr_pt)

    # -- Combine (system, user) into a chat prompt template
    prompt = ChatPromptTemplate.from_messages([sys_msg_pt, usr_msg_pt])

    # Create chain for QA and pass the prompt instead of plain text query
    chain = load_qa_chain(llm=llm, chain_type="stuff", prompt=prompt)
    return chain


def run_qa_chain(chain, query, vec_db) -> str:
    # Lookup
    docs = vec_db.similarity_search(query, k=10, include_metadata=True)
    res = chain({"input_documents": docs, "question": query})
    return res["output_text"]
        

    

