from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI

from tools.fraud_tools import search_similar_cases
import os
from dotenv import load_dotenv
load_dotenv()


llm = ChatOpenAI(
    openai_api_base="https://router.huggingface.co/novita/v3/openai",
    openai_api_key="HUGGINGFACE_API_KEY",
    model="deepseek/deepseek-v3-0324"
)

tools = [search_similar_cases]

agent_executor = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)
