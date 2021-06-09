from typing import TypeVar, Generic


class Beverage:
    """Any beverage."""


class Juice(Beverage):
    """Any fruit juice."""


class OrangeJuice(Juice):
    """Delicious juice from Brazilian oranges."""


# tag::BEVERAGE_TYPES[]
T_co = TypeVar('T_co', covariant=True)  # <1>


class BeverageDispenser(Generic[T_co]):  # <2>
    def __init__(self, beverage: T_co) -> None:
        self.beverage = beverage

    def dispense(self) -> T_co:
        return self.beverage

def install(dispenser: BeverageDispenser[Juice]) -> None:  # <3>
    """Install a fruit juice dispenser."""
# end::BEVERAGE_TYPES[]

################################################ covariant dispenser

# tag::INSTALL_JUICE_DISPENSERS[]
juice_dispenser = BeverageDispenser(Juice())
install(juice_dispenser)

orange_juice_dispenser = BeverageDispenser(OrangeJuice())
install(orange_juice_dispenser)
# end::INSTALL_JUICE_DISPENSERS[]

################################################ more general dispenser

# tag::INSTALL_BEVERAGE_DISPENSER[]
beverage_dispenser = BeverageDispenser(Beverage())
install(beverage_dispenser)
## mypy: Argument 1 to "install" has
## incompatible type "BeverageDispenser[Beverage]"
##          expected "BeverageDispenser[Juice]"
# end::INSTALL_BEVERAGE_DISPENSER[]
