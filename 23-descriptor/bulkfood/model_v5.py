# tag::MODEL_V5_VALIDATED_ABC[]
import abc

class Validated(abc.ABC):

    def __set_name__(self, owner, name):
        self.storage_name = name

    def __set__(self, instance, value):
        value = self.validate(self.storage_name, value)  # <1>
        instance.__dict__[self.storage_name] = value  # <2>

    @abc.abstractmethod
    def validate(self, name, value):  # <3>
        """return validated value or raise ValueError"""
# end::MODEL_V5_VALIDATED_ABC[]

# tag::MODEL_V5_VALIDATED_SUB[]
class Quantity(Validated):
    """a number greater than zero"""

    def validate(self, name, value):  # <1>
        if value <= 0:
            raise ValueError(f'{name} must be > 0')
        return value


class NonBlank(Validated):
    """a string with at least one non-space character"""

    def validate(self, name, value):
        value = value.strip()
        if not value:  # <2>
            raise ValueError(f'{name} cannot be blank')
        return value  # <3>
# end::MODEL_V5_VALIDATED_SUB[]
