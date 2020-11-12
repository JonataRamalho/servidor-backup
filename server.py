#Servidor somente para testes do cliente

import socket
import json

HOST = ''
PORT = 10000   

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen()
print('>>> Aguardando conexão com cliente')
connection, address = s.accept()

print('>>> Conectado em', address)
while True:
  #recebe o metodo, envia status
  data = connection.recv(1024)
  print('Metodo:')
  print(data)
  connection.sendall(str.encode('255'))

  #recebe arquivo json
  data = connection.recv(1024)
  data.decode()
  data = json.loads(data)
  print("Arquivo JSON:")
  print(data)
  
  print('\n>>> Fechando a conexão')
  connection.close()
  break