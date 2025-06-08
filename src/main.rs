mod prompts;

use once_cell::sync::Lazy;
use prompts::get_tera;
use prompts::Tool;
use pyo3::prelude::*;
use pyo3::FromPyObject;
use serde::{Deserialize, Serialize};
use tera::{Context, Tera};

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
    fn new(name: String, age: u32) -> Self {
        Self { name, age }
    }
    fn greet(&self) -> String {
        format!("Hello, {}! You are {} years old.", self.name, self.age)
    }
    fn try_python_struct(&self, another_person: Animal) -> String {
        format!("Hello, {}! You are {} years old.", self.name, self.age)
    }
}

#[derive(Serialize)]
struct Item {
    name: String,
    price: f64,
}

fn main() {
    let person = Person::new("David".to_string(), 13);
    let animal = Animal {
        name: "Doggo".to_string(),
        age: 10,
    };
    let result = person.try_python_struct(animal);
    println!("{}", result);
}
