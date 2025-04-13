from agent.agent import create_agent
from agent.ipython_shell_manager import ipython_shell_manager
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage


chat_id = "b4657a15-e8f4-4cb3-9d59-1347d0c82966"
ipython_shell = ipython_shell_manager.get_shell(chat_id)
code = """
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text

engine = create_engine(
"postgresql+psycopg://username:password@localhost:5432/air_gpt"
)
"""
LLM = ChatOpenAI(
    api_key="your_api_key",
    model="gpt-4o",
    temperature=0
)
ipython_shell_manager.setup_environment(ipython_shell, code)
agent = create_agent(chat_id, ipython_shell, LLM)
config = {"configurable": {"thread_id": chat_id}}

messages = [
    HumanMessage(content="What was the longest continuous period of pollution in Beijing recently?")
]
input_message = {"messages": messages}
response = agent.invoke(input_message,  config=config)
print(response["messages"][-1].content)