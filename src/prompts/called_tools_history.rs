use tera::Tera;
use pyo3::prelude::*;
use serde::Serialize;


#[derive(FromPyObject,Serialize,Debug)]
pub struct CalledTool {
    pub name: String,
    pub arguments: String,
    pub result: String,
}

const TEMPLATE: &str = r#"
Previous tools have been called. {% for tool in called_tools %}
- Tool: {{ tool.name }}
- Arguments: {{ tool.arguments }}
- Result:
```
{{ tool.result }}
```
{%- endfor -%}
"#;

#[allow(dead_code)]
pub fn get_called_tools_history_prompt(tera: &mut Tera) {
    let template = TEMPLATE;
    tera.add_raw_template("called_tools_history", template).unwrap();
}