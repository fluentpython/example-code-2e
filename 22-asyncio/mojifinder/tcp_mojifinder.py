#!/usr/bin/env python3

# tag::TCP_MOJIFINDER_TOP[]
import sys
import asyncio
import functools

from charindex import InvertedIndex, format_results  # <1>

CRLF = b'\r\n'
PROMPT = b'?> '

async def finder(index: InvertedIndex,          # <2>
                 reader: asyncio.StreamReader,
                 writer: asyncio.StreamWriter):
    client = writer.get_extra_info('peername')  # <3>
    while True:  # <4>
        writer.write(PROMPT)  # can't await!  # <5>
        await writer.drain()  # must await!  # <6>
        data = await reader.readline()  # <7>
        try:
            query = data.decode().strip()  # <8>
        except UnicodeDecodeError:  # <9>
            query = '\x00'
        print(f' From {client}: {query!r}')  # <10>
        if query:
            if ord(query[:1]) < 32:  # <11>
                break
            results = await search(query, index, writer)  # <12>
            print(f'   To {client}: {results} results.')  # <13>

    writer.close()  # <14>
    await writer.wait_closed()  # <15>
    print(f'Close {client}.')  # <16>
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
async def supervisor(index: InvertedIndex, host: str, port: int):
    server = await asyncio.start_server(    # <1>
        functools.partial(finder, index),   # <2>
        host, port)                         # <3>
    addr = server.sockets[0].getsockname()  # type: ignore  # <4>
    print(f'Serving on {addr}. Hit CTRL-C to stop.')
    await server.serve_forever()  # <5>

def main(host: str = '127.0.0.1', port_arg: str = '2323'):
    port = int(port_arg)
    print('Building index.')
    index = InvertedIndex()                         # <6>
    try:
        asyncio.run(supervisor(index, host, port))  # <7>
    except KeyboardInterrupt:                       # <8>
        print('\nServer shut down.')

if __name__ == '__main__':
    main(*sys.argv[1:])
# end::TCP_MOJIFINDER_MAIN[]
