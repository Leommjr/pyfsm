# pyfsm - Finite State Machine Web Server 

Este é um servidor HTTP simples escrito em Python. Ele foi desenvolvido como um exemplo de como criar um servidor HTTP básico usando sockets e o conceito de Finite State Machines 

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

## Contribuindo

Se você deseja contribuir com este projeto, basta seguir os seguintes passos:

1. Faça um fork do repositório.
2. Crie uma nova branch para as suas alterações usando o comando `git checkout -b my-new-feature`.
3. Faça as alterações necessárias no código.
4. Adicione as alterações ao seu fork do repositório com o comando `git add .`.
5. Faça um commit das suas alterações com o comando `git commit -m "Adicionando nova feature"`.
6. Envie as alterações para o seu fork do repositório com o comando `git push origin my-new-feature`.
7. Crie um novo Pull Request no repositório original.
