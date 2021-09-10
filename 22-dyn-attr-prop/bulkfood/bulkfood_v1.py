"""
A line item for a bulk food order has description, weight and price fields.
A ``subtotal`` method gives the total price for that line item::

    >>> raisins = LineItem('Golden raisins', 10, 6.95)
    >>> raisins.weight, raisins.description, raisins.price
    (10, 'Golden raisins', 6.95)
    >>> raisins.subtotal()
    69.5

But, without validation, these public attributes can cause trouble::

# tag::LINEITEM_PROBLEM_V1[]

    >>> raisins = LineItem('Golden raisins', 10, 6.95)
    >>> raisins.subtotal()
    69.5
    >>> raisins.weight = -20  # garbage in...
    >>> raisins.subtotal()    # garbage out...
    -139.0

# end::LINEITEM_PROBLEM_V1[]

"""


# tag::LINEITEM_V1[]
class LineItem:

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price
# end::LINEITEM_V1[]
