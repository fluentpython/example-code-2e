from typing import (
    List,
    Optional,
    Union,
)


class BulkItemPromo:
    def discount(self, order: Order) -> Union[float, int]: ...


class FidelityPromo:
    def discount(self, order: Order) -> Union[float, int]: ...


class LargeOrderPromo:
    def discount(self, order: Order) -> Union[float, int]: ...


class LineItem:
    def __init__(self, product: str, quantity: int, price: float) -> None: ...
    def total(self) -> float: ...


class Order:
    def __init__(
        self,
        customer: Customer,
        cart: List[LineItem],
        promotion: Optional[Union[BulkItemPromo, LargeOrderPromo, FidelityPromo]] = ...
    ) -> None: ...
    def due(self) -> float: ...
    def total(self) -> float: ...
