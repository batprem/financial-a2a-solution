from financial_a2a_solution.types import Tool, CalledTool, AgentAnswer
from a2a.types import AgentCard

def get_tools_prompt(py_tools: list[Tool]) -> str: ...
def get_called_tools_history_prompt(
    py_called_tools: list[CalledTool],
) -> str: ...
def get_tool_decide_prompt(
    question: str, called_tools: str, tool_prompt: str, tone: str | None = None
) -> str: ...
def get_agent_answer_prompt(py_called_agents: list[AgentAnswer]) -> str: ...
def get_available_agents_prompt(
    py_agent_cards: list[AgentCard] | tuple[AgentCard, ...],
) -> str: ...
def get_agent_decide_prompt(
    question: str,
    call_agent_prompt: str,
    agent_prompt: str,
    tone: str | None = None,
) -> str: ...
