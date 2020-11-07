import os
import socket

HOST = '127.0.0.1'
PORT = 10000  

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

path = '//home/'

def showMenu():
  print('\nInforme uma das opcoes:\n')
  print('1. Transmitir arquivos'
      '\n2. Listar arquivos' 
      '\n3. Baixar arquivos'
      '\n4. Configurações'
      '\n5. Sair\n')
  
  option = int(input('>>> '))
  handleSelectedOption(option)

def handleMenu(option):
  if (option == 1):
    client.sendall(str.encode('TRANSMITIR')),
  elif (option == 2):
    client.sendall(str.encode('LISTAR')),
  elif (option == 3):
    client.sendall(str.encode('BAIXAR')),
  elif (option == 5):
    client.close(),

def updatePath(currentDirectory):
  global path
  path = path+currentDirectory+'/'

  return path

def listDirectory(directory):
  listDirectory = os.listdir(directory)
  for i in listDirectory:
    print(i)

def getUserName():
  userName = input('\nInforme o nome do usuário do seu pc: ')
  while not os.path.exists(path+userName):
    userName = input('\nInsira um usuario valido!\n>>> ')

  updatePath(userName)

def handleSubMenu(option):
  if (option == 1):
    apelido_usuario = input('Informe seu apelido: ')
    with open('client_data/apelido_usuario.txt','a') as arquivo:
      arquivo.write('\n' + apelido_usuario)

  elif (option == 2):
    getUserName()
    listDirectory(path)

    directory = input('\n## Escolha um dos diretorios listados acima ##\nEx: Downloads\n>>> ')

    while not os.path.exists(path+directory):
      print('\nInsira um diretorio valido (lembre-se que os acentos contam)')
      directory = input('>>> ')

    print('\nSua rota de download foi configurada para: ' + updatePath(directory))
    with open('client_data/diretorio_download.txt','w') as arquivo:
      arquivo.write(path)

  elif (option == 3):
    print('Configurando endereço IP...')

  elif (option == 4):
    showMenu()

def handleSelectedOption(option):
  if (option != 4):
    handleMenu(option)

    if (option == 5):
      print('Saindo...')
    else:
      data = client.recv(1024)
      print('>>> Resposta do servidor:', data.decode())
    
  else: 
    subMenuOption = int(input('\n1. Configurar apelido' 
                    '\n2. Configurar diretorio de download'
                    '\n3. Configurar endereço IP do Coordenador'
                    '\n4. Voltar'
                    '\n\n>>> '))

    handleSubMenu(subMenuOption)

showMenu()