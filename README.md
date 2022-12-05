# pyfsm - Finite State Machine Web Server 

O código é um servidor web simples que usa uma máquina de estados finitos (FSM) para lidar com requisições de entrada de forma concorrente. O servidor usa uma única thread para processar múltiplas solicitações simultaneamente, utilizando coroutines.
O FSM é inicializado com os estados IDLE, READING, WRITING e CLOSING, que são usados para controlar o fluxo de dados na conexão.
A função run é responsável por iniciar o loop do FSM, enquanto a função process_request é chamada a cada iteração do loop para processar a requisição de acordo com o estado atual. As funções read_request, write_response e close_connection são chamadas a partir da função process_request para realizar as ações de leitura, escrita e fechamento da conexão, respectivamente.
O uso do FSM permite que o servidor gerencie várias conexões de forma concorrente, processando cada uma em seu próprio estado e transição de acordo com o fluxo de dados na conexão. Isso é possível graças ao uso do módulo asyncio, que permite a criação de tarefas assíncronas em Python.
O método run é usado para iniciar o loop do FSM, criando uma nova tarefa assíncrona com o método create_task e chamando o método _run internamente. O método _run é o coração do FSM, contendo o loop principal que será executado enquanto não houver dados a serem lidos no socket e a conexão não estiver sendo fechada.

Dentro do loop principal, o método process_request é chamado a cada iteração para processar a requisição de acordo com o estado atual do FSM. O estado atual é verificado e, de acordo com as transições válidas definidas no dicionário transições, é definido o próximo estado do FSM. Em seguida, o método process_request é chamado novamente para continuar o processamento da requisição.

O método process_request é responsável por chamar as funções de leitura, escrita e fechamento de conexão de acordo com o estado atual do FSM. Por exemplo, se o estado atual for READING, o método read_request é chamado para ler os dados da requisição do socket. Se o estado for WRITING, o método write_response é chamado para escrever a resposta na conexão. E se o estado for CLOSING, o método close_connection é chamado para fechar a conexão.

O fluxo de execução do código acima é o seguinte:

1. O módulo asyncio é importado, junto com o módulo socket.
2. Os estados e as transições do FSM são definidos.
3. A classe FSM é definida, que é responsável por gerenciar uma conexão.
4. A função new_connection é definida, que é chamada pela função start_server do módulo asyncio a cada nova conexão.
5. A função main é definida, que inicializa o servidor e o loop de eventos.
6. O servidor é inicializado e começa a escutar por novas conexões.
7. Quando uma nova conexão é estabelecida, a função new_connection é chamada, que cria uma nova instância de FSM para gerenciar a conexão.
8. A instância de FSM é iniciada e começa a rodar
9. O loop interno do FSM fica rodando indefinidamente, processando a requisição de acordo com o seu estado atual.
10. Quando o estado atual é IDLE, o próximo estado é definido como READING.
11. Quando o estado atual é READING, o método read_request é chamado para ler os dados da requisição do socket.
12. Quando o estado atual é WRITING, o método write_response é chamado para enviar uma resposta para o cliente.
13. Quando o estado atual é CLOSING, o método close_connection é chamado para fechar a conexão com o cliente.
14. O loop interno do FSM volta para o início e repete os passos 9-13 até que a conexão seja fechada ou ocorra um erro.

## Começando

Para começar a usar este servidor em sua máquina local, siga as instruções abaixo:

1. Clone o repositório para sua máquina local usando o comando `git clone https://github.com/Leommjr/pyfsm.git`.
2. Entre na pasta do repositório clonado usando o comando `cd pyfsm`.
3. Instale as dependências do projeto executando o comando `pip install -r requirements.txt`.
4. Execute o servidor com o comando `python server.py`.

O servidor será iniciado na porta 8080 do seu localhost. Você pode alterar a porta padrão no arquivo `server.py`, alterando o valor da constante `PORT`.

### Pré-requisitos

Para executar este servidor em sua máquina local, você precisará ter o Python 3.6 ou superior instalado. Além disso, é necessário instalar as dependências do projeto, listadas no arquivo `requirements.txt`.

## Executando

Para executar o servidor, basta seguir as instruções na seção "Começando" deste README. Uma vez que o servidor está sendo executado, você pode acessá-lo em seu navegador web digitando `http://localhost:5000` na barra de endereços. O servidor irá processar qualquer requisição HTTP que você enviar e retornará uma resposta apropriada.

## Testando
Para executar requisições simultâneas utilize a ferramenta Apache Bench. Download: https://www.apachelounge.com/download/#google_vignette

Ex: ab.exe -n 100 -c 20 http://127.0.0.1:8080/

Result:
```
Benchmarking 127.0.0.1 (be patient).....done


Server Software:
Server Hostname:        127.0.0.1
Server Port:            8080

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
