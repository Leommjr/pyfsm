import socket
from typing import Tuple
from states import ServerState
from parser import parse_request_headers, generate_response_body, generate_response_headers
from logger import log

async def fsm(connection_socket: socket.socket, address: Tuple[str, int],
              BUFFER_SIZE: int):
    # Estado inicial do servidor
    state = ServerState.WAITING_FOR_CONNECTION

    # Loop de processamento da conexão
    while True:
        # Estado de espera por conexão
        if state == ServerState.WAITING_FOR_CONNECTION:
            # Recebimento dos dados da requisição
            data = connection_socket.recv(BUFFER_SIZE)
            # Verificação de dados recebidos
            if data:
                log.info(f"Recebimento de dados de {address}")
                # Alteração do estado para recebimento de cabeçalhos
                state = ServerState.RECEIVING_REQUEST_HEADERS
            else:
                # Fechamento da conexão
                log.info(f"Conexão de {address} fechada")
                connection_socket.close()
                break

        # Estado de recebimento de cabeçalhos
        elif state == ServerState.RECEIVING_REQUEST_HEADERS:
            # Análise dos dados recebidos
            request_method, path, http_version = parse_request_headers(data.decode())
            log.info(f"Requisição {request_method} {path} {http_version} de {address}")
            # Alteração do estado para envio de cabeçalhos
            state = ServerState.SENDING_RESPONSE_HEADERS

        # Estado de envio de cabeçalhos
        elif state == ServerState.SENDING_RESPONSE_HEADERS:
            # Envio dos cabeçalhos da resposta
            response_headers = generate_response_headers(200)
            connection_socket.send(response_headers.encode())
            # Alteração do estado para envio do corpo da resposta
            state = ServerState.SENDING_RESPONSE_BODY

        # Estado de envio do corpo da resposta
        elif state == ServerState.SENDING_RESPONSE_BODY:
            # Envio do corpo da resposta
            response_body = generate_response_body(path)
            connection_socket.send(response_body.encode())
            # Alteração do estado para fechamento da conexão
            state = ServerState.CLOSING_CONNECTION

        # Estado de fechamento da conexão
        elif state == ServerState.CLOSING_CONNECTION:
            # Fechamento da conexão
            connection_socket.close()
            break
