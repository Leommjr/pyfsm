# Importando os módulos asyncio e socket
import asyncio
import socket
from fsm import FSM
from logger import log

async def new_connection(reader, writer) -> None:
    """Cria uma nova conexão"""
    log.info("Nova requisição recebida")
    fsm = FSM(reader, writer)
    await fsm.run()


async def main() -> None:
    # Cria um socket e o associa a um endereço local
    sock = socket.socket()
    sock.bind(('127.0.0.1', 8080))

    # Inicia o loop de eventos e escuta por requisições entrantes
    server = await asyncio.start_server(new_connection, sock=sock)
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
