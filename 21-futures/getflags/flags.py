#!/usr/bin/env python3

"""Download flags of top 20 countries by population

Sequential version

Sample runs (first with new domain, so no caching ever)::

    $ ./flags.py
    BD BR CD CN DE EG ET FR ID IN IR JP MX NG PH PK RU TR US VN
    20 downloads in 26.21s
    $ ./flags.py
    BD BR CD CN DE EG ET FR ID IN IR JP MX NG PH PK RU TR US VN
    20 downloads in 14.57s


"""

# tag::FLAGS_PY[]
import time
from pathlib import Path
from typing import Callable

import requests  # <1>

POP20_CC = ('CN IN US ID BR PK NG BD RU JP '
            'MX PH VN ET EG DE IR TR CD FR').split()  # <2>

BASE_URL = 'http://fluentpython.com/data/flags'       # <3>
DEST_DIR = Path('downloaded')                         # <4>

def save_flag(img: bytes, filename: str) -> None:     # <5>
    (DEST_DIR / filename).write_bytes(img)

def get_flag(cc: str) -> bytes:  # <6>
    cc = cc.lower()
    url = f'{BASE_URL}/{cc}/{cc}.gif'
    resp = requests.get(url)
    return resp.content

def download_many(cc_list: list[str]) -> int:  # <7>
    for cc in sorted(cc_list):                 # <8>
        image = get_flag(cc)
        print(cc, end=' ', flush=True)         # <9>
        save_flag(image, cc.lower() + '.gif')
    return len(cc_list)

def main(downloader: Callable[[list[str]], int]) -> None:  # <10>
    t0 = time.perf_counter()                               # <11>
    count = downloader(POP20_CC)
    elapsed = time.perf_counter() - t0
    print(f'\n{count} downloads in {elapsed:.2f}s')

if __name__ == '__main__':
    main(download_many)     # <12>
# end::FLAGS_PY[]
