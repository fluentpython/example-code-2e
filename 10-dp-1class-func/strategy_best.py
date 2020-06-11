# strategy_best.py
# Strategy pattern -- function-based implementation
# selecting best promotion from static list of functions

"""
    >>> joe = Customer('John Doe', 0)
    >>> ann = Customer('Ann Smith', 1100)
    >>> cart = [LineItem('banana', 4, .5),
    ...         LineItem('apple', 10, 1.5),
    ...         LineItem('watermellon', 5, 5.0)]
    >>> banana_cart = [LineItem('banana', 30, .5),
    ...                LineItem('apple', 10, 1.5)]
    >>> big_cart = [LineItem(str(item_code), 1, 1.0)
    ...               for item_code in range(10)]

# tag::STRATEGY_BEST_TESTS[]

    >>> Order(joe, big_cart, best_promo)  # <1>
    <Order total: 10.00 due: 9.30>
    >>> Order(joe, banana_cart, best_promo)  # <2>
    <Order total: 30.00 due: 28.50>
    >>> Order(ann, cart, best_promo)  # <3>
    <Order total: 42.00 due: 39.90>

# end::STRATEGY_BEST_TESTS[]
"""

from strategy import Customer, LineItem, Order
from strategy import fidelity_promo, bulk_item_promo, large_order_promo

# tag::STRATEGY_BEST[]

promos = [fidelity_promo, bulk_item_promo, large_order_promo]  # <1>


def best_promo(order) -> float:  # <2>
    """Select best discount available
    """
    return max(promo(order) for promo in promos)  # <3>


# end::STRATEGY_BEST[]
