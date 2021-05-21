from cafeteria import (
    Cafeteria,
    BeverageDispenser,
    JuiceDispenser,
    Juice,
    OrangeJuice,
    Coak,
)

orange = OrangeJuice()

orange_dispenser: JuiceDispenser[OrangeJuice] = JuiceDispenser(orange)

juice: Juice = orange_dispenser.dispense()

soda = Coak()

## Value of type variable "JuiceT" of "JuiceDispenser" cannot be "Coak"
# soda_dispenser = JuiceDispenser(soda)

soda_dispenser = BeverageDispenser(soda)

arnold_hall = Cafeteria(soda_dispenser)
