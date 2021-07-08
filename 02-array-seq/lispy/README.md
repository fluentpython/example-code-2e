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


_Luciano Ramalho<br/>June 29, 2021_
