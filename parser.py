from typing import Tuple

# Função para parsear os cabeçalhos da requisição
def parse_request_headers(data: str) -> Tuple[str, str, str]:
    lines = data.split("\r\n")
    request_line = lines[0].split(" ")
    request_method = request_line[0]
    path = request_line[1]
    http_version = request_line[2]
    return request_method, path, http_version

# Função para gerar os cabeçalhos da resposta
def generate_response_headers(status_code: int) -> str:
    response_headers = f"HTTP/1.1 {status_code}\r\n\r\n"
    return response_headers

# Função para gerar o corpo da resposta
def generate_response_body(path: str) -> str:
    if path == "/":
        response_body = "Página inicial"
    elif path == "/about":
        response_body = "Página sobre"
    else:
        response_body = "Página não encontrada"
    return response_body
