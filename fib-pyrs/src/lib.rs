pub extern crate fib_rust;
use pyo3::prelude::*;

#[pyfunction]
fn fib(n: u32) -> PyResult<Vec<u32>> {
    Ok(fib_rust::generate_fibonacci_sequence(n))
}

#[pymodule]
fn fib_pyrs(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(fib, m)?)?;
    Ok(())
}
