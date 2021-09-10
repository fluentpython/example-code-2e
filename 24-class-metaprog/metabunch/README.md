# Examples from Python in a Nutshell, 3rd edition

The metaclass `MetaBunch` example in `original/bunch.py` is an exact copy of the
last example in the _How a Metaclass Creates a Class_ section of 
_Chapter 4: Object Oriented Python_ from  
[_Python in a Nutshell, 3rd edition_](https://learning.oreilly.com/library/view/python-in-a/9781491913833)
by Alex Martelli, Anna Ravenscroft, and Steve Holden.

The version in `pre3.6/bunch.py` is slightly simplified by taking advantage
of Python 3 `super()` and removing comments and docstrings,
to make it easier to compare to the `from3.6` version.

The version in `from3.6/bunch.py` is further simplified by taking advantage
of the order-preserving `dict` that appeared in Python 3.6,
as well as other simplifications,
such as leveraging closures in `__init__` and `__repr__` 
to avoid adding a `__defaults__` mapping to the class.

The external behavior of all three versions is the same, and
the test files `bunch_test.py` are identical in the three directories.
