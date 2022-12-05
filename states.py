from enum import Enum
# Definindo os estados do FSM (máquina de estado finito)

class States(Enum):
    IDLE = 'IDLE'
    READING = 'READING'
    WRITING = 'WRITING'
    CLOSING = 'CLOSING'


