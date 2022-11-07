# py-rust-fib

A reference (learning) repo for:

 - Writing library code in vanilla Rust (`fib-rust`)
 - Writing a mixed Python-Rust library that wraps the pure Rust lib (`fib-pyrs`)
   - Building `manylinux` wheels for use on host machine
   - Building `emscripten` wheels for use in Pyodide
 - Writing library code in vanilla Python (`fib-python`)
 - Benchmarking the performance difference calling the pure Python vs Python-Rust bindings
 - Writing a webapp (FastAPI) that serves up a Pyodide-based webworker which can import `fib-pyrs` and `fib-python`
 

```
❯ cd benchmarks

# When using an unoptimized build (`maturin build` in `fib-pyrs`)
❯ poetry run benchmark
Generating Fib number 500_000
Python: 2.17376 seconds
PyRS: 27.04524 seconds
fib-python and fib-pyrs gave same answer? py_result == pyrs_result=True

# When using an optimized build (`maturin build --release` in `fib-pyrs`)
❯ poetry run benchmark
Generating Fib number 500_000
Python: 2.17259 seconds
PyRS: 0.93138 seconds
fib-python and fib-pyrs gave same answer? py_result == pyrs_result=True
```

# Motivation
First, I'm interested in using [y-py](https://github.com/y-crdt/ypy) and potentially contributing to that library. It is a combined Python/Rust library though, a thin wrapper around the [Rust implementation of the Y CRDT](https://github.com/y-crdt/y-crdt). This repo is minimal example of a combined Python/Rust library.

Second, I'm a big fan and user of [Pydantic](https://pydantic-docs.helpmanual.io/), and in their [V2 Plan](https://pydantic-docs.helpmanual.io/blog/pydantic-v2/) the `pydantic-core` will be written in Rust. 

