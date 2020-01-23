Doctests for ``cf.py``
======================

How to run the tests
----------------------

Run the ``doctest`` module from the command line::

    $ python3 -m doctest cf_tests.rst


Tests
-----

Import functions for testing::

    >>> from cf import find, main

Test ``find`` with single result::

    >>> find("sign", "registered")  # doctest:+NORMALIZE_WHITESPACE
    U+00AE  ®   REGISTERED SIGN
    (1 found)


Test ``find`` with two results::

    >>> find("chess", "queen", last=0xFFFF)  # doctest:+NORMALIZE_WHITESPACE
    U+2655	♕	WHITE CHESS QUEEN
    U+265B	♛	BLACK CHESS QUEEN
    (2 found)

Test ``main`` with no words::

    >>> main([])
    Please provide words to find.
