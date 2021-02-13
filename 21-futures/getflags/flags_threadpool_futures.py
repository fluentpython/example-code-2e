#!/usr/bin/env python3

"""Download flags of top 20 countries by population

ThreadPoolExecutor example with ``as_completed``.
"""
from concurrent import futures

from flags import save_flag, main
from flags_threadpool import download_one


# tag::FLAGS_THREADPOOL_AS_COMPLETED[]
def download_many(cc_list: list[str]) -> int:
    cc_list = cc_list[:5]  # <1>
    with futures.ThreadPoolExecutor(max_workers=3) as executor:  # <2>
        to_do: list[futures.Future] = []
        for cc in sorted(cc_list):  # <3>
            future = executor.submit(download_one, cc)  # <4>
            to_do.append(future)  # <5>
            msg = 'Scheduled for {}: {}'
            print(msg.format(cc, future))  # <6>

        count = 0
        for future in futures.as_completed(to_do):  # <7>
            res: str = future.result()  # <8>
            msg = '{} result: {!r}'
            print(msg.format(future, res)) # <9>
            count += 1

    return count
# end::FLAGS_THREADPOOL_AS_COMPLETED[]

if __name__ == '__main__':
    main(download_many)

