import socket

ip = '127.0.0.1'
port = 9999
addr = ((ip,port)) 


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

client_socket.connect(addr) 
mensagem = input("Mensagem: ") 

client_socket.send(str.encode(mensagem))

print('mensagem enviada') 
client_socket.close()