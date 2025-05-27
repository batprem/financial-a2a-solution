import click
import uvicorn
from a2a.server.agent_execution import AgentExecutor
from a2a.server.apps.starlette_app import A2AStarletteApplication
from a2a.server.request_handlers.default_request_handler import (
    DefaultRequestHandler,
)
from a2a.server.tasks.inmemory_task_store import InMemoryTaskStore
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
    TaskQueryParams,
    Task,
    MessageSendParams,
    Message
)

from financial_a2a_solution.balance_sheet_agent.agent_executor import BalanceSheetAgentExecutor
from dotenv import load_dotenv


class A2ARequestHandler(DefaultRequestHandler):
    """A2A Request Handler for the A2A Repo Agent."""

    def __init__(
        self, agent_executor: AgentExecutor, task_store: InMemoryTaskStore
    ):
        super().__init__(agent_executor, task_store)

    async def on_get_task(self, params: TaskQueryParams) -> Task | None:
        return await super().on_get_task(params)

    async def on_message_send(
        self, params: MessageSendParams
    ) -> Message | Task:
        return await super().on_message_send(params)


@click.command()
@click.option('--host', 'host', default='localhost')
@click.option('--port', 'port', default=9999)
@click.option('--env-file', 'env_file', default='.env')
def main(host: str, port: int, env_file: str):
    """Start the A2A Repo Agent server.

    This function initializes the A2A Repo Agent server with the specified host and port.
    It creates an agent card with the agent's name, description, version, and capabilities.

    Args:
        host (str): The host address to run the server on.
        port (int): The port number to run the server on.
    """  # noqa: E501
    load_dotenv(env_file)
    skill = AgentSkill(
        id='financial_balance_sheet_agent',
        name='Financial Balance Sheet Agent',
        description='The agent will look up the information about financial balance sheet, do data analysis and answer the question about any stock in Thai stock market.',  # noqa: E501
        tags=['Financial Balance Sheet'],
        examples=['What is financial balance sheet of KBANK?'],
    )

    agent_card = AgentCard(
        name='Financial Balance Sheet Agent',
        description='This agent can access financial statements of the Thai stock company and give brief summary ',  # noqa: E501
        url=f'http://{host}:{port}/',
        version='1.0.0',
        defaultInputModes=['text'],
        defaultOutputModes=['text'],
        capabilities=AgentCapabilities(
            inputModes=['text'],
            outputModes=['text'],
            streaming=True,
        ),
        skills=[skill],
        examples=['What is financial balance sheet of KBANK?', 'Analyze financial balance sheet of KBANK'],
    )

    task_store = InMemoryTaskStore()
    request_handler = A2ARequestHandler(
        agent_executor=BalanceSheetAgentExecutor(),
        task_store=task_store,
    )

    server = A2AStarletteApplication(
        agent_card=agent_card, http_handler=request_handler
    )
    uvicorn.run(server.build(), host=host, port=port)


if __name__ == '__main__':
    main()
