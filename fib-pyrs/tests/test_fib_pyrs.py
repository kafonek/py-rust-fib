import fib_pyrs


def test_fib():
    # test fib 1-5, fib 10, fib 100
    assert fib_pyrs.fib(1) == 1
    assert fib_pyrs.fib(2) == 1
    assert fib_pyrs.fib(3) == 2
    assert fib_pyrs.fib(4) == 3
    assert fib_pyrs.fib(5) == 5
    assert fib_pyrs.fib(10) == 55
    assert fib_pyrs.fib(100) == 354224848179261915075
