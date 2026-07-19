from langchain.agents import create_agent

from app.llm.model import llm
from app.tools import TOOLS
from app.agent.prompts import SYSTEM_PROMPT


agent = create_agent(
    model=llm,
    tools=TOOLS,
    system_prompt=SYSTEM_PROMPT,
)