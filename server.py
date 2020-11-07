import socket

HOST = '127.0.0.1'
PORT = 10000   

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()
print('>>> Aguardando conexão com cliente')
connection, address = s.accept()

print('>>> Conectado em', address)
while True:
  data = connection.recv(1024)
  if not data:
    print('>>> Fechando a conexão')
    connection.close()
    break
  connection.sendall(data)