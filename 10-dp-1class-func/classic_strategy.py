# classic_strategy.py
# Strategy pattern -- classic implementation

"""
# tag::CLASSIC_STRATEGY_TESTS[]

    >>> joe = Customer('John Doe', 0)  # <1>
    >>> ann = Customer('Ann Smith', 1100)
    >>> cart = [LineItem('banana', 4, .5),  # <2>
    ...         LineItem('apple', 10, 1.5),
    ...         LineItem('watermellon', 5, 5.0)]
    >>> Order(joe, cart, FidelityPromo())  # <3>
    <Order total: 42.00 due: 42.00>
    >>> Order(ann, cart, FidelityPromo())  # <4>
    <Order total: 42.00 due: 39.90>
    >>> banana_cart = [LineItem('banana', 30, .5),  # <5>
    ...                LineItem('apple', 10, 1.5)]
    >>> Order(joe, banana_cart, BulkItemPromo())  # <6>
    <Order total: 30.00 due: 28.50>
    >>> big_cart = [LineItem(str(item_code), 1, 1.0) # <7>
    ...               for item_code in range(10)]
    >>> Order(joe, big_cart, LargeOrderPromo())  # <8>
    <Order total: 10.00 due: 9.30>
    >>> Order(joe, cart, LargeOrderPromo())
    <Order total: 42.00 due: 42.00>

# end::CLASSIC_STRATEGY_TESTS[]
"""
# tag::CLASSIC_STRATEGY[]

from abc import ABC, abstractmethod
import typing
from typing import Sequence, Optional


class Customer(typing.NamedTuple):
    name: str
    fidelity: int


class LineItem:
    def __init__(self, product: str, quantity: int, price: float):
        self.product = product
        self.quantity = quantity
        self.price = price

    def total(self):
        return self.price * self.quantity


class Order:  # the Context
    def __init__(
        self,
        customer: Customer,
        cart: Sequence[LineItem],
        promotion: Optional['Promotion'] = None,
    ):
        self.customer = customer
        self.cart = list(cart)
        self.promotion = promotion

    def total(self) -> float:
        if not hasattr(self, '__total'):
            self.__total = sum(item.total() for item in self.cart)
        return self.__total

    def due(self) -> float:
        if self.promotion is None:
            discount = 0.0
        else:
            discount = self.promotion.discount(self)
        return self.total() - discount

    def __repr__(self):
        fmt = '<Order total: {:.2f} due: {:.2f}>'
        return fmt.format(self.total(), self.due())


class Promotion(ABC):  # the Strategy: an abstract base class
    @abstractmethod
    def discount(self, order: Order) -> float:
        """Return discount as a positive dollar amount"""


class FidelityPromo(Promotion):  # first Concrete Strategy
    """5% discount for customers with 1000 or more fidelity points"""

    def discount(self, order: Order) -> float:
        return order.total() * 0.05 if order.customer.fidelity >= 1000 else 0


class BulkItemPromo(Promotion):  # second Concrete Strategy
    """10% discount for each LineItem with 20 or more units"""

    def discount(self, order: Order) -> float:
        discount = 0
        for item in order.cart:
            if item.quantity >= 20:
                discount += item.total() * 0.1
        return discount


class LargeOrderPromo(Promotion):  # third Concrete Strategy
    """7% discount for orders with 10 or more distinct items"""

    def discount(self, order: Order) -> float:
        distinct_items = {item.product for item in order.cart}
        if len(distinct_items) >= 10:
            return order.total() * 0.07
        return 0


# end::CLASSIC_STRATEGY[]
