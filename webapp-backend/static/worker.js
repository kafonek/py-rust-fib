importScripts("https://cdn.jsdelivr.net/pyodide/v0.21.3/full/pyodide.js");

// placeholder onmessage function while Python/WASM is set up.
// onmessage event handler will be overwritten by code in worker.py
// Post a Map to match behavior from worker.py response
onmessage = async (event) => {
    postMessage("Pyodide is still loading...")
}

async function init() {
    console.log("loading pyodide");
    self.pyodide = await loadPyodide();
    await pyodide.loadPackage('micropip')

    await self.pyodide.runPythonAsync(`
    # Install locally developed packages
    import micropip
    import js

    fib_python_wheel = f"{js.location.origin}/fib-python/dist/fib_python-0.1.0-py3-none-any.whl"
    await micropip.install(fib_python_wheel)

    # Below fails: ValueError: Wheel platform 'linux_x86_64' is not compatible with Pyodide's platform 'emscripten-3.1.14-wasm32'
    #
    # fib_pyrs_wheel = f"{js.location.origin}/fib-pyrs/target/wheels/fib_pyrs-0.1.0-cp37-abi3-linux_x86_64.whl"
    # await micropip.install(fib_pyrs_wheel)

    webworker_wheel = f"{js.location.origin}/webapp-webworker/dist/webworker-0.1.0-py3-none-any.whl"
    await micropip.install(webworker_wheel, keep_going=True)
    `)
    // Python code in worker.py will hook into the onmessage / postMessage methods on Python import
    self.pyodide.pyimport('webworker')

}
let initPromise = init();