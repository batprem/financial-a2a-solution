import asyncio
from typing import Literal, cast

import asyncclick as click
import colorama
from dotenv import load_dotenv

from financial_a2a_solution.main_agent.agent import Agent


@click.command()
@click.option(
    "--host",
    "host",
    default=["http://localhost:9999", "http://localhost:9998"],
    multiple=True,
)
@click.option("--mode", "mode", default="streaming")
@click.option("--question", "question", required=True)
@click.option("--env-file", "env_file", default=".env")
async def a_main(
    host: list[str],
    mode: Literal["completion", "streaming"],
    question: str,
    env_file: str,
):
    """Main function to run the A2A Repo Agent client.

    Args:
        host (str): The host address to run the server on.
        port (int): The port number to run the server on.
        mode (Literal['completion', 'streaming']): The mode to run the server on.
        question (str): The question to ask the Agent.
    """  # noqa: E501
    load_dotenv(env_file)
    agent = Agent(
        mode="stream",
        token_stream_callback=None,
        agent_urls=host,
        agent_prompt="Act as a financial expert and answer the question in a formal, robust and convincing tone.",  # noqa: E501
    )

    async for chunk in agent.stream(question):
        if chunk.startswith('<agent name="'):
            print(cast(str, colorama.Fore.CYAN) + chunk, end="", flush=True)
        elif chunk.startswith("</agent>"):
            print(cast(str, colorama.Fore.RESET) + chunk, end="", flush=True)
        else:
            print(chunk, end="", flush=True)


def main() -> None:
    """Main function to run the A2A Repo Agent client."""
    asyncio.run(a_main())


if __name__ == "__main__":
    main()
