from unicodedata import name

SKIN1 = 0x1F3FB  # EMOJI MODIFIER FITZPATRICK TYPE-1-2  # <1>
SKINS = [chr(i) for i in range(SKIN1, SKIN1 + 5)]       # <2>
THUMB = '\U0001F44d'  # THUMBS UP SIGN 👍

examples = [THUMB]                                      # <3>
examples.extend(THUMB + skin for skin in SKINS)         # <4>

for example in examples:
    print(example, end='\t')                            # <5>
    print(' + '.join(name(char) for char in example))   # <6>
