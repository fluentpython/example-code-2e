import importlib
import sys
import resource

NUM_VECTORS = 10**7

module = None
if len(sys.argv) == 2:
    module_name = sys.argv[1].replace('.py', '')
    module = importlib.import_module(module_name)
else:
    print(f'Usage: {sys.argv[0]} <vector-module-to-test>')

if module is None:
    print('Running test with built-in `complex`')
    cls = complex
else:
    fmt = 'Selected Vector2d type: {.__name__}.{.__name__}'
    print(fmt.format(module, module.Vector2d))
    cls = module.Vector2d

mem_init = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
print(f'Creating {NUM_VECTORS:,} {cls.__qualname__!r} instances')

vectors = [cls(3.0, 4.0) for i in range(NUM_VECTORS)]

mem_final = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
print(f'Initial RAM usage: {mem_init:14,}')
print(f'  Final RAM usage: {mem_final:14,}')
