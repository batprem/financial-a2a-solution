use serde::Serialize;
use tera::Tera;
use pyo3::prelude::*;
use std::collections::HashMap;

#[derive(FromPyObject,Serialize,Debug)]
pub struct ToolInputSchema {
    pub properties: HashMap<String, String>,
}

#[derive(FromPyObject,Serialize,Debug)]
#[allow(non_snake_case)]
pub struct Tool {
    name: String,
    description: String,
    inputSchema: String,
}

pub fn get_tools_prompt(tera: &mut Tera) {
    let template = r#"Tools{% for tool in tools %}
- {{loop.index}}: {{ tool.name }}
- Description: {{ tool.description }}
- Input Schema: {{tool.inputSchema}}{% endfor %}
"#;
    tera.add_raw_template("tools", template).unwrap();
}