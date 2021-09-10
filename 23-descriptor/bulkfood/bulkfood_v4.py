"""

A line item for a bulk food order has description, weight and price fields::

    >>> raisins = LineItem('Golden raisins', 10, 6.95)
    >>> raisins.weight, raisins.description, raisins.price
    (10, 'Golden raisins', 6.95)

A ``subtotal`` method gives the total price for that line item::

    >>> raisins.subtotal()
    69.5

The weight of a ``LineItem`` must be greater than 0::

    >>> raisins.weight = -20
    Traceback (most recent call last):
        ...
    ValueError: weight must be > 0

No change was made::

    >>> raisins.weight
    10

Negative or 0 price is not acceptable either::

    >>> truffle = LineItem('White truffle', 100, 0)
    Traceback (most recent call last):
        ...
    ValueError: price must be > 0

If the descriptor is accessed in the class, the descriptor object is
returned:

    >>> LineItem.weight  # doctest: +ELLIPSIS
    <bulkfood_v4.Quantity object at 0x...>
    >>> LineItem.weight.storage_name
    'weight'

"""


# tag::LINEITEM_V4[]
class Quantity:

    def __set_name__(self, owner, name):  # <1>
        self.storage_name = name          # <2>

    def __set__(self, instance, value):   # <3>
        if value > 0:
            instance.__dict__[self.storage_name] = value
        else:
            msg = f'{self.storage_name} must be > 0'
            raise ValueError(msg)

    # no __get__ needed  # <4>

class LineItem:
    weight = Quantity()  # <5>
    price = Quantity()

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price
# end::LINEITEM_V4[]
