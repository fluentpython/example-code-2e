"""
Semantics of ``__missing__`` across mappings.

✅ = indicates ``__missing__`` was called

Subclass of ``dict``::

    >>> d = DictSub(A = 'letter A')
    >>> d['a']  # ✅
    'letter A'
    >>> d.get('a', '')
    ''
    >>> 'a' in d
    False

Subclass of ``UserDict``::

    >>> ud = UserDictSub(A = 'letter A')
    >>> ud['a']  # ✅
    'letter A'
    >>> ud.get('a', '')  # ✅
    'letter A'
    >>> 'a' in ud
    False


Simple subclass of ``abc.Mapping``::

    >>> sms = SimpleMappingSub(A = 'letter A')
    >>> sms['a']
    Traceback (most recent call last):
      ...
    KeyError: 'a'
    >>> sms.get('a', '')
    ''
    >>> 'a' in sms
    False


Subclass of ``abc.Mapping`` with support for ``__missing__``::

    >>> mms = MappingMissingSub(A = 'letter A')
    >>> mms['a']  # ✅
    'letter A'
    >>> mms.get('a', '')  # ✅
    'letter A'
    >>> 'a' in mms  # ✅
    True

Subclass of ``abc.Mapping`` with support for ``__missing__``::

    >>> dms = DictLikeMappingSub(A = 'letter A')
    >>> dms['a']  # ✅
    'letter A'
    >>> dms.get('a', '')
    ''
    >>> 'a' in dms
    False


"""

from collections import UserDict
from collections import abc


def _upper(x):
    try:
        return x.upper()
    except AttributeError:
        return x


class DictSub(dict):
    def __missing__(self, key):
        return self[_upper(key)]


class UserDictSub(UserDict):
    def __missing__(self, key):
        return self[_upper(key)]


class SimpleMappingSub(abc.Mapping):
    def __init__(self, *args, **kwargs):
        self._data = dict(*args, **kwargs)

    # next three methods: abstract in ABC
    def __getitem__(self, key):
        return self._data[key]

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data)

    # never called by instances of this class
    def __missing__(self, key):
        return self[_upper(key)]


class MappingMissingSub(SimpleMappingSub):
    def __getitem__(self, key):
        try:
            return self._data[key]
        except KeyError:
            return self[_upper(key)]


class DictLikeMappingSub(SimpleMappingSub):
    def __getitem__(self, key):
        try:
            return self._data[key]
        except KeyError:
            return self[_upper(key)]

    def get(self, key, default=None):
        return self._data.get(key, default)

    def __contains__(self, key):
        return key in self._data
