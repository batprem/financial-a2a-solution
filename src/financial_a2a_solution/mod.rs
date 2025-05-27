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
pub struct Animal {
    name: String,
    age: u32,
}


#[pyclass]
#[derive(Clone, Debug)]
pub struct Person {
    name: String,
    age: u32,
}


#[pymethods]
impl Person {
    #[new]
    pub fn new(name: String, age: u32) -> Self {
        Self { name, age }
    }
    pub fn greet(&self) -> String {
        format!("Hello, {}! You are {} years old.", self.name, self.age)
    }
    pub fn try_python_struct(&self, another_person: Animal) -> String {
        format!("Hello, {}! You are {} years old.", self.name, self.age)
    }
}