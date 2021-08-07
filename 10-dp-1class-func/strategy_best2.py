# strategy_best2.py
# Strategy pattern -- function-based implementation
# selecting best promotion from current module globals

"""
    >>> from decimal import Decimal
    >>> from strategy import Customer, LineItem, Order
    >>> joe = Customer('John Doe', 0)
    >>> ann = Customer('Ann Smith', 1100)
    >>> cart = [LineItem('banana', 4, Decimal('.5')),
    ...         LineItem('apple', 10, Decimal('1.5')),
    ...         LineItem('watermelon', 5, Decimal(5))]
    >>> Order(joe, cart, fidelity_promo)
    <Order total: 42.00 due: 42.00>
    >>> Order(ann, cart, fidelity_promo)
    <Order total: 42.00 due: 39.90>
    >>> banana_cart = [LineItem('banana', 30, Decimal('.5')),
    ...                LineItem('apple', 10, Decimal('1.5'))]
    >>> Order(joe, banana_cart, bulk_item_promo)
    <Order total: 30.00 due: 28.50>
    >>> long_cart = [LineItem(str(item_code), 1, Decimal(1))
    ...               for item_code in range(10)]
    >>> Order(joe, long_cart, large_order_promo)
    <Order total: 10.00 due: 9.30>
    >>> Order(joe, cart, large_order_promo)
    <Order total: 42.00 due: 42.00>

# tag::STRATEGY_BEST_TESTS[]

    >>> Order(joe, long_cart, best_promo)
    <Order total: 10.00 due: 9.30>
    >>> Order(joe, banana_cart, best_promo)
    <Order total: 30.00 due: 28.50>
    >>> Order(ann, cart, best_promo)
    <Order total: 42.00 due: 39.90>

# end::STRATEGY_BEST_TESTS[]
"""

# tag::STRATEGY_BEST2[]
from decimal import Decimal
from strategy import Order
from strategy import (
    fidelity_promo, bulk_item_promo, large_order_promo  # <1>
)

promos = [promo for name, promo in globals().items()  # <2>
                if name.endswith('_promo') and        # <3>
                   name != 'best_promo'               # <4>
]


def best_promo(order: Order) -> Decimal:              # <5>
    """Compute the best discount available"""
    return max(promo(order) for promo in promos)

# end::STRATEGY_BEST2[]
