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

Negative or 0 price is not acceptable either::

    >>> truffle = LineItem('White truffle', 100, 0)
    Traceback (most recent call last):
        ...
    ValueError: price must be > 0

No change was made::

    >>> raisins.weight
    10

"""


# tag::LINEITEM_QUANTITY_V3[]
class Quantity:  # <1>

    def __init__(self, storage_name):
        self.storage_name = storage_name  # <2>

    def __set__(self, instance, value):  # <3>
        if value > 0:
            instance.__dict__[self.storage_name] = value  # <4>
        else:
            msg = f'{self.storage_name} must be > 0'
            raise ValueError(msg)

    def __get__(self, instance, owner):  # <5>
        return instance.__dict__[self.storage_name]


# end::LINEITEM_QUANTITY_V3[]

# tag::LINEITEM_V3[]
class LineItem:
    weight = Quantity('weight')  # <1>
    price = Quantity('price')  # <2>

    def __init__(self, description, weight, price):  # <3>
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price
# end::LINEITEM_V3[]
