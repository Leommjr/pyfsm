# pyfsm - Finite State Machine Web Server 

O código é um servidor web simples que usa uma máquina de estados finitos (FSM) para lidar com requisições de entrada de forma concorrente. O servidor usa uma única thread para processar múltiplas solicitações simultaneamente, utilizando coroutines e a biblioteca asyncio.

O servidor é iniciado chamando a função "main", que escuta por conexões de entrada e cria uma coroutine para cada nova conexão usando a função "gather". A função "gather" mantém uma fila de coroutines e itera "acordando" cada coroutine na fila até que todas as coroutines tenham sido concluídas.

A coroutine "fsm" é responsável por lidar com cada conexão individual. Ele processa requisições de entrada, passando por uma série de estados:

WAITING_FOR_CONNECTION: O servidor aguarda por dados de entrada do cliente.
RECEIVING_REQUEST_HEADERS: O servidor recebe e analisa os cabeçalhos da requisição.
SENDING_RESPONSE_HEADERS: O servidor gera e envia os cabeçalhos de resposta para o cliente.
SENDING_RESPONSE_BODY: O servidor gera e envia o corpo da resposta para o cliente.
CLOSING_CONNECTION: O servidor fecha a conexão com o cliente.

A função fsm é uma coroutine que implementa a FSM, que tem vários estados diferentes que representam as diferentes etapas de processamento de uma solicitação. O estado inicial é ServerState.WAITING_FOR_CONNECTION, onde o servidor aguarda por dados de entrada no socket de conexão. Quando os dados são recebidos, a FSM transita para o estado ServerState.RECEIVING_REQUEST_HEADERS, onde analisa os cabeçalhos da solicitação usando a função parse_request_headers.

Depois de analisar os cabeçalhos da solicitação, a FSM transita para o estado ServerState.SENDING_RESPONSE_HEADERS, onde gera os cabeçalhos de resposta usando a função generate_response_headers. A FSM, então, transita para o estado ServerState.SENDING_RESPONSE_HEADERS, onde ele gera os cabeçalhos da resposta usando a função generate_response_headers. A FSM, então, transita para o estado ServerState.SENDING_RESPONSE_BODY, onde ele gera o corpo da resposta usando a função generate_response_body. Finalmente, a FSM transita para o estado ServerState.CLOSING_CONNECTION, onde ela fecha a conexão e termina a coroutine.

Para alcançar a concorrência, a função principal usa a função gather para executar múltiplas coroutines fsm concorrentemente. A função gather cria uma fila de coroutines fsm e as executa em um loop até que todas estejam concluídas. Isso permite que o servidor processe múltiplas solicitações concorrentemente em uma única thread.

## Começando

Para começar a usar este servidor em sua máquina local, siga as instruções abaixo:

1. Clone o repositório para sua máquina local usando o comando `git clone https://github.com/Leommjr/pyfsm.git`.
2. Entre na pasta do repositório clonado usando o comando `cd pyfsm`.
3. Instale as dependências do projeto executando o comando `pip install -r requirements.txt`.
4. Execute o servidor com o comando `python server.py`.

O servidor será iniciado na porta 5000 do seu localhost. Você pode alterar a porta padrão no arquivo `server.py`, alterando o valor da constante `PORT`.

### Pré-requisitos

Para executar este servidor em sua máquina local, você precisará ter o Python 3.6 ou superior instalado. Além disso, é necessário instalar as dependências do projeto, listadas no arquivo `requirements.txt`.

## Executando

Para executar o servidor, basta seguir as instruções na seção "Começando" deste README. Uma vez que o servidor está sendo executado, você pode acessá-lo em seu navegador web digitando `http://localhost:5000` na barra de endereços. O servidor irá processar qualquer requisição HTTP que você enviar e retornará uma resposta apropriada.

## Testando
Para executar requisições simultâneas utilize a ferramenta Apache Bench. Download: https://www.apachelounge.com/download/#google_vignette

Ex: ab.exe -n 100 -c 20 http://127.0.0.1:5000/

Result:
```
Benchmarking 127.0.0.1 (be patient).....done


Server Software:
Server Hostname:        127.0.0.1
Server Port:            5000

Document Path:          /
Document Length:        15 bytes

Concurrency Level:      20
Time taken for tests:   0.257 seconds
Complete requests:      100
Failed requests:        0
Total transferred:      3100 bytes
HTML transferred:       1500 bytes
Requests per second:    388.88 [#/sec] (mean)
Time per request:       51.430 [ms] (mean)
Time per request:       2.571 [ms] (mean, across all concurrent requests)
Transfer rate:          11.77 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    1   3.4      0      16
Processing:    16   45  12.9     47      63
Waiting:        0   44  13.3     47      63
Total:         17   46  13.0     47      63

Percentage of the requests served within a certain time (ms)
  50%     47
  66%     48
  75%     57
  80%     58
  90%     58
  95%     63
  98%     63
  99%     63
 100%     63 (longest request)

```
## Contribuindo

Se você deseja contribuir com este projeto, basta seguir os seguintes passos:

1. Faça um fork do repositório.
2. Crie uma nova branch para as suas alterações usando o comando `git checkout -b my-new-feature`.
3. Faça as alterações necessárias no código.
4. Adicione as alterações ao seu fork do repositório com o comando `git add .`.
5. Faça um commit das suas alterações com o comando `git commit -m "Adicionando nova feature"`.
6. Envie as alterações para o seu fork do repositório com o comando `git push origin my-new-feature`.
7. Crie um novo Pull Request no repositório original.
