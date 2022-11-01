# py-rust-fib

A reference (learning) repo for:

 - Writing library code in vanilla Rust (`fib-rust`)
 - Writing a mixed Python-Rust library that uses the pure Rust lib (`fib-pyrs`)
 - Writing library code in vanilla Python (`fib-python`)
 - Benchmarking the performance difference calling the pure Python vs Python-Rust functions


```
py-rust-fib/benchmarks on  main [?] is 📦 v0.1.0 via 🐍 v3.9.11 took 7s 
❯ poetry run test
Generating Fib sequence of 500_000 numbers
Python: 7.522406816482544
Pyrs: 0.020959854125976562
```

# Motivation
First, I'm interested in using [y-py](https://github.com/y-crdt/ypy) and potentially contributing to that library. It is a combined Python/Rust library though, a thin wrapper around the [https://github.com/y-crdt/y-crdt](Rust implementation of the Y CRDT). This repo is minimal example of a combined Python/Rust library.

Second, I'm a big fan and user of [Pydantic](https://pydantic-docs.helpmanual.io/), and in their [V2 Plan](https://pydantic-docs.helpmanual.io/blog/pydantic-v2/) the `pydantic-core` will be written in Rust. 

Third, I'm very interested in the [Pyodide](https://pyodide.org/en/stable/) and WASM space (also see [Pyscript](https://pyscript.net/) although I have been content with Pyodide features alone). I'm intrigued by the idea that Python can call into [any other wasm function](https://www.jhanley.com/blog/pyscript-interfacing-with-wasm/) in that runtime. I want to learn more about that. Not to mention I need to stay on top of the [Docker + WASM, or Docker vs WASM?](https://www.docker.com/blog/why-containers-and-webassembly-work-well-together/) conversation.

Finally, I expect Rust will become a go-to language for enhancing Python performance in critical code paths, like C extensions have been used for in the past. I have never tried delving into `cython` or writing a C extension, so this is my first foray into lower level code.

# Notes

## Poetry and Cargo
I used `poetry` and `cargo` to create the repos: `poetry new <name>`, `cargo new --lib <name>`

To test: `poetry run pytest`, `crate test`

`pyproject.toml` and `Cargo.toml` use very similar syntax. For instance, depending on other libraries built locally (vice hosted on `pypi.org` / `crates.io`) looks like: `library-name: {path = "../lib_directory"}`

## fib-rust
`fib-rust` is the pure Rust repo. It's about as minimal as a Rust repo can get. 

## fib-pyrs
`fib-pyrs` is the combined Python/Rust repo. You can't have two compile targets for Rust libraries, so if you want to be able to use a library in Rust and in Python, you need two repos: one for the pure lib, one targeting a binding. `fib-pyrs` uses `fib-rust` as a dependency (see `Cargo.toml`) and `pyo3` for `pyfunction` / `pymodule` macros that translate Rust objects into Python objects when Python code calls into the library.

In order to build the Python wheel, we need the `maturin` Python library and configuration for the `pyo3` Rust library in `Cargo.toml`. A combined Python/Rust repo can have `pyproject.toml` and `Cargo.toml`. To build the wheel: `poetry run maturin develop`

Notice the `tests/` in `fib-pyrs` are written in Python, and executed with `poetry run pytest` even though there's no Python code in `src/`. It is possible to have the combined package (i.e. what's in the `wheel`) use [some code from Rust and some from Python](https://www.maturin.rs/project_layout.html#mixed-rustpython-project), it's just not part of this example.

Finally, the `fib_pyrs.pyi` file is not required to build the wheel or use the `fib-pyrs` library in Python. Without it though, VSCode won't acknowledge `fib_pyrs` as a valid library to import. It also let's us customize the docstring in Python.

## benchmarks
It's worth mentioning here that depending on a vanilla Python libarary (`fib-python`) and a combined Rust/Python library (`fib-pyrs`) is identical in `pyproject.toml` syntax.


## Unit vs Integration tests
One thing I learned from this repo is Rust's definition of Unit vs Integration tests. Unit tests are tests that can access private functions, and need to be written in-line with the code (as seen in `fib-rust` despite that function being public). Integration tests live in the `tests/` folder and can only test public functions. That's not a distinction I would have made just working in the Python ecosystem.