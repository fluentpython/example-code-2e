# The Python Data Model

Sample code for Chapter 1 of _Fluent Python 2e_ by Luciano Ramalho (O'Reilly, 2020)

## Running the tests

### Doctests

Use Python's standard ``doctest`` module to check stand-alone doctest file:

    $ python3 -m doctest frenchdeck.doctest -v

And to check doctests embedded in a module:

    $ python3 -m doctest vector2d.py -v

### Jupyter Notebook

Install ``pytest`` and the ``nbval`` plugin:

    $ pip install pytest nbval

Run:

    $ pytest --nbval
