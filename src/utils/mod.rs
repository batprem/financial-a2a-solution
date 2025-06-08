use pyo3::prelude::*;
use pyo3::types::PyDict;
use regex::Regex;

/// Helper function to find the closing tag position (handles nested tags)
fn find_closing_tag(stream: &str, start_pos: usize, tag: &str) -> Option<usize> {
    let open_tag = format!("<{}", tag);
    let close_tag = format!("</{}>", tag);

    let mut pos = start_pos;
    let mut count = 1;

    while count > 0 {
        let next_open = stream[pos..].find(&open_tag).map(|i| i + pos);
        let next_close = stream[pos..].find(&close_tag).map(|i| i + pos);

        match (next_open, next_close) {
            (_, None) => return None,
            (Some(o), Some(c)) if o < c => {
                count += 1;
                pos = o + open_tag.len();
            }
            (_, Some(c)) => {
                count -= 1;
                pos = c + close_tag.len();
            }
        }
    }

    Some(pos)
}

/// Parse streamed XML-like data into a Python list of dicts
#[pyfunction]
pub fn parse_streamed_tags(py: Python<'_>, stream: &str) -> PyResult<Vec<PyObject>> {
    let tag_open_re = Regex::new(r"<(?P<tag>\w+)(?P<attr>[^>]*)>").unwrap();
    let attr_re = Regex::new(r#"(\w+)="(.*?)""#).unwrap();

    let mut pos = 0;
    let mut result = Vec::new();

    while let Some(cap) = tag_open_re.captures(&stream[pos..]) {
        let whole_match = cap.get(0).unwrap();
        let tag = cap.name("tag").unwrap().as_str();
        let attr_str = cap.name("attr").map_or("", |m| m.as_str()).trim();

        let attributes = PyDict::new_bound(py);
        for attr_cap in attr_re.captures_iter(attr_str) {
            attributes.set_item(attr_cap[1].to_string(), attr_cap[2].to_string())?;
        }

        let content_start = pos + whole_match.end();
        let content_end;

        let is_complete;
        if let Some(end) = find_closing_tag(stream, content_start, tag) {
            content_end = end - format!("</{}>", tag).len();
            is_complete = true;
            pos = end;
        } else {
            content_end = stream.len();
            is_complete = false;
            pos = stream.len();
        }

        let content = stream[content_start..content_end].trim().to_string();

        let py_dict = PyDict::new_bound(py);
        py_dict.set_item("tag", tag)?;
        py_dict.set_item("attributes", attributes)?;
        py_dict.set_item("content", content)?;
        py_dict.set_item("is_complete", is_complete)?;

        result.push(py_dict.into());
    }

    Ok(result)
}
