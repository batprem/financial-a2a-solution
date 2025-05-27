from financial_a2a_solution.balance_sheet_agent.constant import GOOGLE_API_KEY
from financial_a2a_solution.balance_sheet_agent.mcp import (
    call_mcp_tool,
    get_mcp_tool_prompt,
)

import asyncio
import commentjson as json
import re
from collections.abc import AsyncGenerator, Callable, Generator
from pathlib import Path
from typing import Literal

import google.generativeai as genai
from jinja2 import Template
from mcp.types import CallToolResult


from pydantic import BaseModel

class StreamChunk(BaseModel):
    is_task_complete: bool
    require_user_input: bool
    content: str

class ToolCall(BaseModel):
    tool: str
    arguments: dict
    isError: bool
    result: str


dir_path = Path(__file__).parent

with Path(dir_path / "decide.jinja").open("r") as f:
    decide_template = Template(f.read())

with Path(dir_path / "called_tools_history.jinja").open("r") as f:
    called_tools_history_template = Template(f.read())


def stream_llm(prompt: str) -> Generator[str, None]:
    """Stream LLM response.

    Args:
        prompt (str): The prompt to send to the LLM.

    Returns:
        Generator[str, None, None]: A generator of the LLM response.
    """
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    for chunk in model.generate_content(prompt, stream=True):
        yield chunk.text


class MCPParameters(BaseModel):
    url: str | None = None
    cmd: list[str] | None = None


class Agent:
    """Agent for interacting with the Google Gemini LLM in different modes."""

    def __init__(
        self,
        mode: Literal["complete", "stream"] = "stream",
        token_stream_callback: Callable[[str], None] | None = None,
        mcp_parameters: MCPParameters | None = None,
    ):
        self.mode = mode
        self.token_stream_callback = token_stream_callback
        self.mcp_parameters = mcp_parameters

    async def decide(
        self, question: str, called_tools: list[ToolCall] | None = None
    ) -> AsyncGenerator[str, None]:
        """Decide which tool to use to answer the question.

        Args:
            question (str): The question to answer.
            called_tools (list[dict]): The tools that have been called.
        """
        if self.mcp_parameters is None:
            for chunk in stream_llm(question):
                yield chunk
            return
        tool_prompt = await get_mcp_tool_prompt(**self.mcp_parameters.model_dump())
        if called_tools:
            called_tools_prompt = called_tools_history_template.render(
                called_tools=called_tools
            )
        else:
            called_tools_prompt = ""

        prompt = decide_template.render(
            question=question,
            tool_prompt=tool_prompt,
            called_tools=called_tools_prompt,
        )
        for chunk in stream_llm(prompt):
            yield chunk

    def extract_tools(self, response: str) -> list[dict]:
        """Extract the tools from the response.

        Args:
            response (str): The response from the LLM.
        """
        pattern = r"```json\n(.*?)\n```"
        match = re.search(pattern, response, re.DOTALL)
        if match:
            return json.loads(match.group(1))
        return []

    async def call_tool(self, tools: list[dict]) -> tuple[CallToolResult, ...]:
        """Call the tool.

        Args:
            tools (list[dict]): The tools to call.
        """
        if self.mcp_parameters is None:
            return tuple()
        return await asyncio.gather(
            *[
                call_mcp_tool(
                    **self.mcp_parameters.model_dump(),
                    tool_name=tool["name"],
                    arguments=tool["arguments"],
                )
                for tool in tools
            ]
        )

    async def stream(self, question: str) -> AsyncGenerator[StreamChunk, None]:
        """Stream the process of answering a question, possibly involving tool calls.

        Args:
            question (str): The question to answer.

        Yields:
            dict: Streaming output, including intermediate steps and final result.
        """  # noqa: E501
        called_tools: list[ToolCall] = []

        for i in range(10):
            yield StreamChunk(
                is_task_complete=False,
                require_user_input=False,
                content=f"Step {i}",
            )

            response = ""
            async for chunk in self.decide(question, called_tools):
                response += chunk
                yield StreamChunk(
                    is_task_complete=False,
                    require_user_input=False,
                    content=chunk,
                )
            tools = self.extract_tools(response)
            if not tools:
                break
            results = await self.call_tool(tools)

            called_tools.extend([
                ToolCall(
                    tool=tool["name"],
                    arguments=tool["arguments"],
                    isError=result.isError,
                    result=getattr(result.content[0], "text", ""),
                )
                for tool, result in zip(tools, results, strict=True)
            ])
            called_tools_history = called_tools_history_template.render(
                called_tools=called_tools, question=question
            )

            yield StreamChunk(
                is_task_complete=False,
                require_user_input=False,
                content=called_tools_history,
            )

        yield StreamChunk(
            is_task_complete=True,
            require_user_input=False,
            content="Task completed",
        )


if __name__ == "__main__":
    agent = Agent(
        token_stream_callback=lambda token: print(token, end="", flush=True),
        mcp_parameters=MCPParameters(url="https://gitmcp.io/google/A2A"),
    )

    async def main():
        """Main function."""
        async for chunk in agent.stream("What is A2A Protocol?"):
            print(chunk)

    asyncio.run(main())
