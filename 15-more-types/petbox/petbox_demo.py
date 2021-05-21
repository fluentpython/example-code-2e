"""
Example adapted from `Atomic Kotlin` by Bruce Eckel & Svetlana Isakova,
chapter `Creating Generics`, section `Variance`.
"""

from typing import TYPE_CHECKING

from petbox import *


cat_box: Box[Cat] = Box()

si = Siamese()

cat_box.put(si)

animal = cat_box.get()

# if TYPE_CHECKING:
#    reveal_type(animal)  # Revealed: petbox.Cat*


################### Covariance

out_box: OutBox[Cat] = OutBox(Cat())

out_box_si: OutBox[Siamese] = OutBox(Siamese())

out_box = out_box_si

## Incompatible types in assignment
##   expression has type "OutBox[Cat]"
##     variable has type "OutBox[Siamese]"
# out_box_si = out_box

################### Contravariance

in_box: InBox[Cat] = InBox()

in_box_si: InBox[Siamese] = InBox()

## Incompatible types in assignment
##   expression has type "InBox[Siamese]"
##     variable has type "InBox[Cat]"
# in_box = in_box_si

in_box_si = in_box
