#!/usr/bin/env python3

"""Download flags of countries (with error handling).

asyncio async/await version

"""
# tag::FLAGS2_ASYNCIO_TOP[]
import asyncio
from collections import Counter
from http import HTTPStatus
from pathlib import Path

import httpx
import tqdm  # type: ignore

from flags2_common import main, DownloadStatus, save_flag

# low concurrency default to avoid errors from remote site,
# such as 503 - Service Temporarily Unavailable
DEFAULT_CONCUR_REQ = 5
MAX_CONCUR_REQ = 1000

async def get_flag(client: httpx.AsyncClient,  # <1>
                   base_url: str,
                   cc: str) -> bytes:
    url = f'{base_url}/{cc}/{cc}.gif'.lower()
    resp = await client.get(url, timeout=3.1, follow_redirects=True)   # <2>
    resp.raise_for_status()
    return resp.content

# tag::FLAGS3_ASYNCIO_GET_COUNTRY[]
async def get_country(client: httpx.AsyncClient,
                      base_url: str,
                      cc: str) -> str:    # <1>
    url = f'{base_url}/{cc}/metadata.json'.lower()
    resp = await client.get(url, timeout=3.1, follow_redirects=True)
    resp.raise_for_status()
    metadata = resp.json()  # <2>
    return metadata['country']  # <3>
# end::FLAGS3_ASYNCIO_GET_COUNTRY[]

# tag::FLAGS3_ASYNCIO_DOWNLOAD_ONE[]
async def download_one(client: httpx.AsyncClient,
                       cc: str,
                       base_url: str,
                       semaphore: asyncio.Semaphore,
                       verbose: bool) -> DownloadStatus:
    try:
        async with semaphore:  # <1>
            image = await get_flag(client, base_url, cc)
        async with semaphore:  # <2>
            country = await get_country(client, base_url, cc)
    except httpx.HTTPStatusError as exc:
        res = exc.response
        if res.status_code == HTTPStatus.NOT_FOUND:
            status = DownloadStatus.NOT_FOUND
            msg = f'not found: {res.url}'
        else:
            raise
    else:
        filename = country.replace(' ', '_')  # <3>
        await asyncio.to_thread(save_flag, image, f'{filename}.gif')
        status = DownloadStatus.OK
        msg = 'OK'
    if verbose and msg:
        print(cc, msg)
    return status
# end::FLAGS3_ASYNCIO_DOWNLOAD_ONE[]

# tag::FLAGS2_ASYNCIO_START[]
async def supervisor(cc_list: list[str],
                     base_url: str,
                     verbose: bool,
                     concur_req: int) -> Counter[DownloadStatus]:  # <1>
    counter: Counter[DownloadStatus] = Counter()
    semaphore = asyncio.Semaphore(concur_req)  # <2>
    async with httpx.AsyncClient() as client:
        to_do = [download_one(client, cc, base_url, semaphore, verbose)
                 for cc in sorted(cc_list)]  # <3>
        to_do_iter = asyncio.as_completed(to_do)  # <4>
        if not verbose:
            to_do_iter = tqdm.tqdm(to_do_iter, total=len(cc_list))  # <5>
        error: httpx.HTTPError | None = None  # <6>
        for coro in to_do_iter:  # <7>
            try:
                status = await coro  # <8>
            except httpx.HTTPStatusError as exc:
                error_msg = 'HTTP error {resp.status_code} - {resp.reason_phrase}'
                error_msg = error_msg.format(resp=exc.response)
                error = exc  # <9>
            except httpx.RequestError as exc:
                error_msg = f'{exc} {type(exc)}'.strip()
                error = exc  # <10>
            except KeyboardInterrupt:
                break

            if error:
                status = DownloadStatus.ERROR  # <11>
                if verbose:
                    url = str(error.request.url)  # <12>
                    cc = Path(url).stem.upper()   # <13>
                    print(f'{cc} error: {error_msg}')
            counter[status] += 1

    return counter

def download_many(cc_list: list[str],
                  base_url: str,
                  verbose: bool,
                  concur_req: int) -> Counter[DownloadStatus]:
    coro = supervisor(cc_list, base_url, verbose, concur_req)
    counts = asyncio.run(coro)  # <14>

    return counts

if __name__ == '__main__':
    main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)
# end::FLAGS2_ASYNCIO_START[]
