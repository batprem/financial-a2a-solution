mod prompts;
mod utils;

use once_cell::sync::Lazy;
use prompts::get_tera;
use prompts::{Tool, CalledTool};
use pyo3::prelude::*;
use tera::{Context, Tera};
use utils::parse_streamed_tags;

static TERA: Lazy<Tera> = Lazy::new(get_tera);

#[pyfunction]
pub fn get_tools_prompt(py_tools: Bound<'_, PyAny>) -> PyResult<String> {
    let tools: Vec<Tool> = py_tools.extract()?;
    let mut context = Context::new();

    context.insert("tools", &tools);
    Ok(TERA.render("tools", &context).unwrap())
}

#[pyfunction]
pub fn get_called_tools_history_prompt(py_called_tools: Bound<'_, PyAny>) -> PyResult<String> {
    let called_tools: Vec<CalledTool> = py_called_tools.extract()?;
    let mut context = Context::new();
    context.insert("called_tools", &called_tools);
    Ok(TERA.render("called_tools_history", &context).unwrap())
}

#[pyfunction]
#[pyo3(signature = (question, called_tools, tool_prompt, tone=None))]
pub fn get_tool_decide_prompt(question: &str, called_tools: &str, tool_prompt: &str, tone: Option<&str>) -> PyResult<String> {
    let mut context = Context::new();
    context.insert("question", question);
    context.insert("called_tools", called_tools);
    context.insert("tool_prompt", tool_prompt);
    if let Some(tone) = tone {
        context.insert("tone", tone);
    }
    Ok(TERA.render("tool_decide", &context).unwrap())
}

fn register_utils_module(parent_module: &Bound<'_, PyModule>) -> PyResult<()> {
    let utils_module = PyModule::new_bound(parent_module.py(), "utils")?;
    utils_module.add_function(wrap_pyfunction!(parse_streamed_tags, &utils_module)?)?;
    parent_module.add_submodule(&utils_module)?;
    Ok(())
}

fn register_prompts_module(parent_module: &Bound<'_, PyModule>) -> PyResult<()> {
    let prompts_module = PyModule::new_bound(parent_module.py(), "prompts")?;
    prompts_module.add_function(wrap_pyfunction!(get_tools_prompt, &prompts_module)?)?;
    prompts_module.add_function(wrap_pyfunction!(get_called_tools_history_prompt, &prompts_module)?)?;
    prompts_module.add_function(wrap_pyfunction!(get_tool_decide_prompt, &prompts_module)?)?;
    parent_module.add_submodule(&prompts_module)?;
    Ok(())
}

/// A Python module implemented in Rust. The name of this function must match
/// the `lib.name` setting in the `Cargo.toml`, else Python will not be able to
/// import the module.
#[pymodule]
fn the_solution(m: &Bound<'_, PyModule>) -> PyResult<()> {
    register_prompts_module(m)?;
    register_utils_module(m)?;
    Ok(())
}
