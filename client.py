import socket

HOST = '127.0.0.1'
PORT = 8000  

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

def showMenu():
  print('\nInforme uma das opcoes:\n')
  print('1. Transmitir arquivos'
      '\n2. Listar arquivos disponı́veis por apelido' 
      '\n3. Baixar arquivos'
      '\n4. Configurações'
      '\n5. Sair\n')
  
  option = int(input('>>> '))
  handleSelectedOption(option)

def handleMenu(option):
  case = {
    1: lambda option: s.sendall(str.encode('1')),
    2: lambda option: s.sendall(str.encode('2')),
    3: lambda option: s.sendall(str.encode('3')),
    5: lambda option: s.close(),
    }

  return case[option](option)

def handleSubMenu(option):
  case = {
    1: lambda option: 'Configurando apelido...',
    2: lambda option: 'Configurando diretorio...',
    3: lambda option: 'Configurando endereço IP...',
    4: lambda option: showMenu(),
    }
  return case[option](option)

def handleSelectedOption(option):
  if (option != 4):
    response = handleMenu(option)

    if (option == 5):
      print('Saindo...')
    else:
      data = s.recv(1024)
      print('>>> Resposta do servidor:', data.decode())
    
  else: 
    subMenuOption = int(input('\n1. Configurar apelido' 
                    '\n2. Configurar diretório de download'
                    '\n3. Configurar endereço IP do Coordenador'
                    '\n4. Voltar'
                    '\n\n>>> '))

    handleSubMenu(subMenuOption)

showMenu()