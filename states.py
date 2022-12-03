# Estados possíveis do servidor
from enum import Enum
class ServerState(Enum):
    WAITING_FOR_CONNECTION = 0
    RECEIVING_REQUEST_HEADERS = 1
    SENDING_RESPONSE_HEADERS = 2
    SENDING_RESPONSE_BODY = 3
    CLOSING_CONNECTION = 4


