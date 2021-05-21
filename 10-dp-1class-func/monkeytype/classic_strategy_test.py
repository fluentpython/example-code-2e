from typing import List

import pytest  # type: ignore

from classic_strategy import Customer, LineItem, Order
from classic_strategy import FidelityPromo, BulkItemPromo, LargeOrderPromo


@pytest.fixture
def customer_fidelity_0() -> Customer:
    return Customer('John Doe', 0)


@pytest.fixture
def customer_fidelity_1100() -> Customer:
    return Customer('Ann Smith', 1100)


@pytest.fixture
def cart_plain() -> List[LineItem]:
    return [LineItem('banana', 4, .5),
            LineItem('apple', 10, 1.5),
            LineItem('watermelon', 5, 5.0)]


def test_fidelity_promo_no_discount(customer_fidelity_0, cart_plain) -> None:
    order = Order(customer_fidelity_0, cart_plain, FidelityPromo())
    assert order.total() == 42.0
    assert order.due() == 42.0


def test_fidelity_promo_with_discount(customer_fidelity_1100, cart_plain) -> None:
    order = Order(customer_fidelity_1100, cart_plain, FidelityPromo())
    assert order.total() == 42.0
    assert order.due() == 39.9


def test_bulk_item_promo_no_discount(customer_fidelity_0, cart_plain) -> None:
    order = Order(customer_fidelity_0, cart_plain, BulkItemPromo())
    assert order.total() == 42.0
    assert order.due() == 42.0


def test_bulk_item_promo_with_discount(customer_fidelity_0) -> None:
    cart = [LineItem('banana', 30, .5),
            LineItem('apple', 10, 1.5)]
    order = Order(customer_fidelity_0, cart, BulkItemPromo())
    assert order.total() == 30.0
    assert order.due() == 28.5


def test_large_order_promo_no_discount(customer_fidelity_0, cart_plain) -> None:
    order = Order(customer_fidelity_0, cart_plain, LargeOrderPromo())
    assert order.total() == 42.0
    assert order.due() == 42.0


def test_large_order_promo_with_discount(customer_fidelity_0) -> None:
    cart = [LineItem(str(item_code), 1, 1.0) for item_code in range(10)]
    order = Order(customer_fidelity_0, cart, LargeOrderPromo())
    assert order.total() == 10.0
    assert order.due() == 9.3
