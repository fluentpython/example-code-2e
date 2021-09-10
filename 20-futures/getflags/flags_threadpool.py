#!/usr/bin/env python3

"""Download flags of top 20 countries by population

ThreadPoolExecutor version

Sample run::

    $ python3 flags_threadpool.py
    DE FR BD CN EG RU IN TR VN ID JP BR NG MX PK ET PH CD US IR
    20 downloads in 0.35s

"""

# tag::FLAGS_THREADPOOL[]
from concurrent import futures

from flags import save_flag, get_flag, main  # <1>

def download_one(cc: str):  # <2>
    image = get_flag(cc)
    save_flag(image, f'{cc}.gif')
    print(cc, end=' ', flush=True)
    return cc

def download_many(cc_list: list[str]) -> int:
    with futures.ThreadPoolExecutor() as executor:         # <3>
        res = executor.map(download_one, sorted(cc_list))  # <4>

    return len(list(res))                                  # <5>

if __name__ == '__main__':
    main(download_many)  # <6>
# end::FLAGS_THREADPOOL[]
