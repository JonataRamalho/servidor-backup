import socket
import threading
import time

HOST = ''     
PORT = 8000 

def connect(conn, cliente):
    amount_Thread = threading.active_count()

    print('Quantidade de Thread: ', amount_Thread)

    print('Conectado por', cliente)
    
    time.sleep(10)
    
    while True:
        data = conn.recv(1024)
        if not data: 
            print('Finalizando conexão')
            conn.close()
            break
        conn.sendall(data)
        
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((HOST, PORT)) 

s.listen() 

print('Aguardando conexão de um cliente')

while True:
    conn, ender = s.accept() 

    t = threading.Thread(target=connect,args=(conn, ender))

    t.start()






