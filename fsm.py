import asyncio
from logger import log

# Definindo os estados do FSM (máquina de estado finito)
IDLE = 'IDLE'
READING = 'READING'
WRITING = 'WRITING'
CLOSING = 'CLOSING'

# Definindo as transicoes do FSM
transicoes = {
    IDLE: (READING,),
    READING: (WRITING,),
    WRITING: (CLOSING,),
    CLOSING: (IDLE,),
}

# Definindo o FSM
class FSM:
    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        """Inicializa o FSM

        Args:
            reader: O leitor de stream do asyncio
            writer: O escritor de stream do asyncio
        """
        # Inicializando o estado do FSM
        self.state = IDLE
        self.reader = reader
        self.writer = writer

    async def run(self) -> None:
        """Inicia o loop do FSM"""
        await asyncio.create_task(self._run())

    async def _run(self) -> None:
        """Loop do FSM"""
        while not self.reader.at_eof() and not self.writer.is_closing():
            # Mantém o loop do FSM rodando indefinidamente
            while True:
                # Processa a requisição de acordo com o estado atual
                if self.state == IDLE:
                    next_state = READING
                elif self.state == READING:
                    next_state = WRITING
                elif self.state == WRITING:
                    next_state = CLOSING
                elif self.state == CLOSING:
                    next_state = IDLE

                if self.writer.is_closing():
                    # Retorna sem mudar o estado do FSM
                    return
                # Verifica se o próximo estado é válido
                if next_state in transicoes[self.state]:
                    # Define o próximo estado como o estado atual
                    self.state = next_state

                await self.process_request()

    async def process_request(self) -> None:
        """Processa a requisição de acordo com o estado atual do FSM"""
        if self.writer.is_closing():
            # Retorna do método sem processar a requisição
            return
        # Processa a requisição de acordo com o estado atual
        if self.state == READING:
            log.info("LENDO")
            await self.read_request()
        elif self.state == WRITING:
            log.info("ESCREVENDO")
            await self.write_response()
        elif self.state == CLOSING:
            log.info("FECHANDO")
            await self.close_connection()

    async def read_request(self) -> None:
        """Lê a requisição do socket"""
        request = await self.reader.readuntil(b'\r\n')
        # Converte os dados da requisição em uma string
        if request == b'':
            return

        request_str = str(request, 'utf-8')
        # Analisa os dados da requisição para extrair o método HTTP e a URL
        method, url, version = request_str.split('\n')[0].split(' ')
        log.info(f"Requisição: {method} | Path: {path}")
        # Se o método for GET, processa a requisição
        if method == "GET":
            # Divide a URL pelo caractere / para extrair o caminho
            path = url.split('/')[1]

            # Armazena o caminho na instância do FSM para uso posterior
            self.path = path

    async def write_response(self) -> None:
        """Escreve a resposta na conexão"""
        # Se o caminho for /, cria uma resposta com uma mensagem "Hello World"
        # Cria os dados da resposta
        response_data = "HTTP/1.1 200 OK\r\n\r\nContent-Type: text/html\r\n\n<html><body><h1>Bem-vindo ao meu site!</h1><p>Esta é uma resposta HTML de exemplo que pode ser enviada usando sockets.</p></body></html>\r\n"
        # Converte os dados da resposta em um objeto bytes
        if self.path == "abc":
            await asyncio.sleep(3)
        response_bytes = bytes(response_data, "utf-8")
        # Escreve os dados da resposta no socket
        if self.writer.is_closing():
            # Retorna do método sem enviar a resposta
            return
        try:
            self.writer.write(response_bytes)
            await self.writer.drain()
        except Exception as e:
           log.info(str(e))

    async def close_connection(self) -> None:
        """Fecha a conexão"""
        if self.writer.is_closing():
            # Retorna do método sem fechar a conexão novamente
            return
        # Fecha a conexão
        self.writer.close()
        await self.writer.wait_closed()



