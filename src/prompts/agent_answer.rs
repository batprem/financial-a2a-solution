use tera::Tera;
use pyo3::prelude::*;
use serde::Serialize;


const TEMPLATE: &str = r#"
Previous agents have been called.
{%- for agent in called_agents -%}
- Agent: {{ agent.name }}
- Prompt: {{ agent.prompt }}
- Answer: {{ agent.answer }}
-------
{%- endfor -%}
"#;


#[derive(FromPyObject,Serialize,Debug)]
pub struct AgentAnswer {
    pub name: String,
    pub prompt: String,
    pub answer: String,
}

#[allow(dead_code)]
pub fn get_agent_answer_prompt(tera: &mut Tera) {
    tera.add_raw_template("agent_answer", TEMPLATE).unwrap();
}