# strategy_param.py
# Strategy pattern -- parametrized with closure

"""
    >>> joe = Customer('John Doe', 0)
    >>> ann = Customer('Ann Smith', 1100)
    >>> cart = [LineItem('banana', 4, .5),
    ...         LineItem('apple', 10, 1.5),
    ...         LineItem('watermelon', 5, 5.0)]
    >>> Order(joe, cart, fidelity_promo(10))
    <Order total: 42.00 due: 42.00>
    >>> Order(ann, cart, fidelity_promo(10))
    <Order total: 42.00 due: 37.80>
    >>> banana_cart = [LineItem('banana', 30, .5),
    ...                LineItem('apple', 10, 1.5)]
    >>> Order(joe, banana_cart, bulk_item_promo(10))
    <Order total: 30.00 due: 28.50>
    >>> long_cart = [LineItem(str(item_code), 1, 1.0)
    ...               for item_code in range(10)]
    >>> Order(joe, long_cart, LargeOrderPromo(7))
    <Order total: 10.00 due: 9.30>
    >>> Order(joe, cart, LargeOrderPromo(7))
    <Order total: 42.00 due: 42.00>

Using ``partial`` to build a parametrized discounter on the fly::

    >>> from functools import partial
    >>> Order(joe, cart, partial(general_discount, 5))
    <Order total: 42.00 due: 39.90>

"""

import typing
from typing import Sequence, Optional, Callable


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
            discount = self.promotion(self)  # <1>
        return self.total() - discount

    def __repr__(self):
        return f'<Order total: {self.total():.2f} due: {self.due():.2f}>'


# tag::STRATEGY_PARAM[]

Promotion = Callable[[Order], float]  # <2>


def fidelity_promo(percent: float) -> Promotion:
    """discount for customers with 1000 or more fidelity points"""
    return lambda order: (
        order.total() * percent / 100 if order.customer.fidelity >= 1000 else 0
    )


def bulk_item_promo(percent: float) -> Promotion:
    """discount for each LineItem with 20 or more units"""

    def discounter(order: Order) -> float:
        discount = 0
        for item in order.cart:
            if item.quantity >= 20:
                discount += item.total() * percent / 100
        return discount

    return discounter


class LargeOrderPromo:
    """discount for orders with 10 or more distinct items"""

    def __init__(self, percent: float):
        self.percent = percent

    def __call__(self, order: Order) -> float:
        distinct_items = {item.product for item in order.cart}
        if len(distinct_items) >= 10:
            return order.total() * self.percent / 100
        return 0


def general_discount(percent: float, order: Order) -> float:
    """unrestricted discount; usage: ``partial(general_discount, 5)``"""
    return order.total() * percent / 100


# end::STRATEGY[]
