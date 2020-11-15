import socket
import threading
import json

def connectDataChannel():
    client = createSocketClient()

    acceptConnection(client)

def connectControlChannel(): 
    print('Thread canal de controle ')

def createSocketClient():
    address = informClientAddress()

    socketClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socketClient.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socketClient.bind(address)
    socketClient.listen()

    return socketClient

def informClientAddress():
    hostClient = ''
    portClient = 10000

    return (hostClient, portClient)

def acceptConnection(client):
    while True:
        connection, clientIP = client.accept()

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
    data = extractData(connection)

    option = data.decode()

    if option == 'TRANSMITIR':
        transmitFile()
    elif option == 'LISTAR':
        listFile()
    elif option == 'BAIXAR':
        downloadFile()
    
def extractData(connection):
    return connection.recv(2048)

def transmitFile():
    message = 'Opção selecionada >> Transmitir arquivos'
    print(message)

def listFile():
    message = 'Opção selecionada >> Listar arquivos'
    print(message)

def downloadFile():
    message = 'Opção selecionada >> Baixar arquivo'
    print(message)

def send(message):
    connection.sendall(str.encode(message))
    connection.close()

dataChannelThread = threading.Thread(target=connectDataChannel, args=())
controlChannelThread = threading.Thread(target=connectControlChannel, args=())

dataChannelThread.start()
controlChannelThread.start()





