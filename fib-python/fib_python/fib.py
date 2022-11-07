def fib(n: int) -> int:
    """Calculate the nth value of Fib sequence without recursion"""
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b
