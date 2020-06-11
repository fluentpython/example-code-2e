from lake import alert                         # <1>

class Swan:                                    # <2>
    def honk(self, repetitions: int) -> None:  # <3>
        print('Honk! ' * repetitions)

    def swim(self) -> None:                    # <4>
        pass


bella = Swan()

alert(bella)                                   # <5>
