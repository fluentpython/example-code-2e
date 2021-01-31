import sys

MAX_BITS = len(format(sys.maxsize, 'b'))
print(f'{MAX_BITS + 1}-bit Python build')

def hash_diff(o1, o2):
    h1 = f'{hash(o1):>0{MAX_BITS}b}'
    h2 = f'{hash(o2):>0{MAX_BITS}b}'
    diff = ''.join('!' if b1 != b2 else ' ' for b1, b2 in zip(h1, h2))
    count = f'!= {diff.count("!")}'
    width = max(len(repr(o1)), len(repr(o2)), 8)
    sep = '-' * (width * 2 + MAX_BITS)
    return (f'{o1!r:{width}} {h1}\n{" ":{width}} {diff} {count}\n'
            f'{o2!r:{width}} {h2}\n{sep}')

if __name__ == '__main__':
    print(hash_diff(1, 1.0))
    print(hash_diff(1.0, 1.0001))
    print(hash_diff(1.0001, 1.0002))
    print(hash_diff(1.0002, 1.0003))
