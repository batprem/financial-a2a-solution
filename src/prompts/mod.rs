mod tools;
mod called_tools_history;
mod tool_decide;
mod agent_answer;
mod available_agents;
mod agent_decide;
use tera::Tera;

pub use tools::Tool;
#[allow(unused_imports)]
pub use called_tools_history::CalledTool;
#[allow(unused_imports)]
pub use agent_answer::AgentAnswer;
#[allow(unused_imports)]
pub use available_agents::AgentCard;


#[allow(dead_code)]
pub fn get_tera() -> Tera {
    let mut tera = Tera::default();
    tools::get_tools_prompt(&mut tera);
    called_tools_history::get_called_tools_history_prompt(&mut tera);
    tool_decide::get_tool_decide_prompt(&mut tera);
    agent_answer::get_agent_answer_prompt(&mut tera);
    available_agents::get_available_agents_prompt(&mut tera);
    agent_decide::get_agent_decide_prompt(&mut tera);
    tera
}
