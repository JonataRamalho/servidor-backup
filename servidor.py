import socket
import json
import os

con = None


def receive():
    #received = read_message()

    # return json.loads(received)

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
        # return submit("success")
    else:
        data = read_data_json()
        data[item["id"]] = item["content"]
        save_json(data)
        # return submit("success")


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
            return print(data[key])
        else:
            return print("Error: ID not found")


def run(file):

    if file == 'RESCUE':
        return None


'''
    assignment = file["assignment"]

    if assignment == "save":
        save(file)
    elif assignment == "rescue":
        rescue(file["id"])
    else:
        return print('609')
'''


def startServer():
    port = 8000
    host = ''

    serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serv_socket.bind((host, port))
    serv_socket.listen()

    global con
    con, cliente = serv_socket.accept()

    status = con.recv(1024).decode()

    while True:
        msg = con.recv(1024).decode()

        if msg == 'TRANSMITIR':
            data = con.recv(1024).decode()
            data = json.loads(data)
            save(data)
        elif msg == 'BAIXAR':
            ip = con.recv(1024).decode()
            rescue(ip)

        #received_file = receive()
        # run(received_file)


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
    ip = socket.gethostbyname(hostName)

    msg = {
        "ip": ip
    }

    data = json.dumps(msg)
    serv_socket.sendall(bytes(data, encoding="utf-8"))

    data = serv_socket.recv(1024).decode()
    print('Response:', data)


def register():
    response = input('IP: ')
    saveIP(response)

    sendRegistration()
    startServer()


def unsubscribe():
    HOST = open('ip_cordenador.txt', 'r')
    HOST = HOST.read()
    PORT = 9999

    try:
        serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serv_socket.connect((HOST, PORT))
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
        menuSimplificado()


def menu():
    try:
        with open('ip_cordenador.txt', 'r') as f:
            host = f
            host = host.read()
            if host == '':
                menuCompleto()
            else:
                menuSimplificado()
    except IOError:
        menuCompleto()


menu()