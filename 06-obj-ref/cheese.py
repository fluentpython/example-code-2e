"""
>>> import weakref
>>> stock = weakref.WeakValueDictionary()
>>> catalog = [Cheese('Red Leicester'), Cheese('Tilsit'),
...            Cheese('Brie'), Cheese('Parmesan')]
...
>>> for cheese in catalog:
...     stock[cheese.kind] = cheese
...
>>> sorted(stock.keys())
['Brie', 'Parmesan', 'Red Leicester', 'Tilsit']
>>> del catalog
>>> sorted(stock.keys())
['Parmesan']
>>> del cheese
>>> sorted(stock.keys())
[]
"""

# tag::CHEESE_CLASS[]
class Cheese:

    def __init__(self, kind):
        self.kind = kind

    def __repr__(self):
        return f'Cheese({self.kind!r})'
# end::CHEESE_CLASS[]
