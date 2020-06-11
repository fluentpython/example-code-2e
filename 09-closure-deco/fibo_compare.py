from clockdeco import clock
import fibo_demo
import fibo_demo_lru


@clock
def demo1():
    fibo_demo.fibonacci(30)


@clock
def demo2():
    fibo_demo_lru.fibonacci(30)


demo1()
demo2()