Third, I'm very interested in the [Pyodide](https://pyodide.org/en/stable/) and WASM space (also see [Pyscript](https://pyscript.net/) although I have been content with Pyodide features alone). I'm intrigued by the idea that Python can call into [any other wasm function](https://www.jhanley.com/blog/pyscript-interfacing-with-wasm/) in that runtime. I want to learn more about that. Not to mention I need to stay on top of the [Docker + WASM, or Docker vs WASM?](https://www.docker.com/blog/why-containers-and-webassembly-work-well-together/) conversation.

Finally, I expect Rust will become a go-to language for enhancing Python performance in critical code paths, like C extensions have been used for in the past. I have never tried delving into `cython` or writing a C extension, so this is my first foray into lower level code.

# Notes

## Poetry and Cargo
I used `poetry` and `cargo` to create the repos: `poetry new <name>`, `cargo new --lib <name>`

To test: `poetry run pytest`, `crate test`

`pyproject.toml` and `Cargo.toml` use very similar syntax. For instance, depending on other libraries built locally (vice hosted on `pypi.org` / `crates.io`) looks like: `library-name: {path = "../lib_directory"}`

## fib-rust
`fib-rust` is the pure Rust library. In my first attempt at implementing a fib generator, I foolishly used `u32` which meant it would panic going past ~46th number. It's since been rewritten to use the `num_bigint` crate and deal with larger numbers. Tests are written in-line (`src/lib.rs`) and can be run with `cargo test`

## fib-pyrs
`fib-pyrs` is the combined Python/Rust repo that wraps `fib-rust`. It uses [pyo3](https://pyo3.rs/v0.17.3/) to make Rust functions and objects available as Python callables -- `pyo3` is listed as a dependency in `Cargo.toml`. It uses [maturin](https://www.maturin.rs/) to build Python wheels -- `maturin` is a Python dependency so it is in `pyproject.toml` and can be called with `poetry install && poetry run maturin develop`. `maturin develop` creates a `.so` file (such as `fib_pyrs.cpython-311-x64_64-linux-gnu.so` on my host machine) inside the poetry-managed virtualenv / `fib-pyrs` site-packages library.

To build a wheel, use `poetry run maturin build`. That will create a new `.whl` file in `target/wheels`. In testing, the unoptimized build was slightly slower than the pure-Python implementation in `fib-python`, but an optimized build (`maturin build --release`) was faster. See sections below for details on building an `emscripten` (wasm runtime) wheel.

Tests are written in Python, in the `tests/` folder. They can be run with `poetry run pytest` after `maturin develop`. If they have an error `No module named 'fib_pyrs'`, double check that you've run `maturin develop` (I frequently forget to after recreating venv).

## benchmarks
To run the benchmarks use `poetry install && poetry run benchmark`. There is a CLI section defined in `pyproject.toml` that just calls into `benchmarks/main.py::benchmark()`. I had some trouble getting the `fib-pyrs` installs to work right with the local `path`, but specifying the exact wheel location did the trick consistently.

## Unit vs Integration tests
One thing I learned from this repo is Rust's definition of Unit vs Integration tests. Unit tests are tests that can access private functions, and need to be written in-line with the code (as seen in `fib-rust` despite that function being public). Integration tests live in the `tests/` folder and can only test public functions. That's not a distinction I would have made just working in the Python ecosystem.

# WASM

As I said before, I am interested in building wheels for the combined Python/Rust that can be installed and imported in Pyodide (WASM) scripts. Trying to `micropip.install` the `manylinux` wheel that `maturin build` creates will raise an error: `ValueError: Wheel platform 'linux_x86_64' is not compatible with Pyodide's platform 'emscripten-3.1.14-wasm32'`.

## Build fib-python
Pure Python wheels can be installed in Pyodide as is.

- `cd fib-python`
- `poetry build`
- You should see a file created `fib-python/dist/fib_python-0.1.0-py3-none-any.whl`

## Build fib-pyrs wasm target
Our Python/Rust repo needs to build a wheel for `emscripten`.

1. [Install emsdk](https://emscripten.org/docs/getting_started/downloads.html#installation-instructions-using-the-emsdk-recommended):
  - `git clone https://github.com/emscripten-core/emsdk.git`
  - In the `emsdk` directory: `./emsdk install 3.1.14` to match the Emscripten build used in Pyodide 0.21.3 ([relevant changelog entry](https://pyodide.org/en/stable/project/changelog.html?highlight=3.1.14#build-system)). Using `latest` will end up with an emscripten version mismatch when installing in Pyodide.
  - `source ./emsdk_env.sh`
2. In the `fib-pyrs` directory: `poetry run maturin build --target wasm32-unknown-emscripten -i python3.10` (optionally, `--release` to optimize the build too)

If you build the normal manylinux bindings (`poetry run maturin build`) and the wasm bindings, then there should be two entries in `fib-pyrs/target/wheels`.

## Run webapp

1. `cd webapp-worker && poetry build`
2. `cd webapp-backend && poetry install && poetry run uvicorn app.main:app --reload`

This will start a server at `http://localhost:8000`. The FastAPI app serves the entire `py-rust-fib` repo as a static directory, so any files (`.whl`'s specifically) are accessible. Navigating to the site will redirect to `/webapp-backend/static/index.html` which starts a webworker (`/webapp-backend/static/worker.js`) that downloads and installs the `fib-python` library (`/fib-python/dist/fib_python-0.1.0-py3-none-any.whl`) and `fib-pyrs` library (`/fib-pyrs/target/wheels/fib_pyrs-0.1.0-cp311-cp311-manylinux_2_28_x86_64.whl`) with micropip. Then it does the same for the `webapp-webworker` application (`/webapp-webworker/dist/webworker-0.1.0-py3-none-any.whl`). *Note: your browser may cache these, use incognito mode if you're hacking on this repo*

When `worker.js` runs the line `self.pyodide.pyimport('webworker')`, `webapp-webworker/src/webworker/__init__.py` sets an `.onmessage` handler for the webworker and will handle any messages that the main document sends over. When you click "submit", a message is sent from the main document thread into the webworker, handled by Python/Pyodide code, and a response sent back to the main thread to render the status / duration.

```
# Uvicorn logs
INFO:     127.0.0.1:51792 - "GET /webapp-backend/static/index.html HTTP/1.1" 200 OK
INFO:     127.0.0.1:51792 - "GET /webapp-backend/static/index.css HTTP/1.1" 200 OK
INFO:     127.0.0.1:51792 - "GET /webapp-backend/static/worker.js HTTP/1.1" 200 OK
INFO:     127.0.0.1:51792 - "GET /fib-python/dist/fib_python-0.1.0-py3-none-any.whl HTTP/1.1" 200 OK
INFO:     127.0.0.1:51792 - "GET /fib-pyrs/target/wheels/fib_pyrs-0.1.0-cp310-cp310-emscripten_3_1_14_wasm32.whl HTTP/1.1" 200 OK
INFO:     127.0.0.1:51792 - "GET /webapp-webworker/dist/webworker-0.1.0-py3-none-any.whl HTTP/1.1" 200 OK
```

```
# Browser output when submitting n=500000 (500,000)
{"status":"complete","n":500000,"fib_py_duration":7.299999952316284,"fib_pyrs_duration":4.802000045776367}
```



