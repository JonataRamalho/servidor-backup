import socket
import threading
import json
import random

controlChannelSocket = ''

def connectDataChannel():
    dataChannelSocket = createDataChannelSocket()

    acceptConnection(dataChannelSocket)

def createDataChannelSocket():
    address = informDataChannelAddress()

    dataChannelSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dataChannelSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    dataChannelSocket.bind(address)
    dataChannelSocket.listen()

    return dataChannelSocket

def informDataChannelAddress():
    host = ''
    port = 10000

    return (host, port)

def acceptConnection(dataChannelSocket):
    while True:
        connection, clientIP = dataChannelSocket.accept()

        createClientThread(connection, clientIP)

def createClientThread(connection, clientIP):
    print('Conectado por', clientIP)

    clientThread = threading.Thread(target=confirmConnectionAndSelectOption, args=(connection,))
    clientThread.start()

def confirmConnectionAndSelectOption(connection):

    confirmConnection(connection)

    selectOption(connection)

def confirmConnection(connection):
    connection.sendall(str.encode("255"))

def selectOption(connection):
    data = getData(connection)

    option = data.decode()

    if option == 'TRANSMITIR':
        transmitFile(connection)
    elif option == 'LISTAR':
        listFile()
    elif option == 'BAIXAR':
        downloadFile()
    
def getData(connection):
    return connection.recv(2048)

def transmitFile(connection):
    identifier = generateID()
    
    content = getContent(connection)

    transmit(content, identifier)

def transmit(content, identifier):
    content = content['conteudo_arquivo']

    content = organizeData(content, identifier)

    content = json.dumps(content)

    send(content)

def generateID():
    return random.randint(0, 10000)

def getContent(connection):
    data = getData(connection)
    data = data.decode()
    data = json.loads(data)    

    return data

def organizeData(content, identifier):
    data = {
        'id': str(identifier),
        'content': content
    }

    return data

def listFile():
    message = 'Opção selecionada >> Listar arquivos'
    print(message)

def downloadFile():
    message = 'Opção selecionada >> Baixar arquivo'
    print(message)

def connectControlChannel(): 
    global controlChannelSocket

    controlChannelSocket = createControlChannelSocket()

def createControlChannelSocket():
    address = informControlChannelAddress()

    controlChannelSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    controlChannelSocket.connect(address)

    return controlChannelSocket

def informControlChannelAddress():
    host = ''
    port = 8000

    return (host, port)

def send(data):
    controlChannelSocket.sendall(bytes(data, encoding="utf-8"))

#Main
dataChannelThread = threading.Thread(target=connectDataChannel, args=())
controlChannelThread = threading.Thread(target=connectControlChannel, args=())

dataChannelThread.start()
controlChannelThread.start()





