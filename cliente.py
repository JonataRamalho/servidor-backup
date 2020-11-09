import socket
import json

HOST = '127.0.0.1'

PORT = 9999

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((HOST, PORT))

msg = {
    "func": "salvar",
    "id": "654",
    "content": "kdu"
}

data = json.dumps(msg)

s.sendall(bytes(data, encoding="utf-8"))

data = s.recv(1024).decode()

print('Mensagem ecoada:', data)
