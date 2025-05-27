from financial_a2a_solution.types import Tool

class Person:
    name: str
    age: int
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
    def __str__(self) -> str:
        return f"Person(name={self.name}, age={self.age})"
    def __repr__(self) -> str:
        return f"Person(name={self.name}, age={self.age})"
    def greet(self) -> str: ...

def hello_from_bin() -> str:
    pass

def get_tools_prompt(tools: list[Tool]) -> str:
    pass
