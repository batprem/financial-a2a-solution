import time
from typing import AsyncGenerator

from textual import on, work
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Footer, Header, Input, Markdown

SYSTEM = """Formulate all responses as if you where the sentient AI named Mother from the Aliens movies."""


class Prompt(Markdown):
    pass


class Response(Markdown):
    BORDER_TITLE = "Mother2"


class Other(Markdown):
    def __init__(
        self, content: str = "", border_title: str = "Other", **kwargs
    ):
        self.BORDER_TITLE = border_title
        super().__init__(content, **kwargs)


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
    Response {
        border: $success;
        background: $success 10%;   
        color: $text;             
        margin: 1;      
        padding: 1 2 0 2;
    }
    Other {
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
            yield Response("INTERFACE 2037 READY FOR INQUIRY")
        yield Input(placeholder="How can I help you?")
        yield Footer()

    def on_mount(self) -> None:
        pass

    @on(Input.Submitted)
    async def on_input(self, event: Input.Submitted) -> None:
        chat_view = self.query_one("#chat-view")
        event.input.clear()
        await chat_view.mount(Prompt(event.value))
        await chat_view.mount(response := Response())
        # await chat_view.mount)
        response.anchor()
        self.send_prompt(event.value, response)

    async def mount_other(self, border_title: str):
        chat_view = self.query_one("#chat-view")
        other = Other(border_title=border_title)
        await chat_view.mount(other)
        return other

    @work(thread=True)
    async def send_prompt(self, prompt: str, response: Response) -> None:
        response_content = ""
        if prompt == "/exit":
            self.exit()
        llm_response = mock_stream(prompt, system=SYSTEM)
        async for chunk in llm_response:
            response_content += chunk
            self.call_from_thread(response.update, response_content)
        llm_response = mock_stream(prompt, system=SYSTEM)

        other = self.call_from_thread(self.mount_other, border_title="test")

        response_content = ""
        async for chunk in llm_response:
            response_content += chunk
            self.call_from_thread(other.update, response_content)


async def mock_stream(
    prompt: str, *args, **kwargs
) -> AsyncGenerator[str, None]:
    for c in """<b>Hello</b>, how can I help you?
```json
{
    "name": "John",
    "age": 30
}
```
<span>some *blue* text</span>.
""":
        time.sleep(0.01)
        yield c


if __name__ == "__main__":
    app = MotherApp()
    app.run()
