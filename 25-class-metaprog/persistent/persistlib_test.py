import pytest


from persistlib import Persistent


def test_field_descriptor_validation_type_error():
    class Cat(Persistent):
        name: str
        weight: float

    with pytest.raises(TypeError) as e:
        felix = Cat(name='Felix', weight=None)

    assert str(e.value) == 'None is not compatible with weight:float.'


def test_field_descriptor_validation_value_error():
    class Cat(Persistent):
        name: str
        weight: float

    with pytest.raises(TypeError) as e:
        felix = Cat(name='Felix', weight='half stone')

    assert str(e.value) == "'half stone' is not compatible with weight:float."


def test_constructor_attribute_error():
    class Cat(Persistent):
        name: str
        weight: float

    with pytest.raises(AttributeError) as e:
        felix = Cat(name='Felix', weight=3.2, age=7)

    assert str(e.value) == "'Cat' has no attribute 'age'"
