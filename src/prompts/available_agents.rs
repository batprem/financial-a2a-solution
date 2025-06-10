use tera::Tera;
use pyo3::prelude::*;
use serde::Serialize;


const TEMPLATE: &str = r#"# Agent contexts

These are some consults from agent(s) that may be useful to answer the question
{% for agent in agent_cards %}
Agent index: {{loop.index}}
Agent name: {{agent.name}}
Agent description: {{agent.description}}
Agent skills: {% for skill in agent.skills%}
    - name: {{skill.name}}
        - description: {{skill.description}}
        - example: {{skill.examples}}{% endfor %}{% endfor %}
-------------------"#;

#[derive(FromPyObject,Serialize,Debug)]
pub struct AgentCard {
    pub name: String,
    pub description: String,
    pub skills: Vec<Skill>,
}

#[derive(FromPyObject,Serialize,Debug)]
pub struct Skill {
    pub name: String,
    pub description: String,
    pub examples: Vec<String>,
}

#[allow(dead_code)]
pub fn get_available_agents_prompt(tera: &mut Tera) {
    tera.add_raw_template("available_agents", TEMPLATE).unwrap();
}