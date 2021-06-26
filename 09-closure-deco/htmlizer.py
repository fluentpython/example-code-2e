r"""
htmlize(): generic function example

# tag::HTMLIZE_DEMO[]

>>> htmlize({1, 2, 3})  # <1>
'<pre>{1, 2, 3}</pre>'
>>> htmlize(abs)
'<pre>&lt;built-in function abs&gt;</pre>'
>>> htmlize('Heimlich & Co.\n- a game')  # <2>
'<p>Heimlich &amp; Co.<br/>\n- a game</p>'
>>> htmlize(42)  # <3>
'<pre>42 (0x2a)</pre>'
>>> print(htmlize(['alpha', 66, {3, 2, 1}]))  # <4>
<ul>
<li><p>alpha</p></li>
<li><pre>66 (0x42)</pre></li>
<li><pre>{1, 2, 3}</pre></li>
</ul>
>>> htmlize(True)  # <5>
'<pre>True</pre>'
>>> htmlize(fractions.Fraction(2, 3))  # <6>
'<pre>2/3</pre>'
>>> htmlize(2/3)   # <7>
'<pre>0.6666666666666666 (2/3)</pre>'
>>> htmlize(decimal.Decimal('0.02380952'))
'<pre>0.02380952 (1/42)</pre>'

# end::HTMLIZE_DEMO[]
"""

# tag::HTMLIZE[]

from functools import singledispatch
from collections import abc
import fractions
import decimal
import html
import numbers

@singledispatch  # <1>
def htmlize(obj: object) -> str:
    content = html.escape(repr(obj))
    return f'<pre>{content}</pre>'

@htmlize.register  # <2>
def _(text: str) -> str:  # <3>
    content = html.escape(text).replace('\n', '<br/>\n')
    return f'<p>{content}</p>'

@htmlize.register  # <4>
def _(seq: abc.Sequence) -> str:
    inner = '</li>\n<li>'.join(htmlize(item) for item in seq)
    return '<ul>\n<li>' + inner + '</li>\n</ul>'

@htmlize.register  # <5>
def _(n: numbers.Integral) -> str:
    return f'<pre>{n} (0x{n:x})</pre>'

@htmlize.register  # <6>
def _(n: bool) -> str:
    return f'<pre>{n}</pre>'

@htmlize.register(fractions.Fraction)  # <7>
def _(x) -> str:
    frac = fractions.Fraction(x)
    return f'<pre>{frac.numerator}/{frac.denominator}</pre>'

@htmlize.register(decimal.Decimal)  # <8>
@htmlize.register(float)
def _(x) -> str:
    frac = fractions.Fraction(x).limit_denominator()
    return f'<pre>{x} ({frac.numerator}/{frac.denominator})</pre>'

# end::HTMLIZE[]

