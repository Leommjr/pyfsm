import socket
import logging
from states import ServerState
from parser import parse_request_headers, generate_response_body, generate_response_headers
import sys, signal

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s - %(message)s")

# Função para lidar com Ctrl - C
def signal_handler(signal, frame):
    logging.info(f"Aplicação finalizada manualmente")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
# Configurações do servidor
HOST = "127.0.0.1"
PORT = 5000
BUFFER_SIZE = 1024

# Criação do socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#SO_REUSEADDR indica o reuso de uma socket anterior para fins de otimização
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen()

logging.info(f"Servidor iniciado na porta {PORT}")
# Início do loop principal
while True:
    # Estado inicial do servidor
    state = ServerState.WAITING_FOR_CONNECTION
    # Aceitando uma nova conexão
    connection_socket, address = server_socket.accept()
    logging.info(f"Nova conexão de {address}")
    # Loop de processamento da conexão
    while True:
        # Estado de espera por conexão
        if state == ServerState.WAITING_FOR_CONNECTION:
            # Recebimento dos dados da requisição
            data = connection_socket.recv(BUFFER_SIZE)
            # Verificação de dados recebidos
            if data:
                logging.info(f"Recebimento de dados de {address}")
                # Alteração do estado para recebimento de cabeçalhos
                state = ServerState.RECEIVING_REQUEST_HEADERS
            else:
                # Fechamento da conexão
                logging.info(f"Conexão de {address} fechada")
                connection_socket.close()
                break

        # Estado de recebimento de cabeçalhos
        elif state == ServerState.RECEIVING_REQUEST_HEADERS:
            # Análise dos dados recebidos
            request_method, path, http_version = parse_request_headers(data.decode())
            logging.info(f"Requisição {request_method} {path} {http_version} de {address}")
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
            logging.info(f"Conexão de {address} fechada")
            connection_socket.close()
            break
