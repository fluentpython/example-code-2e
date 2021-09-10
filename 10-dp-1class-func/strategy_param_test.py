from typing import List
import functools

import pytest  # type: ignore

from strategy_param import Customer, LineItem, Order, Promotion
from strategy_param import fidelity_promo, bulk_item_promo, LargeOrderPromo
from strategy_param import general_discount


@pytest.fixture
def customer_fidelity_0() -> Customer:
    return Customer('John Doe', 0)


@pytest.fixture
def customer_fidelity_1100() -> Customer:
    return Customer('Ann Smith', 1100)


@pytest.fixture
def cart_plain() -> List[LineItem]:
    return [
        LineItem('banana', 4, 0.5),
        LineItem('apple', 10, 1.5),
        LineItem('watermelon', 5, 5.0),
    ]


def test_fidelity_promo_with_discount(customer_fidelity_1100, cart_plain) -> None:
    order = Order(customer_fidelity_1100, cart_plain, fidelity_promo(10))
    assert order.total() == 42.0
    assert order.due() == 37.8


def test_bulk_item_promo_with_discount(customer_fidelity_0) -> None:
    cart = [LineItem('banana', 30, 0.5), LineItem('apple', 10, 1.5)]
    order = Order(customer_fidelity_0, cart, bulk_item_promo(10))
    assert order.total() == 30.0
    assert order.due() == 28.5


def test_large_order_promo_with_discount(customer_fidelity_0) -> None:
    cart = [LineItem(str(item_code), 1, 1.0) for item_code in range(10)]
    order = Order(customer_fidelity_0, cart, LargeOrderPromo(7))
    assert order.total() == 10.0
    assert order.due() == 9.3


def test_general_discount(customer_fidelity_1100, cart_plain) -> None:
    general_promo: Promotion = functools.partial(general_discount, 5)
    order = Order(customer_fidelity_1100, cart_plain, general_promo)
    assert order.total() == 42.0
    assert order.due() == 39.9
