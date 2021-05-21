# Legacy Class Descriptor and Metaclass Examples

Examples from _Fluent Python, First Edition_—Chapter 21, _Class Metaprogramming_,
that are mentioned in _Fluent Python, Second Edition_—Chapter 25, _Class Metaprogramming_.

These examples were developed with Python 3.4.
They run correctly in Python 3.9, but now it is easier to fullfill the same requirements
without resorting to class decorators or metaclasses.

I have preserved them here as examples of class metaprogramming techniques
that you may find in legacy code, and that can be refactored to simpler code
using a base class with `__init_subclass__` and decorators implementing `__set_name__`.

## Suggested Exercise

If you'd like to practice the concepts presented in chapters 24 and 25 of
_Fluent Python, Second Edition_,
you may to refactor the most advanced example, `model_v8.py` with these changes:

1. Simplify the `AutoStorage` descriptor by implementing `__set_name__`.
This will allow you to simplify the `EntityMeta` metaclass as well.

2. Rewrite the `Entity` class to use `__init_subclass__` instead of the `EntityMeta` metaclass—which you can then delete.

Nothing should change in the `bulkfood_v8.py` code, and its doctests should still pass.

To run the doctests while refactoring, it's often convenient to pass the `-f` option,
to exit the test runner on the first failing test.

```
$ python3 -m doctest -f bulkfood_v8.py
```

Enjoy!
