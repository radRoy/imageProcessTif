"""
daniel walther
creation: 17.08.2023 dd.mm.yyyy
purpose: getting to know the *args thing in python
goal: writing a function taking a sub-function and a dynamic number of input arguments to be passed to the sub-function
links:
    https://docs.python.org/3/tutorial/controlflow.html#tut-unpacking-arguments
"""


def sub_fun_0(s):
    return 2 * s


def sub_fun_1(a, b, c):
    return a + b + c


def super_fun(fun, *args):
    for arg in args:
        print(arg)
    print(fun(*args))
    pass


if __name__ == "__main__":
    super_fun(sub_fun_0, "echo.")
    super_fun(sub_fun_1, 1, 2, 3)
