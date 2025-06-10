from pydantic import BaseModel
from typing import TypedDict


class Tag(TypedDict):
    tag: str
    attributes: dict
    content: str
    is_complete: bool


class Tool(BaseModel):
    name: str
    description: str
    inputSchema: str


class CalledTool(BaseModel):
    name: str
    arguments: str
    isError: bool
    result: str


class AgentAnswer(BaseModel):
    name: str
    prompt: str
    answer: str


class Skill(BaseModel):
    name: str
    description: str
    examples: list[str]
