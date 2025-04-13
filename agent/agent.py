from agent.tools import PythonREPLTool
from langgraph.prebuilt import create_react_agent
from agent.prompt import AGENT_SYSTEM_PROMPT
from IPython import InteractiveShell
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI

memory = MemorySaver()

def create_agent(
    id: str, ipython_shell: InteractiveShell, llm: ChatOpenAI
):
    """
    Create and configure a data analysis agent with specific tools and language models.

    Returns:
    A React agent equipped with data analysis capabilities.
    """

    python_repl_tool = PythonREPLTool(ipython_shell)
    tools = [python_repl_tool]
    system_message = SystemMessage(content=AGENT_SYSTEM_PROMPT)
    return create_react_agent(
        llm,
        tools,
        checkpointer=memory,
        prompt=system_message
    )
