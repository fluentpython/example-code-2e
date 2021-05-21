from collections.abc import Collection, Sequence

col_int: Collection[int]

seq_int: Sequence[int] = (1, 2, 3)

## Incompatible types in assignment
##   expression has type "Collection[int]"
##     variable has type "Sequence[int]"
# seq_int = col_int

col_int = seq_int

## List item 0 has incompatible type "float"
##   expected "int"
# col_int = [1.1]
