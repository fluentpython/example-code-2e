import time
from typing import Optional

def ctime(secs: Optional[float] = None, /) -> str:
    return time.ctime(secs)
