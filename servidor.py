import socket
import json

host, port = '', 9999
addr = (host, port)


def receber():
    msg = ler_mensagem()
    return json.loads(msg)


def enviar(txt):
    con.send(txt.encode())


def ler_mensagem():
    mensagem = con.recv(1024)
    return mensagem.decode()


def salvar(nova_data):
    index, content = nova_data["id"], nova_data["content"]
    data = {index: content}

    with open('data.json', 'w') as json_file:
        json.dump(data, json_file, indent=2)

    enviar('Sucesso')


def baixar(index):
    with open("data.json", "r") as json_file:
        data = json.load(json_file)
    data = data[index]
    return data


def executar(data):
    func = data["func"]
    if func == "salvar":
        salvar(data)
    elif func == "baixar":
        content = baixar(data["id"])
        enviar(content)
    else:
        return print('609')


serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

serv_socket.bind(addr)
serv_socket.listen()


while True:
    con, cliente = serv_socket.accept()
    msg = receber()
    executar(msg)


serv_socket.close()
