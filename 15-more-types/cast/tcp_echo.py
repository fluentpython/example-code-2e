import asyncio

from asyncio import StreamReader, StreamWriter
from asyncio.trsock import TransportSocket
from typing import cast

async def handle_echo(reader: StreamReader, writer: StreamWriter) -> None:
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')

    print(f"Received {message!r} from {addr!r}")

    print(f"Send: {message!r}")
    writer.write(data)
    await writer.drain()

    print("Close the connection")
    writer.close()

async def main() -> None:
    server = await asyncio.start_server(
        handle_echo, '127.0.0.1', 8888)

    # tag::CAST[]
    socket_list = cast(tuple[TransportSocket, ...], server.sockets)
    addr = socket_list[0].getsockname()
    # end::CAST[]
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()

asyncio.run(main())
