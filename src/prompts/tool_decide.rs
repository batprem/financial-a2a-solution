use tera::Tera;


const TEMPLATE: &str = r#"You duty is to decide which tool to use to answer the question.
The question is:

{{ question }}

{{ called_tools }}

{{ tool_prompt }}

You must answer in the following format:


<thoughts>
thoughts:
- ...
- ...
- ...
</thoughts>

<selected_tools>
```json
[
        {
            "name": "tool_name",
            "arguments": {
                "argument_name": "argument_value"
            }
        },
        ...
]
```
</selected_tools>

<answer>
YOUR ANSWER HERE YOU MUST ANSWER IF YOU THINK YOU STILL NEED TO CALL MORE TOOLS TO ANSWER THE QUESTION, LEAVE THIS BLANK.
</answer>


Note:
- You can leave the selected tools empty if you think none of the tools are relevant to the question or given contexts are enough to answer the question.
- You can select multiple tools if you think multiple tools are relevant to the question.
- You `tool_name` must be one of the tool names in the tools list, and you must spell it correctly.
- If there is no need to call any tool, answer the question

{%- if tone -%}
Answer tone: {{tone}}
{%- endif -%}
"#;

#[allow(dead_code)]
pub fn get_tool_decide_prompt(tera: &mut Tera) {
    tera.add_raw_template("tool_decide", TEMPLATE).unwrap();
}