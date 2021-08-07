# strategy_best.py
# Strategy pattern -- function-based implementation
# selecting best promotion from static list of functions

"""
    >>> from strategy import Customer, LineItem
    >>> joe = Customer('John Doe', 0)
    >>> ann = Customer('Ann Smith', 1100)
    >>> cart = [LineItem('banana', 4, Decimal('.5')),
    ...         LineItem('apple', 10, Decimal('1.5')),
    ...         LineItem('watermelon', 5, Decimal(5))]
    >>> banana_cart = [LineItem('banana', 30, Decimal('.5')),
    ...                LineItem('apple', 10, Decimal('1.5'))]
    >>> long_cart = [LineItem(str(item_code), 1, Decimal(1))
    ...               for item_code in range(10)]

# tag::STRATEGY_BEST_TESTS[]

    >>> Order(joe, long_cart, best_promo)  # <1>
    <Order total: 10.00 due: 9.30>
    >>> Order(joe, banana_cart, best_promo)  # <2>
    <Order total: 30.00 due: 28.50>
    >>> Order(ann, cart, best_promo)  # <3>
    <Order total: 42.00 due: 39.90>

# end::STRATEGY_BEST_TESTS[]
"""

from decimal import Decimal

from strategy import Order
from strategy import fidelity_promo, bulk_item_promo, large_order_promo

# tag::STRATEGY_BEST[]

promos = [fidelity_promo, bulk_item_promo, large_order_promo]  # <1>


def best_promo(order: Order) -> Decimal:  # <2>
    """Compute the best discount available"""
    return max(promo(order) for promo in promos)  # <3>


# end::STRATEGY_BEST[]
