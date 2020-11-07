import socket
import threading

hostClient = ''
portClient = 10000
address = (hostClient, portClient)

def connectDataChannel(connection, clientIP):
    option = connection.recv(1024)
    select(option.decode())

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

socketClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketClient.bind(address)
socketClient.listen()

while True:
    connection, clientIP = socketClient.accept()

    clientThread = threading.Thread(target=connectDataChannel, args=(connection, clientIP))
    clientThread.start()






