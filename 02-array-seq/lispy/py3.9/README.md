# Changes from the original

While adapting Peter Norvig's [lis.py](https://github.com/norvig/pytudes/blob/705c0a335c1811a203e79587d7d41865cf7f41c7/py/lis.py) for
use in _Fluent Python, Second Edition_, I made a few changes for didactic reasons.

_Luciano Ramalho_

## Major changes

* Make the `lambda` form accept more than one expression as the body. This is consistent with [_Scheme_ syntax](https://web.mit.edu/scheme_v9.2/doc/mit-scheme-ref/Lambda-Expressions.html), and provides a useful example for the book. To implement this:
    * In `Procedure.__call__`: evaluate `self.body` as a list of expressions, instead of a single expression. Return the value of the last expression.
    * In `evaluate()`: when processing `lambda`, unpack expression into `(_, parms, *body)`, to accept a list of expressions as the body.
* Remove the `global_env` global `dict`. It is only used as a default value for the `env` parameter in `evaluate()`, but it is unsafe to use mutable data structures as parameter default values. To implement this:
    * In `repl()`: create local variable `global_env` and pass it as the `env` paramater of `evaluate()`.
    * In `evaluate()`, remove `global_env` default value for `env`.
* Rewrite the custom test script
[lispytest.py](https://github.com/norvig/pytudes/blob/705c0a335c1811a203e79587d7d41865cf7f41c7/py/lispytest.py) as 
[lis_test.py](https://github.com/fluentpython/example-code-2e/blob/master/02-array-seq/lispy/py3.9/lis_test.py):
a standard [pytest](https://docs.pytest.org) test suite including new test cases, preserving all Norvig's test cases for
[lis.py](https://github.com/norvig/pytudes/blob/705c0a335c1811a203e79587d7d41865cf7f41c7/py/lis.py)
but removing the test cases for the features implemented only in
[lispy.py](https://github.com/norvig/pytudes/blob/705c0a335c1811a203e79587d7d41865cf7f41c7/py/lispy.py).


## Minor changes

Cosmetic changes to make the code look more familiar to
Python programmers, the audience of _Fluent Python_.

* Rename `eval()` to `evaluate()`, to avoid confusion with Python's `eval` built-in function.
* Refer to the list class as `list` instead of aliasing as `List`, to avoid confusion with `typing.List` which is often imported as `List`.
* Import `collections.ChainMap` as `ChainMap` instead of `Environment`.

