from typing import List, Tuple

def tokenize(text: str) -> List[str]:
    return text.upper().split()

l: List[str] = []
l.append(1)
print(l)

t: Tuple[str, float] = ('São Paulo', 12_176_866)
