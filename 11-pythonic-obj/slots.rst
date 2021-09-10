# tag::PIXEL[]
>>> class Pixel:
...     __slots__ = ('x', 'y')  # <1>
...
>>> p = Pixel()  # <2>
>>> p.__dict__  # <3>
Traceback (most recent call last):
  ...
AttributeError: 'Pixel' object has no attribute '__dict__'
>>> p.x = 10  # <4>
>>> p.y = 20
>>> p.color = 'red'  # <5>
Traceback (most recent call last):
  ...
AttributeError: 'Pixel' object has no attribute 'color'

# end::PIXEL[]

# tag::OPEN_PIXEL[]
>>> class OpenPixel(Pixel):  # <1>
...     pass
...
>>> op = OpenPixel()
>>> op.__dict__  # <2>
{}
>>> op.x = 8  # <3>
>>> op.__dict__  # <4>
{}
>>> op.x  # <5>
8
>>> op.color = 'green'  # <6>
>>> op.__dict__  # <7>
{'color': 'green'}

# end::OPEN_PIXEL[]

# tag::COLOR_PIXEL[]
>>> class ColorPixel(Pixel):
...    __slots__ = ('color',)  # <1>
>>> cp = ColorPixel()
>>> cp.__dict__  # <2>
Traceback (most recent call last):
  ...
AttributeError: 'ColorPixel' object has no attribute '__dict__'
>>> cp.x = 2
>>> cp.color = 'blue'  # <3>
>>> cp.flavor = 'banana'
Traceback (most recent call last):
  ...
AttributeError: 'ColorPixel' object has no attribute 'flavor'

# end::COLOR_PIXEL[]
