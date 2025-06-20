use tera::Tera;


const TEMPLATE: &str = r#"You duty is to decide which agent to consult or ask for help to answer the question.
The question is:

{{ question }}

{{ call_agent_prompt }}

{{ agent_prompt }}

You must answer in the following format:


<thoughts>
thoughts:
- ...
- ...
- ...
</thoughts>

<selected_agents>
```json
[
        {
            "index": agent_index (integer),
            "name": "agent_name",
            "prompt": "prompt_to_agent"
        },
        ...
]
```
</selected_agents>

Note:
- You can leave the selected agents empty if you think none of the agents are relevant to the question or given contexts are enough to answer the question.
- You can select multiple agents if you think multiple agents are relevant to the question.
- You must ensure that your selected agents exist in the agents list.
- You `agent_name` must be one of the agent names in the agents list, and you must spell it correctly.
- If there is no need to call any agent, Please give your answer by continuing the following format:
{%if tone%}
Answer tone: {{tone}}
{%endif%}

You must answer in the following format:
<answer>
<Your answer here>
</answer>
"#;


#[allow(dead_code)]
pub fn get_agent_decide_prompt(tera: &mut Tera) {
    tera.add_raw_template("agent_decide", TEMPLATE).unwrap();
}