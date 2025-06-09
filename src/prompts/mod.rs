mod tools;
mod called_tools_history;
mod tool_decide;
use tera::Tera;

pub use tools::Tool;
#[allow(unused_imports)]
pub use called_tools_history::CalledTool;


#[allow(dead_code)]
pub fn get_tera() -> Tera {
    let mut tera = Tera::default();
    tools::get_tools_prompt(&mut tera);
    called_tools_history::get_called_tools_history_prompt(&mut tera);
    tool_decide::get_tool_decide_prompt(&mut tera);
    tera
}
