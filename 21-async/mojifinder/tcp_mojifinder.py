#!/usr/bin/env python3

# tag::TCP_MOJIFINDER_TOP[]
import asyncio
import functools
import sys
from asyncio.trsock import TransportSocket
from typing import cast

from charindex import InvertedIndex, format_results  # <1>

CRLF = b'\r\n'
PROMPT = b'?> '

async def finder(index: InvertedIndex,          # <2>
                 reader: asyncio.StreamReader,
                 writer: asyncio.StreamWriter) -> None:
    client = writer.get_extra_info('peername')  # <3>
    while True:  # <4>
        writer.write(PROMPT)  # can't await!  # <5>
        await writer.drain()  # must await!  # <6>
        data = await reader.readline()  # <7>
        if not data:  # <8>
            break
        try:
            query = data.decode().strip()  # <9>
        except UnicodeDecodeError:  # <10>
            query = '\x00'
        print(f' From {client}: {query!r}')  # <11>
        if query:
            if ord(query[:1]) < 32:  # <12>
                break
            results = await search(query, index, writer)  # <13>
            print(f'   To {client}: {results} results.')  # <14>

    writer.close()  # <15>
    await writer.wait_closed()  # <16>
    print(f'Close {client}.')  # <17>
# end::TCP_MOJIFINDER_TOP[]

# tag::TCP_MOJIFINDER_SEARCH[]
async def search(query: str,  # <1>
                 index: InvertedIndex,
                 writer: asyncio.StreamWriter) -> int:
    chars = index.search(query)  # <2>
    lines = (line.encode() + CRLF for line  # <3>
                in format_results(chars))
    writer.writelines(lines)  # <4>
    await writer.drain()      # <5>
    status_line = f'{"─" * 66} {len(chars)} found'  # <6>
    writer.write(status_line.encode() + CRLF)
    await writer.drain()
    return len(chars)
# end::TCP_MOJIFINDER_SEARCH[]

# tag::TCP_MOJIFINDER_MAIN[]
async def supervisor(index: InvertedIndex, host: str, port: int) -> None:
    server = await asyncio.start_server(    # <1>
        functools.partial(finder, index),   # <2>
        host, port)                         # <3>

    socket_list = cast(tuple[TransportSocket, ...], server.sockets)  # <4>
    addr = socket_list[0].getsockname()
    print(f'Serving on {addr}. Hit CTRL-C to stop.')  # <5>
    await server.serve_forever()  # <6>

def main(host: str = '127.0.0.1', port_arg: str = '2323'):
    port = int(port_arg)
    print('Building index.')
    index = InvertedIndex()                         # <7>
    try:
        asyncio.run(supervisor(index, host, port))  # <8>
    except KeyboardInterrupt:                       # <9>
        print('\nServer shut down.')

if __name__ == '__main__':
    main(*sys.argv[1:])
# end::TCP_MOJIFINDER_MAIN[]
