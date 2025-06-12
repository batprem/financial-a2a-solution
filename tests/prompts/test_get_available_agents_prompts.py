from financial_a2a_solution.the_solution import prompts
from a2a.types import AgentCard, AgentSkill, AgentCapabilities
import pytest


agent_card_1 = AgentCard.model_construct(
    name="Agent 1",
    description="Agent 1 description",
    skills=[
        AgentSkill(
            id="skill_1",
            name="Skill 1",
            description="Skill 1 description",
            examples=["Example 1"],
            tags=["tag1", "tag2"],
        )
    ],
    inputModes=["input_mode_1"],
    outputModes=["output_mode_1"],
    # capabilities=[AgentCapabilities(id="capability_1", name="Capability 1", description="Capability 1 description", tags=["tag1", "tag2"], inputModes=["input_mode_1"], outputModes=["output_mode_1"])],
)

agent_card_2 = AgentCard.construct(
    name="Agent 2",
    description="Agent 2 description",
    skills=[
        AgentSkill(
            id="skill_2",
            name="Skill 2",
            description="Skill 2 description",
            examples=["Example 2"],
            tags=["tag3", "tag4"],
        )
    ],
    inputModes=["input_mode_2"],
    outputModes=["output_mode_2"],
    # capabilities=[AgentCapabilities(id="capability_2", name="Capability 2", description="Capability 2 description", tags=["tag3", "tag4"])],
)


def test_get_available_agents_prompt():
    result = prompts.get_available_agents_prompt([agent_card_1, agent_card_2])
    assert (
        result
        == """# Agent contexts

These are some consults from agent(s) that may be useful to answer the question

Agent index: 1
Agent name: Agent 1
Agent description: Agent 1 description
Agent skills: 
    - name: Skill 1
        - description: Skill 1 description
        - example: [Example 1]
Agent index: 2
Agent name: Agent 2
Agent description: Agent 2 description
Agent skills: 
    - name: Skill 2
        - description: Skill 2 description
        - example: [Example 2]
-------------------"""
    )


def test_get_available_agents_prompt_tuple():
    result = prompts.get_available_agents_prompt((agent_card_1, agent_card_2))
    assert (
        result
        == """# Agent contexts

These are some consults from agent(s) that may be useful to answer the question

Agent index: 1
Agent name: Agent 1
Agent description: Agent 1 description
Agent skills: 
    - name: Skill 1
        - description: Skill 1 description
        - example: [Example 1]
Agent index: 2
Agent name: Agent 2
Agent description: Agent 2 description
Agent skills: 
    - name: Skill 2
        - description: Skill 2 description
        - example: [Example 2]
-------------------"""
    )
