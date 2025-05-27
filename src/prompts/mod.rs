mod tools;
use tera::Tera;

pub use tools::Tool;

pub fn get_tera() -> Tera {
    let mut tera = Tera::default();
    tools::get_tools_prompt(&mut tera);
    tera
}