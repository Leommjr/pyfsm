from select import select
from collections import deque
from logger import log

class FSM:
    def __init__(self):
        self.tasks = deque()
        self.IDLE = { }
        self.READING = { }
        self.WAIT_WRITE = { }
        self.WRITING = { }
        self.CLOSING = { }
        self.ALLOWED_PATHS = ["index.html", "about.html"]

    def read_file_async(self, path):
        with open(path, 'r') as file:
            yield 'recv', file
            return file.read()

    def process_request(self, req):
        request_str = str(req, 'utf-8')
        method, url, version = request_str.split('\n')[0].split(' ')
        log.info("Metodo: %s ||  Path: %s", method, url)
        if method == "GET":
            # Divide a URL pelo caractere / para extrair o caminho
            path = url.split('/')[1]

            # Armazena o caminho na instância do FSM para uso posterior
            if path not in self.ALLOWED_PATHS:
                path = "index.html"
        return path


    def run(self):
        while any([self.tasks, self.IDLE, self.WAIT_WRITE]):
            while not self.tasks:
                #  I/O
                self.READING, self.WRITING, _ = select(self.IDLE, self.WAIT_WRITE, [])
                for s in self.READING:
                    self.tasks.append(self.IDLE.pop(s))
                for s in self.WRITING:
                    self.tasks.append(self.WAIT_WRITE.pop(s))


            task = self.tasks.popleft()
            try:
                #callback de corrotinas
                why, what = next(task)
                if why == 'recv':
                    log.info("STARTING READING STATE")
                    self.IDLE[what] = task
                elif why == 'send':
                    log.info("STARTING WRITING STATE")
                    self.WAIT_WRITE[what] = task
                
                elif why == 'close':
                    log.info("CLOSING CONNECTION")
                    self.WRITING.pop(self.WRITING.index(what))

                else:
                    raise RuntimeError("SOMETHING BAD")
            except StopIteration:
                log.info("CLIENT DONE")
