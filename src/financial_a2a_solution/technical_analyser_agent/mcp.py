import asyncio
import json
from pathlib import Path

from mcp.client.session import ClientSession
from mcp.client.sse import sse_client
from mcp.client.stdio import StdioServerParameters, stdio_client
from mcp.types import CallToolResult, TextContent

from financial_a2a_solution.the_solution import prompts  # type: ignore
from financial_a2a_solution.types import Tool

dir_path = Path(__file__).parent


async def get_mcp_tool_prompt(
    *,  # pyright: ignore
    url: str | None = None,
    cmd: list[str] | None = None,
) -> str:
    """Get the MCP tool prompt for a given URL.

    Args:
        url (str): The URL of the MCP tool.
        cmd (list[str]): The command to call the MCP tool.

    Returns:
        str: The MCP tool prompt.
    """
    if not url and not cmd:
        raise ValueError("Either url or cmd must be provided")
    if url and cmd:
        raise ValueError("Only one of url or cmd must be provided")

    if url:
        async with (
            sse_client(url) as (read, write),
            ClientSession(read, write) as session,
        ):
            await session.initialize()

            resources = await session.list_tools()
            tools = [
                Tool(
                    name=tool.name,
                    description=tool.description,
                    inputSchema=json.dumps(tool.inputSchema),
                )
                for tool in resources.tools
            ]
            return prompts.get_tools_prompt(tools)
    if cmd:
        command, *args = cmd
        async with (
            stdio_client(
                StdioServerParameters(command=command, args=args)  # pyright: ignore
            ) as (read, write),
            ClientSession(read, write) as session,
        ):
            await session.initialize()
            resources = await session.list_tools()
            tools = [
                Tool(
                    name=tool.name,
                    description=tool.description,
                    inputSchema=json.dumps(tool.inputSchema),
                )
                for tool in resources.tools
            ]
            return prompts.get_tools_prompt(tools)
    raise ValueError("Either url or cmd must be provided")


async def call_mcp_tool(
    *,  # pyright: ignore
    url: str | None = None,
    cmd: list[str] | None = None,
    tool_name: str | None = None,
    arguments: dict | None = None,
) -> CallToolResult:
    """Call an MCP tool with the given URL and tool name.

    Args:
        url (str): The URL of the MCP tool.
        cmd (list[str]): The command to call the MCP tool.
        tool_name (str): The name of the tool to call.
        arguments (dict | None, optional): The arguments to pass to the tool. Defaults to None.

    Returns:
        CallToolResult: The result of the tool call.
    """  # noqa: E501
    if not tool_name:
        raise ValueError("tool_name (str) must be provided")

    if url:
        async with (
            sse_client(url) as (read, write),
            ClientSession(read, write) as session,
        ):
            await session.initialize()
            return await session.call_tool(tool_name, arguments=arguments)
    if cmd:
        command, *args = cmd
        async with (
            stdio_client(
                StdioServerParameters(command=command, args=args)  # pyright: ignore
            ) as (read, write),
            ClientSession(read, write) as session,
        ):
            await session.initialize()
            return await session.call_tool(tool_name, arguments=arguments)
    else:
        raise ValueError("Either url or cmd must be provided")


if __name__ == "__main__":
    print(
        asyncio.run(
            get_mcp_tool_prompt(
                cmd=[
                    "uvx",
                    # "--with",
                    # "websocket",
                    "--with",
                    "websocket-client",
                    "technical-backtesting-mcp",
                ]
            )
        )
    )
    result = asyncio.run(
        call_mcp_tool(
            cmd=[
                "uvx",
                # "--with",
                # "websocket",
                "--with",
                "websocket-client",
                "technical-backtesting-mcp",
            ],
            tool_name="back_test_asset_price_cross_moving_average",
            arguments={
                "n1": 10,
                "n2": 20,
                "cash": 10000,
                "symbol": "SET:KBANK",
                "commission": 0.002,
            },
        )
    )
    for content in result.content:
        validated_content = TextContent.model_validate(content)
        print(validated_content.text)
