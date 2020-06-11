# tag::REGISTRATION_ABRIDGED[]
registry = []

def register(func):
    print(f'running register({func})')
    registry.append(func)
    return func

@register
def f1():
    print('running f1()')

print('running main()')
print('registry ->', registry)
f1()
# end::REGISTRATION_ABRIDGED[]
