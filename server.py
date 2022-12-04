import socket
from typing import Any
from states import ServerState
from parser import parse_request_headers, generate_response_body, generate_response_headers
from fsm import fsm
from routines import gather
from logger import log
import sys, signal
import asyncio

# Função para lidar com Ctrl - C
def signal_handler(signal: int, frame: Any) -> None:
    log.info("Aplicação finalizada manualmente")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
# Configurações do servidor
HOST: str = "127.0.0.1"
PORT: int = 5000
BUFFER_SIZE: int = 1024

# Criação do socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#SO_REUSEADDR indica o reuso de uma socket anterior para fins de otimização
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen()

log.info(f"Servidor iniciado na porta {PORT}")

async def main() -> None:
    # Início do loop principal
    while True:
       # Aceitando uma nova conexão
        connection_socket, address = server_socket.accept()
        log.info(f"Nova conexão de {address}")
        await gather(fsm(connection_socket, address, BUFFER_SIZE))

asyncio.run(main())
"""
The code above uses a finite state machine (FSM) to process requests concurrently in a single thread web server. The FSM is represented by the fsm() coroutine, which is executed concurrently for each request using the gather() function.

The fsm() coroutine processes each request by transitioning between different states, such as WAITING_FOR_CONNECTION, RECEIVING_REQUEST_HEADERS, SENDING_RESPONSE_HEADERS, and SENDING_RESPONSE_BODY. These states correspond to the different steps involved in processing a request, such as receiving the request headers, generating the response headers and body, and closing the connection.

Because the fsm() coroutine is executed concurrently for each request using the gather() function, the web server is able to handle multiple requests concurrently within the same thread. This allows the server to process requests efficiently and avoid blocking the main thread."""
