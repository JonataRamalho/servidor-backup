<h1 align="center">
    <img  alt="servidor-backup"  src=".github/logo.svg"  height="200" />
</h1>

<p align="center">
  <a href="#sobre">Sobre</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#tecnologias">Tecnologias</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#participantes">Participantes</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#como-executar">Como Executar</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
    <a href="#protocolo">Protocolo</a>

</p>

## Sobre

O **Servidor Backup** é uma aplicação que tem como proposta possibilitar que usuários, fazendo uso de uma aplicação cliente, possam salvar e recuperar arquivos armazenados em rede.

<p  align="center">
   <img  alt="design da aplicação"  width="500px" src="./.github/esquema.svg" />
<p>

A aplicação como visto na imagem acima apresenta três tipos de nós. São eles:

- Clientes: representam as aplicações utilizadas pelos usuários para transmitir e receber arquivos;
- Coordenador: aplicação responsável por servir como ponto de coordenação interconectando os clientes e os servidores de arquivos;
- Servidores de arquivo: responsáveis por armazenar efetivamente os dados enviados pelo cliente.

## Tecnologias

- Python 3.8.5
- Socket
- Thread
- Json

**SO**: Linux Ubuntu

## Participantes

- [Carlos Eduardo](https://github.com/kduFL)
- [Jonata Ramalho](https://github.com/JonataRamalho)
- [Lucilene Bezerra](https://github.com/LuhBezerra)

## Como Executar

- ### **Pré-requisitos**

  - É **necessário** possuir o **[Python3](https://www.python.org/downloads/release/python-385/)** instalado no computador
  - É **necessário** possuir o **[Git](https://git-scm.com/)** instalado e configurado no computador

1. Faça um clone do repositório:

```sh
  $ git clone https://gitlab.com/LuhBezerra1/servidor-backup.git
```

2. Executando a Aplicação:

```sh
  $ cd servidor-backup
```

- Será necessário executar três serviços, em terminais distintos:

```sh
  # TERMINAL 1: Inicia o coordenador
  $ python3 coordinator.py
```

```sh
  # TERMINAL 2: Inicia o servidor
  $ python3 server.py
```

```sh
  # TERMINAL 3: Inicia o cliene
  $ python3 client.py
```

> **Lembre-se** _de executar nessa ordem para que tudo funcione como o desejado_ 

3. Do lado do cliente irá aparecer o seguinte menu:

```
  1. Transmitir 			# Faz o upload de arquivos
  2. Listar					# Lista os arquivos que estão no servidor
  3. Baixar					# Faz download de arquivo
  4. Configurações	        # Pontos necessário para iniciar o cliente
  5. Sair					# Sai do cliente
```

> **É de suma importância** fazer todas as configurações necessário antes de iniciar quaisquer método ( 1, 2 ou 3)

4.  Já do lado do servidor é necessário fazer um cadastramento, para que haja a comunicação entre coordenador <-> servidor, e assim o cliente poderá enviar/receber dados.

## Protocolo

Basicamente define quais mensagens serão enviadas entre os serviços para que haja a comunicação entre eles.

### Métodos

| Verbo      | Descrição                                            |
| ---------- | ---------------------------------------------------- |
| TRANSMITIR | Envia registros para serem salvos no servidor        |
| LISTAR     | Lista os nomes dos registros armazenados no servidor |
| BAIXAR     | Requisitar registros do servidor                     |

### Status de respostas

| SUCESSO | ERRO NO COORDENADOR | ERRO NO SERVIDOR |
| ------- | ------------------- | ---------------- |
| 255     | 158                 | 906              |

#### Dados enviados

1. **TRANSMITIR**

```sh
	# Cliente para Coordenador
	{
		'apelido': '',
		'nome_arquivo': '',
		'conteudo_arquivo': ''
	}
```

```sh
	# Coordenador para Servidor
	{
		'id': '',
		'conteudo_arquivo': ''
	}
```

2.  **LISTAR**

```sh
	# Cliente para Coordenador
	{
		'apelido': ''
	}
```

```sh
	# Coordenador para Cliente
	{
		'list_nome_arquivo': ''
	}
```

3. **BAIXAR**

```sh
	# Cliente para Coordenador
	{
		'apelido': '',
		'id_arquivo': ''
	}
```

```sh
	# Coordenador para Servidor
	{
		'id_arquivo': ''
	}

```

```sh
	# Servidor para Coordenador
	{
		'conteudo_arquivo': ''
	}
```

```sh
	# Coordenador para Cliente
	{
		'nome_arquivo': '',
		'conteudo_arquivo': ''
	}
```
