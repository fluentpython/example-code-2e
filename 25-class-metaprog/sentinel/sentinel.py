"""

    >>> class Missing(Sentinel): pass
    >>> Missing
    <Missing>
    >>> class CustomRepr(Sentinel):
    ...     repr = '*** sentinel ***'
    ...
    >>> CustomRepr
    *** sentinel ***

"""

class SentinelMeta(type):
    def __repr__(cls):
        try:
            return cls.repr
        except AttributeError:
            return f'<{cls.__name__}>'

class Sentinel(metaclass=SentinelMeta):
    def __new__(cls):
        return cls

