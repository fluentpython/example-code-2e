Sample code for Chapter 10 - "Design patterns with first class functions"

From the book "Fluent Python" by Luciano Ramalho (O'Reilly, 2015)
http://shop.oreilly.com/product/0636920032519.do

Notes
=====

No issues on file with zero type hints
--------------------------------------

Running Mypy on ``classic_strategy.py`` from the first edition, with no
type hints::

    $ mypy classic_strategy.py 
    Success: no issues found in 1 source file


Type inference at play
----------------------

When the ``Order.due`` method made first assignment to discount as ``discount = 0``,
Mypy complained::

    mypy classic_strategy.py 
    classic_strategy.py:68: error: Incompatible types in assignment (expression has type "float", variable has type "int")
    Found 1 error in 1 file (checked 1 source file)

To fix it, I made the first assigment as ``discount = 0``.
I never explicitly declared a type for ``discount``.


Mypy ignores functions with no annotations
------------------------------------------

Mypy did not raise any issues with this test case::


    def test_bulk_item_promo_with_discount(customer_fidelity_0):
        cart = [LineItem('banana', 30, .5),
                LineItem('apple', 10, 1.5)]
        order = Order(customer_fidelity_0, 10, BulkItemPromo())
        assert order.total() == 30.0
        assert order.due() == 28.5


The second argument to ``Order`` is declared as ``Sequence[LineItem]``.
Mypy only checks the body of a function the signature as at least one annotation,
like this::

    def test_bulk_item_promo_with_discount(customer_fidelity_0) -> None:
        cart = [LineItem('banana', 30, .5),
                LineItem('apple', 10, 1.5)]
        order = Order(customer_fidelity_0, 10, BulkItemPromo())
        assert order.total() == 30.0
        assert order.due() == 28.5


Now Mypy complains that "Argument 2 of Order has incompatible type".

However, even with the annotation in the test function signature,
Mypy did not find any problem when I mistyped the name of the ``cart`` argument.
Here, ``cart_plain`` should be ``cart``::


    def test_bulk_item_promo_with_discount(customer_fidelity_0) -> None:
        cart = [LineItem('banana', 30, .5),
                LineItem('apple', 10, 1.5)]
        order = Order(customer_fidelity_0, cart_plain, BulkItemPromo())
        assert order.total() == 30.0
        assert order.due() == 28.5


Hypotesis: ``cart_plain`` is a function decorated with ``@pytest.fixture``,
and at the top of the test file I told Mypy to ignore the Pytest import::

    import pytest  # type: ignore
