from fib_python import __version__, fib


def test_version():
    assert __version__ == "0.1.0"


def test_fib():
    assert fib(0) == 0
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(3) == 2
    assert fib(4) == 3
    assert fib(5) == 5
    assert fib(10) == 55
    assert fib(100) == 354224848179261915075
