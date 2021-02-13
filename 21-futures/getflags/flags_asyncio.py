#!/usr/bin/env python3

"""Download flags of top 20 countries by population

asyncio + aiottp version

Sample run::

    $ python3 flags_asyncio.py
    EG VN IN TR RU ID US DE CN MX JP BD NG ET FR BR PH PK CD IR
    20 flags downloaded in 1.07s

"""
# tag::FLAGS_ASYNCIO[]
import asyncio

from aiohttp import ClientSession  # <1>

from flags import BASE_URL, save_flag, main  # <2>

async def get_flag(session: ClientSession, cc: str) -> bytes:  # <3>
    cc = cc.lower()
    url = f'{BASE_URL}/{cc}/{cc}.gif'
    async with session.get(url) as resp:  # <4>
        print(resp)
        return await resp.read()          # <5>

async def download_one(session: ClientSession, cc: str):  # <6>
    image = await get_flag(session, cc)
    print(cc, end=' ', flush=True)
    save_flag(image, cc.lower() + '.gif')
    return cc

async def supervisor(cc_list):
    async with ClientSession() as session:   # <7>
        to_do = [download_one(session, cc)
                 for cc in sorted(cc_list)]  # <8>
        res = await asyncio.gather(*to_do)   # <9>
    return len(res)

def download_many(cc_list):
    return asyncio.run(supervisor(cc_list))  # <10>

if __name__ == '__main__':
    main(download_many)
# end::FLAGS_ASYNCIO[]
