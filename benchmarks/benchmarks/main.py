import time

import fib_pyrs
import fib_python


def benchmark():
    n = 500_000
    print(f"Generating Fib number {n:_}")
    py_start = time.time()
    py_result = fib_python.fib(n)
    py_end = time.time()
    print(f"Python: {py_end - py_start:.5f} seconds")

    pyrs_start = time.time()
    pyrs_result = fib_pyrs.fib(n)
    pyrs_end = time.time()
    print(f"PyRS: {pyrs_end - pyrs_start:.5f} seconds")
    print(f"fib-python and fib-pyrs gave same answer? {py_result == pyrs_result=}")
