import socket
import threading

def connectDataChannel():
    print('Thread 1 ok')

def connectControlChannel(): 
    print('Thread 2 ok')

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





