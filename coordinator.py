import socket
import threading

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

    clientThread = threading.Thread(target=teste, args=(connection,))
    clientThread.start()

def teste(connection):
    data = connection.recv(1024)

    connection.sendall(data)
    
    print('Coordenador se comunicou com Cliente \n')

def select(option):
    if option == '1':
        transferFile()
    elif option == '2':
        listFile()
    else:
        downloadFile()
    
def transferFile():
    message = 'Opção selecionada >> Transmitir arquivo'
    send(message)

def listFile():
    message = 'Opção selecionada >> Listar arquivos'
    send(message)

def downloadFile():
    message = 'Opção selecionada >> Baixar arquivo'
    send(message)

def send(message):
    connection.sendall(str.encode(message))
    connection.close()

dataChannelThread = threading.Thread(target=connectDataChannel, args=())
controlChannelThread = threading.Thread(target=connectControlChannel, args=())

dataChannelThread.start()
controlChannelThread.start()





