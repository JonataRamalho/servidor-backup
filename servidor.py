import socket 

host = '' 
port = 9999
addr = (host, port) 

serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 

serv_socket.bind(addr) 
serv_socket.listen() 
print('aguardando conexão') 

con, cliente = serv_socket.accept() 
print('conectado')
print("aguardando mensagem...") 

msg = con.recv(1024) 

print("mensagem recebida: " + msg.decode()) 
serv_socket.close() 