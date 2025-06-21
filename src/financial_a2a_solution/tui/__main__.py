from dotenv import load_dotenv
from collections.abc import AsyncGenerator
from typing import Any

from textual import on, work
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Footer, Header, Input, Markdown
from financial_a2a_solution.the_solution import utils  # type: ignore
from financial_a2a_solution.main_agent.agent import Agent as ClientAgent


class Prompt(Markdown):
    """A Markdown widget for displaying user prompts in the chat interface."""


class MainAgent(Markdown):
    """A Markdown widget representing the main agent's responses in the chat interface."""  # noqa: E501
    BORDER_TITLE = "Main Agent"


class Agent(Markdown):
    """A Markdown widget for displaying responses from secondary agents with customizable borders."""  # noqa: E501
    def __init__(
        self,
        content: str = "",
        border_title: str = "Agent",
        **kwargs: dict[str, Any],
    ):
        """Initialize an Agent widget.

        Args:
            content (str): The initial content to display.
            border_title (str): The title to display on the border.
            **kwargs: Additional keyword arguments for the Markdown widget.
        """
        self.BORDER_TITLE = border_title
        super().__init__(content, **kwargs)  # pyrefly: ignore


class DataKarateChatApp(App):
    """A Textual TUI application for interacting with financial agents via chat."""  # noqa: E501
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
        """Compose the UI layout for the chat application.

        Returns:
            ComposeResult: The composed UI elements.
        """
        yield Header()
        with VerticalScroll(id="chat-view"):
            yield MainAgent("INTERFACE 2037 READY FOR INQUIRY")
        yield Input(placeholder="How can I help you?")
        yield Footer()

    def on_mount(self) -> None:
        """Called when the application is mounted. Currently does nothing."""

    @on(Input.Submitted)
    async def on_input(self, event: Input.Submitted) -> None:
        """Handle user input submission, display the prompt, and send it to the agent.

        Args:
            event (Input.Submitted): The input submission event.
        """  # noqa: E501
        chat_view = self.query_one("#chat-view")
        event.input.clear()
        await chat_view.mount(Prompt(event.value))

        self.send_prompt(event.value)

    async def mount_main_agent(self) -> MainAgent:
        """Mount a new MainAgent widget to the chat view.

        Returns:
            MainAgent: The mounted MainAgent widget.
        """
        chat_view = self.query_one("#chat-view")
        main_agent = MainAgent()
        await chat_view.mount(main_agent)
        return main_agent

    async def mount_agent(self, border_title: str) -> Agent:
        """Mount a new Agent widget to the chat view with a given border title.

        Args:
            border_title (str): The title for the agent's border.

        Returns:
            Agent: The mounted Agent widget.
        """
        chat_view = self.query_one("#chat-view")
        agent = Agent(border_title=border_title)

        await chat_view.mount(agent)

        return agent

    def render_content(self, content: str) -> str:
        """Render and format the content by replacing custom tags with Markdown headers.

        Args:
            content (str): The content to render.

        Returns:
            str: The formatted content.
        """  # noqa: E501
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
        """Send the user's prompt to the agent, stream the response, and update the UI accordingly.

        Args:
            prompt (str): The user's input prompt.
        """  # noqa: E501
        response_content = ""
        if prompt == "/exit":
            self.exit()
        llm_response = stream_from_a2a(prompt)
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
                        # Set the active agent name
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
                        active_agent_name = agent_name
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


async def stream_from_a2a(
    prompt: str
) -> AsyncGenerator[str, None]:
    """Stream the response from the A2A agent for a given prompt.

    Args:
        prompt (str): The user's input prompt.

    Yields:
        str: Chunks of the agent's response as they are received.
    """
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


def main():
    app = DataKarateChatApp()
    app.run()


if __name__ == "__main__":
    main()
