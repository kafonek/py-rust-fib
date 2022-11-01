import time
from typing import Callable

import fib_pyrs
import fib_python


def test(n: int, fn: Callable) -> float:
    start = time.time()
    fn(n)
    end = time.time()
    return end - start


def run_tests():
    n = 500_000
    print(f"Generating Fib sequence of {n:_} numbers")
    print(f"Python: {test(n, fib_python.fib)}")
    print(f"Pyrs: {test(n, fib_pyrs.fib)}")
