import time

import fib_python
import js
from pyodide import ffi

MessageEvent = ffi.JsProxy


class API:
    def __init__(self):
        js.postMessage(ffi.to_js({"status": "ready"}))

    async def on_webworker_message(self, event: MessageEvent):
        """
        Callback function for when the webworker process receives data from the main browser thread.
        Parse event.data and delegate handling to the appropriate process_* method
        """
        # frontend will only send over a string (event.data is a string)
        js.console.log("on_webworker_message event.data: ", event.data)
        js.postMessage(ffi.to_js({"status": "processing"}))
        n = int(event.data.n)
        start = time.time()
        fib_python.fib(n)
        duration = time.time() - start

        js.postMessage(ffi.to_js({"status": "complete", "n": n, "duration": duration}))


api = API()
js.console.log("API is instantiated")
js.onmessage = api.on_webworker_message
