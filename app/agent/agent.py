from langgraph.prebuilt import chat_agent_executor
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
from app.tools import TOOLS
from app.agent.prompts import SYSTEM_PROMPT
from app.llm.model import llm

agent = create_agent(model=llm,
tools=TOOLS,
system_prompt=SYSTEM_PROMPT)
