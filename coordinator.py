import socket
import threading
import json
import random
import collections
import os

controlChannelSocket = ''
data = collections.defaultdict(dict)
verification = False
ip = '127.0.0.1'
serverData = collections.defaultdict(dict)

def dataChannel():
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
    data = getClientData(connection)

    option = data.decode()

    if option == 'TRANSMITIR':
        transmitFile(connection)
        connection.close()
    elif option == 'LISTAR':
        listFile(connection)
        connection.close()
    elif option == 'BAIXAR':
        downloadFile(connection)
        connection.close()
    
def getClientData(connection):
    return connection.recv(2048)

def transmitFile(connection):
    global ip

    controlChannelSocket.sendall(str.encode("TRANSMITIR"))

    identifier = generateID()
    
    content = getContent(connection)

    transmit(content, identifier)

    saveLocally(content, identifier, ip)

    connection.sendall(str.encode(str(identifier)))

def generateID():
    return random.randint(0, 10000)

def getContent(connection):
    data = getClientData(connection)
    data = data.decode()
    data = json.loads(data)    

    return data

def transmit(content, identifier):
    content = content['conteudo_arquivo']

    content = organizeData(content, identifier)

    content = json.dumps(content)

    send(content)

def organizeData(content, identifier):
    data = {
        'id': str(identifier),
        'content': content
    }

    return data

def saveLocally(content, identifier, ip):
    global data

    nickname = content['apelido']
    fileId = str(identifier)
    fileName = content['nome_arquivo']
    serverIp = ip
    
    data = checkFile(data)

    data[nickname] = data.get(nickname, {})
    data[nickname][fileId] = []
    data[nickname][fileId].append(fileName)
    data[nickname][fileId].append(serverIp)

    save(data)

def save(data):
    with open('coordinatorData.json', 'w') as jsonFile:
        json.dump(data, jsonFile, indent=2)

def checkFile(data):
    global verification
    
    fileVerification = os.path.exists('coordinatorData.json')

    if fileVerification and verification == False:
        verification = True
        with open('coordinatorData.json', 'r') as jsonFile:
            data = json.load(jsonFile)
            
            return data
    
    return data

def listFile(connection):
    nickname = getNickname(connection)
    
    try:
        userData = recoverData()
        
        userData = recover(userData, nickname)

        info = organize(userData, nickname)
    
        connection.sendall(str.encode(info))
    except IOError:
        connection.sendall(str.encode('Nenhum dado salvo'))
    except KeyError:
        connection.sendall(str.encode('Apelido não encontrado'))

def getNickname(connection):
    nickname = getClientData(connection)
    nickname = nickname.decode()
    
    return nickname.replace('"', '') #Colocar return json.loads(nickname)
    
def recoverData():
    with open('coordinatorData.json', 'r') as jsonFile:
        return json.load(jsonFile)

def recover(userData, nickname):
    return userData[nickname]

def organize(userData, nickname):
    info = '\nUsuário: %s' %nickname + "\n\n"

    for fileId in userData:
        fileName = userData[fileId]

        info += '\nID: %s' %fileId +' ---- '+'Nome do Arquivo: %s' %fileName[0] + '\n'

    return info

def downloadFile(connection):
    controlChannelSocket.sendall(str.encode("BAIXAR"))

    nickname, fileId = collectCustomerInformation(connection)

    userData = recoverData()

    try:
        check = nickname in userData
        if check == False:
            raise ValueError('\nUsuário não possui dados salvos no servidor')
        else:
            userData = userData[nickname][fileId]

            send(fileId)

            content = structure(userData)
            
            connection.sendall(bytes(content, encoding="utf-8"))

    except ValueError as err:
        err = str(err)
        connection.sendall(str.encode(err))
        send(fileId)

    except KeyError:
        connection.sendall(str.encode("ID não encontrado"))
        send(fileId)
    
def collectCustomerInformation(connection):
    userData = getClientData(connection)
    userData = userData.decode()
    userData = json.loads(userData)

    nickname = userData['apelido']
    fileId = userData['id']

    return nickname, fileId

def structure(userData):
    content = receiveDataFromServer()
    
    content = {
        'nome_arquivo': userData[0],
        'conteudo': content
    }

    return json.dumps(content)    

def controlChannel(): 
    connectControlCommunication()
'''
    global controlChannelSocket

    controlChannelSocket = createControlChannelSocket()
'''

def connectControlCommunication():
    server = createControlCommunicationSocket()

    acceptControlConnection(server)

def createControlCommunicationSocket():
    communication = 'controle'

    address = informAddress(communication)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(address)
    server.listen()

    return server

def informAddress(communication):
    host = ''
    port = 0

    if communication == 'controle':
        port = 9999
    else:
        host = ''
        port = 8000

    return (host, port)

def acceptControlConnection(server):
    while True:
        connection, ip = server.accept()

        serverThread = threading.Thread(target=serverControl, args=(connection, ip))
        serverThread.start()

def serverControl(connection, ip):
    global serverData
    data = receiveData(connection)
    ip = data['ip']
    method = data['assignment']

    if method == 'cadastrar':
        registerServer(serverData, ip)
        connection.sendall(str.encode('Servidor cadastrado'))
    else:
        unsubscribeServer(serverData, ip)
        connection.sendall(str.encode('Servidor descadastrado'))

    connection.close()

def receiveData(connection):
    dados = connection.recv(2048)
    dados = dados.decode()
    
    return json.loads(dados)

def registerServer(serverData, ip):
    serverData[ip] = serverData.get(ip, {})
    serverData[ip] = []
    serverData[ip].append(0)

    with open('serverData.json', 'w') as jsonFile:
        json.dump(serverData, jsonFile, indent=2)

def unsubscribeServer(serverData, ip):
    serverData.pop(ip, '')        
    
    with open('serverData.json', 'w') as jsonFile:
        json.dump(serverData, jsonFile, indent=2)

def createControlChannelSocket():
    address = informControlChannelAddress()

    controlChannelSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    controlChannelSocket.connect(address)
    controlChannelSocket.sendall(str.encode("255"))
    
    return controlChannelSocket

def informControlChannelAddress():
    host = ''
    port = 8000

    return (host, port)

def send(data):
    controlChannelSocket.sendall(bytes(data, encoding="utf-8"))

def receiveDataFromServer():
    content = controlChannelSocket.recv(2048)
    
    return content.decode()    

#Main
dataChannelThread = threading.Thread(target=dataChannel, args=())
controlChannelThread = threading.Thread(target=controlChannel, args=())

dataChannelThread.start()
controlChannelThread.start()