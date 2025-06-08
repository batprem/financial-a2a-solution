from dotenv import load_dotenv
from collections.abc import AsyncGenerator
from typing import Any

from textual import on, work
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Footer, Header, Input, Markdown
from financial_a2a_solution.the_solution import utils  # type: ignore
from financial_a2a_solution.main_agent.agent import Agent as ClientAgent

SYSTEM = """Formulate all responses as if you where the sentient AI named Mother from the Aliens movies."""  # noqa: E501


class Prompt(Markdown):
    pass


class MainAgent(Markdown):
    BORDER_TITLE = "Main Agent"


class Agent(Markdown):
    def __init__(
        self,
        content: str = "",
        border_title: str = "Agent",
        **kwargs: dict[str, Any],
    ):
        self.BORDER_TITLE = border_title
        super().__init__(content, **kwargs)  # pyrefly: ignore


class MotherApp(App):
    AUTO_FOCUS = "Input"

    CSS = """
    Prompt {
        background: $primary 10%;
        color: $text;
        margin: 1;        
        margin-left: 8;
        padding: 1 2 0 2;
    }
    MainAgent {
        border: $success;
        background: $success 10%;   
        color: $text;             
        margin: 1;      
        padding: 1 2 0 2;
    }
    Agent {
        background: $panel 10%;
        border: wide $panel;
        color: $text;             
        margin: 1;      
        margin-right: 8; 
        padding: 1 2 0 2;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        with VerticalScroll(id="chat-view"):
            yield MainAgent("INTERFACE 2037 READY FOR INQUIRY")
        yield Input(placeholder="How can I help you?")
        yield Footer()

    def on_mount(self) -> None:
        pass

    @on(Input.Submitted)
    async def on_input(self, event: Input.Submitted) -> None:
        chat_view = self.query_one("#chat-view")
        event.input.clear()
        await chat_view.mount(Prompt(event.value))

        # await chat_view.mount)
        # main_agent.anchor()
        self.send_prompt(event.value)

    async def mount_main_agent(self) -> MainAgent:
        chat_view = self.query_one("#chat-view")
        main_agent = MainAgent()
        await chat_view.mount(main_agent)
        return main_agent

    async def mount_agent(self, border_title: str) -> Agent:
        chat_view = self.query_one("#chat-view")
        agent = Agent(border_title=border_title)

        await chat_view.mount(agent)

        return agent

    def render_content(self, content: str) -> str:
        return (
            content.replace("<thoughts>", "# Thoughts:")
            .replace("<answer>", "# Answer:")
            .replace("<selected_tools>", "# Selected Tools:")
            .replace("<selected_agents>", "# Selected Agents:")
            .replace("</thoughts>", "")
            .replace("</answer>", "")
            .replace("</selected_tools>", "")
            .replace("</selected_agents>", "")
        )

    @work(thread=True)
    async def send_prompt(self, prompt: str) -> None:
        response_content = ""
        if prompt == "/exit":
            self.exit()
        llm_response = mock_stream(prompt, system=SYSTEM)
        agent_blocks: list[MainAgent | Agent] = []
        active_agent_name: str | None = None
        async for chunk in llm_response:
            response_content += chunk
            streamed_tags = utils.parse_streamed_tags(response_content)
            if streamed_tags:
                last_tag = streamed_tags[-1]

                if last_tag["tag"] == "main_agent":
                    try:
                        main_agent = agent_blocks[-1]
                        create_new_main_agent_block_flag = not isinstance(
                            main_agent, MainAgent
                        )

                    except IndexError:
                        create_new_main_agent_block_flag = True

                    if create_new_main_agent_block_flag:
                        try:
                            previous_agent_block = agent_blocks[-2]
                            second_last_tag = streamed_tags[-2]
                            self.call_from_thread(
                                previous_agent_block.update,
                                self.render_content(second_last_tag["content"]),
                            )
                        except IndexError:
                            pass
                        main_agent = self.call_from_thread(
                            self.mount_main_agent,
                        )
                        agent_blocks.append(main_agent)
                        active_agent_name = "Main Agent"

                    main_agent.anchor()
                    self.call_from_thread(
                        main_agent.update,
                        self.render_content(last_tag["content"]),
                    )

                if last_tag["tag"] == "agent":
                    agent_name = last_tag["attributes"].get("name", "Agent")
                    try:
                        agent = agent_blocks[-1]
                        create_new_agent_block_flag = (
                            not isinstance(agent, Agent)
                            or agent_name != active_agent_name
                        )

                    except IndexError:
                        create_new_agent_block_flag = True

                    if create_new_agent_block_flag:
                        # Set the active agent name
                        active_agent_name = agent_name
                        try:
                            previous_agent_block = agent_blocks[-2]
                            second_last_tag = streamed_tags[-2]
                            self.call_from_thread(
                                previous_agent_block.update,
                                self.render_content(second_last_tag["content"]),
                            )
                        except IndexError:
                            pass

                        # Mount the new agent block
                        agent = self.call_from_thread(
                            self.mount_agent,
                            border_title=last_tag["attributes"].get(
                                "name", "Agent"
                            ),
                        )
                        agent_blocks.append(agent)

                    # Update the agent block with the new content
                    agent.anchor()
                    self.call_from_thread(
                        agent.update,
                        self.render_content(last_tag["content"]),
                    )


async def mock_stream(
    prompt: str, *_: Any, **__: Any
) -> AsyncGenerator[str, None]:
    balance_sheet_agent_url = "http://localhost:9999"
    technical_analyser_agent_url = "http://localhost:9998"
    env_file = ".env"

    load_dotenv(env_file)
    agent = ClientAgent(
        mode="stream",
        token_stream_callback=None,
        agent_urls=[balance_sheet_agent_url, technical_analyser_agent_url],
        agent_prompt="Act as a financial expert and answer the question in a formal, robust and convincing tone.",  # noqa: E501
    )

    async for chunk in agent.stream(prompt):
        yield chunk


if __name__ == "__main__":
    app = MotherApp()
    app.run()
