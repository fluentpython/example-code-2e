# BEGIN MODEL_V4
class Quantity:

    def __set_name__(self, owner, name):  # <1>
        self.storage_name = name          # <2>

    def __set__(self, instance, value):   # <3>
        if value > 0:
            instance.__dict__[self.storage_name] = value
        else:
            msg = f'{self.storage_name} must be > 0'
            raise ValueError(msg)
# END MODEL_V4
