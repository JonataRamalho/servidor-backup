import socket
import json
import os
import threading

con = None


def receive():
    status = con.recv(1024).decode()
    print(status)


def submit(file):
    con.send(file.encode())


def read_message():
    message = con.recv(1024)
    return message.decode()


def read_data_json():
    try:
        with open('data.json', 'r', encoding='utf8') as f:
            return json.load(f)
    except IOError:
        with open('data.json', 'w', encoding='utf8') as f:
            return read_data_json()


def data_is_empty():
    try:
        file_size = os.stat('data.json').st_size

        if file_size == 0:
            return True
        else:
            return False

    except IOError:
        with open('data.json', 'w', encoding='utf8') as f:
            return data_is_empty()


def save_json(json_file):
    with open('data.json', 'w') as f:
        json.dump(json_file, f, indent=2)


def save(item):
    print(item)
    data = {}
    if data_is_empty():
        data[item["id"]] = item["content"]
        print('>', data)
        save_json(data)
    else:
        data = read_data_json()
        data[item["id"]] = item["content"]
        save_json(data)


def saveIP(ip):
    file = open('ip_cordenador.txt', 'w')
    file.write(ip)
    file.close()


def rescue(key):
    data = {}
    if data_is_empty():
        return print("Error: The data is empty")
    else:
        data = read_data_json()
        if key in data:
            return submit(data[key])
        else:
            return print("Error: ID not found")


def startServer():
    print('\nSERVIDOR INICIADO\n')

    try:
        with open('ip_cordenador.txt', 'r') as f:
            host = f
            host = host.read()
    except IOError:
        print('Erro')

    try:
        port = 8000

        serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serv_socket.bind((host, port))
        serv_socket.listen()

        while True:
            global con
            con, cliente = serv_socket.accept()

            status = con.recv(1024).decode()
            t = threading.Thread(target=teste, args=(con,))
            t.start()
            
    finally:
        con.sendall(str.encode('Desativado'))

def teste(con):
    while True:
        msg = con.recv(1024)
        msg = msg.decode()
        if msg == 'TRANSMITIR':
            data = con.recv(1024).decode()
            data = json.loads(data)
            save(data)
            con.close()
            break

        elif msg == 'BAIXAR':
            ip = con.recv(1024).decode()
            rescue(ip)
            con.close()
            break
        
        elif msg == '':
            break 
        
def sendRegistration():
    HOST = open('ip_cordenador.txt', 'r')
    HOST = HOST.read()
    PORT = 9999

    try:
        serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serv_socket.connect((HOST, PORT))
    except IOError:
        print('\nErro: Coordenador não encontrado. \nVerifique se ele está online.\n')

    hostName = socket.gethostname()
    ip = serv_socket.getsockname()[0]

    msg = {
        "assignment": "cadastrar",
        "ip": ip
    }

    data = json.dumps(msg)
    serv_socket.sendall(bytes(data, encoding="utf-8"))

    data = serv_socket.recv(1024).decode()
    print('Response:', data)


def register():
    response = []
    c = False

    while (len(response) != 4):
        if c:
            print(
                'Digite o IP do coordenador novamente. \nNão esqueça de incluir o "."\n')
        else:
            print('Digite o IP do coordenador. \nEx. 127.0.0.1\n')

        responseTemp = input('> ')
        response = responseTemp.split('.')
        c = True

    saveIP(responseTemp)

    sendRegistration()
    startServer()


def unsubscribe():
    HOST = open('ip_cordenador.txt', 'r')
    HOST = HOST.read()
    PORT = 9999

    try:
        print(1)
        serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serv_socket.connect((HOST, PORT))
        print(2)
    except IOError:
        print('\nErro: Coordenador não encontrado. \nVerifique se ele está online.\n')

    hostName = socket.gethostname()
    ip = socket.gethostbyname(hostName)

    msg = {
        "assignment": "descadastrar",
        "ip": ip
    }

    data = json.dumps(msg)
    serv_socket.sendall(bytes(data, encoding="utf-8"))

    os.remove('ip_cordenador.txt')
    data = serv_socket.recv(1024).decode()
    print('Response:', data)

    print('\nCadastrar novamente.\n')
    menu()


def menuCompleto():
    print('1: Cadastrar servidor')
    print('2: Iniciar')
    print('3: Descadastrar \n')

    response = int(input('> '))

    if response == 1:
        return register()
    elif response == 2:
        return startServer()
    elif response == 3:
        return unsubscribe()
    else:
        print('Invalido \n')
        menuCompleto()


def menuSimplificado():
    print('1: Iniciar')
    print('2: Descadastrar \n')

    response = int(input('> '))

    if response == 1:
        return startServer()
    elif response == 2:
        return unsubscribe()
    else:
        print('Invalido \n')
        menu()


def menu():
    try:
        with open('ip_cordenador.txt', 'r') as f:
            host = f
            host = host.read()
            if host == '':
                register()
            else:
                menuSimplificado()
    except FileNotFoundError:
        register()
    except IOError:
        print('\nServidor fechado')

menu()
