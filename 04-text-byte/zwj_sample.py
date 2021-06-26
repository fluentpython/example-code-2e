from unicodedata import name

zwg_sample = """
1F468 200D 1F9B0            |man: red hair                      |E11.0
1F9D1 200D 1F91D 200D 1F9D1 |people holding hands               |E12.0
1F3CA 1F3FF 200D 2640 FE0F  |woman swimming: dark skin tone     |E4.0
1F469 1F3FE 200D 2708 FE0F  |woman pilot: medium-dark skin tone |E4.0
1F468 200D 1F469 200D 1F467 |family: man, woman, girl           |E2.0
1F3F3 FE0F 200D 26A7 FE0F   |transgender flag                   |E13.0
1F469 200D 2764 FE0F 200D 1F48B 200D 1F469 |kiss: woman, woman  |E2.0
"""

markers = {'\u200D': 'ZWG',  # ZERO WIDTH JOINER
           '\uFE0F': 'V16',  # VARIATION SELECTOR-16
           }

for line in zwg_sample.strip().split('\n'):
    code, descr, version = (s.strip() for s in line.split('|'))
    chars = [chr(int(c, 16)) for c in code.split()]
    print(''.join(chars), version, descr, sep='\t', end='')
    for char in chars:
        if char in markers:
            print(' + ' + markers[char], end='')
        else:
            ucode = f'U+{ord(char):04X}'
            print(f'\n\t{char}\t{ucode}\t{name(char)}', end='')
    print()
