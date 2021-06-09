# tag::BEVERAGE_TYPES[]
from typing import TypeVar, Generic

class Beverage:  # <1>
    """Any beverage."""

class Juice(Beverage):
    """Any fruit juice."""

class OrangeJuice(Juice):
    """Delicious juice from Brazilian oranges."""

T = TypeVar('T')  # <2>

class BeverageDispenser(Generic[T]):  # <3>
    """A dispenser parameterized on the beverage type."""
    def __init__(self, beverage: T) -> None:
        self.beverage = beverage

    def dispense(self) -> T:
        return self.beverage

def install(dispenser: BeverageDispenser[Juice]) -> None:  # <4>
    """Install a fruit juice dispenser."""
# end::BEVERAGE_TYPES[]

################################################ exact type

# tag::INSTALL_JUICE_DISPENSER[]
juice_dispenser = BeverageDispenser(Juice())
install(juice_dispenser)
# end::INSTALL_JUICE_DISPENSER[]


################################################ variant dispenser

# tag::INSTALL_BEVERAGE_DISPENSER[]
beverage_dispenser = BeverageDispenser(Beverage())
install(beverage_dispenser)
## mypy: Argument 1 to "install" has
## incompatible type "BeverageDispenser[Beverage]"
##          expected "BeverageDispenser[Juice]"
# end::INSTALL_BEVERAGE_DISPENSER[]


################################################ variant dispenser

# tag::INSTALL_ORANGE_JUICE_DISPENSER[]
orange_juice_dispenser = BeverageDispenser(OrangeJuice())
install(orange_juice_dispenser)
## mypy: Argument 1 to "install" has
## incompatible type "BeverageDispenser[OrangeJuice]"
##          expected "BeverageDispenser[Juice]"
# end::INSTALL_ORANGE_JUICE_DISPENSER[]
