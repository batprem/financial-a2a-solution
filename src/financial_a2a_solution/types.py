from pydantic import BaseModel


class Tool(BaseModel):
    name: str
    description: str
    inputSchema: str
