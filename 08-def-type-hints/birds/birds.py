class Bird:
    pass

class Duck(Bird):  # <1>
    def quack(self):
        print('Quack!')

def alert(birdie):  # <2>
    birdie.quack()

def alert_duck(birdie: Duck) -> None:  # <3>
    birdie.quack()

def alert_bird(birdie: Bird) -> None:  # <4>
    birdie.quack()
