use pyo3::prelude::*;
use serde::Serialize;
use std::collections::HashMap;
use tera::Tera;

#[derive(FromPyObject, Serialize, Debug)]
pub struct ToolInputSchema {
    pub properties: HashMap<String, String>,
}

#[derive(FromPyObject, Serialize, Debug)]
#[allow(non_snake_case)]
pub struct Tool {
    name: String,
    description: String,
    inputSchema: String,
}

const TEMPLATE: &str = r#"Tools{% for tool in tools %}
- {{loop.index}}: {{ tool.name }}
- Description: {{ tool.description }}
- Input Schema: {{tool.inputSchema}}{% endfor %}
"#;

#[allow(dead_code)]
pub fn get_tools_prompt(tera: &mut Tera) {
    tera.add_raw_template("tools", TEMPLATE).unwrap();
}
