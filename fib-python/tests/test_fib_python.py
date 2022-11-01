from fib_python import __version__, fib


def test_version():
    assert __version__ == "0.1.0"


def test_fib():

    assert fib(10) == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
