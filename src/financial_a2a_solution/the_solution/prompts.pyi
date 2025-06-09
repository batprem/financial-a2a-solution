from financial_a2a_solution.types import Tool, CalledTool

__all__ = [
    "get_called_tools_history_prompt",
    "get_tool_decide_prompt",
    "get_tools_prompt",
]

def get_tools_prompt(tools: list[Tool]) -> str: ...
def get_called_tools_history_prompt(called_tools: list[CalledTool]) -> str: ...
def get_tool_decide_prompt(
    question: str, called_tools: str, tool_prompt: str, tone: str | None = None
) -> str: ...
