"""
Container ``in`` operator performance test
"""
import sys
import timeit

SETUP = '''
import array
selected = array.array('d')
with open('selected.arr', 'rb') as fp:
    selected.fromfile(fp, {size})
if {test_type} is dict:
    haystack = dict.fromkeys(selected, 1)
else:
    haystack = {test_type}(selected)
if {verbose}:
    print(type(haystack), end='  ')
    print('haystack: %10d' % len(haystack), end='  ')
needles = array.array('d')
with open('not_selected.arr', 'rb') as fp:
    needles.fromfile(fp, 500)
needles.extend(selected[::{size}//500])
if {verbose}:
    print(' needles: %10d' % len(needles), end='  ')
'''

SETUP_NEEDLE_SET = '''
needle_set = set(needles)
if {verbose}:
    print(' needle_set: %10d' % len(needle_set), end='  ')
'''


TEST = '''
found = 0
for n in needles:
    if n in haystack:
        found += 1
if {verbose}:
    print('  found: %10d' % found)
'''

TEST_INTERSECT = '''
found = len(needle_set & haystack)
if {verbose}:
    print('  found: %10d' % found)
'''

def test(test_type, verbose):
    MAX_EXPONENT = 7
    if test_type == 'intersect':
        test_type = 'set'
        setup_template = SETUP + SETUP_NEEDLE_SET
        test_template = TEST_INTERSECT
    else:
        setup_template = SETUP
        test_template = TEST

    for n in range(3, MAX_EXPONENT + 1):
        size = 10**n
        setup = setup_template.format(test_type=test_type,
                             size=size, verbose=verbose)
        test = test_template.format(verbose=verbose)
        tt = timeit.repeat(stmt=test, setup=setup, repeat=5, number=1)
        print('|{:{}d}|{:f}'.format(size, MAX_EXPONENT + 1, min(tt)))

if __name__=='__main__':
    if '-v' in sys.argv:
        sys.argv.remove('-v')
        verbose = True
    else:
        verbose = False
    if len(sys.argv) != 2:
        print('Usage: %s <test_type>' % sys.argv[0])
    else:
        test(sys.argv[1], verbose)
