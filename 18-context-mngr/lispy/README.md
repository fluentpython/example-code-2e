# lis.py

This directory contains 4 versions of
[Peter Norvig's `lis.py` interpreter](https://norvig.com/lispy.html)
for a subset of [Scheme](https://en.wikipedia.org/wiki/Scheme_(programming_language)).

* `original/`: Norvig's `lis.py` unchanged, `lispy.py` with
[minor changes](https://github.com/norvig/pytudes/pull/106) to run on Python 3,
and the `lispytest.py` custom test script;
* `py3.9/`: `lis.py` with type hints and a few minor edits—requires Python 3.9;
* `py3.10/`: `lis.py` with type hints, pattern matching, and minor edits—requires Python 3.10.

The `py3.9/` and `py3.10/` directories also have identical `lis_test.py` to run with
[pytest](https://docs.pytest.org).
These files include all the
[`lis_tests` suite](https://github.com/norvig/pytudes/blob/60168bce8cdfacf57c92a5b2979f0b2e95367753/py/lispytest.py#L5)
from `original/lispytest.py`,
and additional separate tests for each expression and special form handled by `evaluate`.

## Provenance, Copyright and License

`lis.py` is published in the [norvig/pytudes](https://github.com/norvig/pytudes) repository on Github.
The copyright holder is Peter Norvig and the code is licensed under the
[MIT license](https://github.com/norvig/pytudes/blob/60168bce8cdfacf57c92a5b2979f0b2e95367753/LICENSE).

I wrote the changes and additions described above.

— Luciano Ramalho ([@ramalho](https://github.com/ramalho/)), 2021-06-09.
