pub extern crate fib_rust;
use num_bigint::BigInt;
use pyo3::prelude::*;

#[pyfunction]
fn fib(n: u32) -> BigInt {
    fib_rust::fib(n)
}

#[pymodule]
fn fib_pyrs(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(fib, m)?)?;
    Ok(())
}
