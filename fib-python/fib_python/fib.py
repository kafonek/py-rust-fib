from typing import List


def fib(n: int) -> List[int]:
    """Return a list of the first n Fibonacci numbers, starting from zero."""
    result = []
    a, b = 0, 1
    while len(result) < n:
        result.append(a)
        a, b = b, a + b
    return result
