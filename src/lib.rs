mod prompts;

use prompts::Tool;
use prompts::get_tera;
use pyo3::prelude::*;
use tera::{Tera, Context};
use once_cell::sync::Lazy;
use pyo3::FromPyObject;
use serde::{Deserialize};

static TERA: Lazy<Tera> = Lazy::new(get_tera);



#[pyclass]
#[derive(Clone, Debug)]
struct Person {
    name: String,
    age: u32,
}


#[pymethods]
impl Person {
    #[new]
    fn new(name: String, age: u32) -> Self {
        Self { name, age }
    }
    fn greet(&self) -> String {
        format!("Hello, {}! You are {} years old.", self.name, self.age)
    }
    fn try_python_struct(&self, another_person: Person) -> String {
        format!("Hello, {}! You are {} years old.", self.name, self.age)
    }
}


#[derive(FromPyObject,Debug, Deserialize)]
struct Address {
    city: String,
    zip_code: Option<String>,  // Nullable field
}

#[derive(FromPyObject,Debug, Deserialize)]
struct User {
    name: String,
    age: u32,
    address: Address,
}



#[pyfunction]
pub fn hello_from_bin() -> String {
    "Hello from financial-a2a-solution!".to_string()
}

#[pyfunction]
pub fn get_tools_prompt(py_tools: Bound<'_, PyAny>) -> PyResult<String> {
    let tools: Vec<Tool> = py_tools.extract()?;
    let mut context = Context::new();

    context.insert("tools", &tools);
    Ok(TERA.render("tools", &context).unwrap())
}

#[pyfunction]
pub fn extract_user(py_user: Bound<'_, PyAny>) -> PyResult<()> {
    let user: User = py_user.extract()?;

    println!("User: {:?}", user);
    match &user.address.zip_code {
        Some(zip) => println!("Zip code: {}", zip),
        None => println!("Zip code is missing"),
    }

    Ok(())
}

/// A Python module implemented in Rust. The name of this function must match
/// the `lib.name` setting in the `Cargo.toml`, else Python will not be able to
/// import the module.
#[pymodule]
fn the_solution(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(hello_from_bin, m)?)?;
    m.add_function(wrap_pyfunction!(get_tools_prompt, m)?)?;
    m.add_function(wrap_pyfunction!(extract_user, m)?)?;
    m.add_class::<Person>()?;
    Ok(())
}
