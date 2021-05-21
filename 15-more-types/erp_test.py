from typing import TYPE_CHECKING

from erp import EnterpriserRandomPopper
import randompop


def test_issubclass() -> None:
    assert issubclass(EnterpriserRandomPopper, randompop.RandomPopper)


def test_isinstance_untyped_items_argument() -> None:
    items = [1, 2, 3]
    popper = EnterpriserRandomPopper(items)  # [int] is not required
    if TYPE_CHECKING:
        reveal_type(popper)
        # Revealed type is 'erp.EnterpriserRandomPopper[builtins.int*]'
    assert isinstance(popper, randompop.RandomPopper)


def test_isinstance_untyped_items_in_var_type() -> None:
    items = [1, 2, 3]
    popper: EnterpriserRandomPopper = EnterpriserRandomPopper[int](items)
    if TYPE_CHECKING:
        reveal_type(popper)
        # Revealed type is 'erp.EnterpriserRandomPopper[Any]'
    assert isinstance(popper, randompop.RandomPopper)


def test_isinstance_item() -> None:
    items = [1, 2, 3]
    popper = EnterpriserRandomPopper[int](items)  # [int] is not required
    popped = popper.pop_random()
    if TYPE_CHECKING:
        reveal_type(popped)
        # Revealed type is 'builtins.int*'
    assert isinstance(popped, int)
