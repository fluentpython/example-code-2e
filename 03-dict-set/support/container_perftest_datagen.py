"""
Generate data for container performance test
"""

import array
import random

MAX_EXPONENT = 7
HAYSTACK_LEN = 10 ** MAX_EXPONENT
NEEDLES_LEN = 10 ** (MAX_EXPONENT - 1)
SAMPLE_LEN = HAYSTACK_LEN + NEEDLES_LEN // 2

needles = array.array('d')

sample = {1 / random.random() for i in range(SAMPLE_LEN)}
print(f'initial sample: {len(sample)} elements')

# complete sample, in case duplicate random numbers were discarded
while len(sample) < SAMPLE_LEN:
    sample.add(1 / random.random())

print(f'complete sample: {len(sample)} elements')

sample = array.array('d', sample)
random.shuffle(sample)

not_selected = sample[:NEEDLES_LEN // 2]
print(f'not selected: {len(not_selected)} samples')
print('  writing not_selected.arr')
with open('not_selected.arr', 'wb') as fp:
    not_selected.tofile(fp)

selected = sample[NEEDLES_LEN // 2:]
print(f'selected: {len(selected)} samples')
print('  writing selected.arr')
with open('selected.arr', 'wb') as fp:
    selected.tofile(fp)
