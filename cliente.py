import socket
import json

HOST = '127.0.0.1'

PORT = 9999

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((HOST, PORT))

'''
msg = {
    "assignment": "save",
    "id": "987",
    "content": "Samsung Brasil"
}
'''
msg = {
    "assignment": "rescue",
    "id": "987"
}

data = json.dumps(msg)

s.sendall(bytes(data, encoding="utf-8"))

data = s.recv(1024).decode()

print('Response:', data)
