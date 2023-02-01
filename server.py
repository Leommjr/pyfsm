from async_socket import AsyncSocket
from socket import *
from fsm import FSM
from select import select
from logger import log


def main(address):
    sock = AsyncSocket(socket(AF_INET, SOCK_STREAM))
    sock.bind(address)
    sock.listen(5)
    while True:
        client, addr = yield from sock.accept()  
        log.info("Connection %s", addr)

        fsm_server.tasks.append(new_connection(client))

def new_connection(client):
    while True:
        req = yield from client.recv(100)  
        if not req:
            break
        
        path = fsm_server.process_request(req)
        resp = yield from fsm_server.read_file_async(path)
        response_data = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\n{resp}\r\n"
        response_bytes = bytes(response_data, "utf-8")
        yield from client.send(response_bytes)    
        yield from client.close()

global fsm_server
fsm_server = FSM()
port = 8080
fsm_server.tasks.append(main(('', port)))
log.info("START SERVER ON PORT %s", port)
fsm_server.run()

