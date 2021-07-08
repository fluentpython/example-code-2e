# Norvig's originals and updates

This directory contains:

* `original/`:
Norvig's [`lis.py`](https://github.com/norvig/pytudes/blob/c33cd6835a506a57d9fe73e3a8317d49babb13e8/py/lis.py),
[`lispy.py`](https://github.com/norvig/pytudes/blob/c33cd6835a506a57d9fe73e3a8317d49babb13e8/py/lispy.py), and the `lispytest.py` custom test script for testing both;
* `py3.10/`: `lis.py` with type hints, pattern matching, and minor edits—requires Python 3.10.

The `py3.10/` directory also has `lis_test.py` to run with
[pytest](https://docs.pytest.org), including the
[`lis_tests` suite](https://github.com/norvig/pytudes/blob/60168bce8cdfacf57c92a5b2979f0b2e95367753/py/lispytest.py#L5)
from `original/lispytest.py`,
and additional separate tests for each expression and special form handled by `evaluate`.


## Provenance, Copyright and License

`lis.py` is
[published](https://github.com/norvig/pytudes/blob/c33cd6835a506a57d9fe73e3a8317d49babb13e8/py/lis.py)
in the [norvig/pytudes](https://github.com/norvig/pytudes) repository on Github.
The copyright holder is Peter Norvig and the code is licensed under the
[MIT license](https://github.com/norvig/pytudes/blob/60168bce8cdfacf57c92a5b2979f0b2e95367753/LICENSE).


## Changes to Norvig's code

I made small changes to the programs in `original/`:

* In `lis.py`:
  * The `Procedure` class accepts a list of expressions as the `body`, and `__call__` evaluates those expressions in order, and returns the value of the last. This is consistent with Scheme's `lambda` syntax and provided a useful example for pattern matching.
  * In the `elif` block for `'lambda'`, I added the `*` in front of the `*body` variable in the tuple unpacking to capture the expressions as a list, before calling the `Procedure` constructor.

* In `lispy.py` I made [changes and a pull request](https://github.com/norvig/pytudes/pull/106) to make it run on Python 3.

_Luciano Ramalho<br/>June 29, 2021_
