import socket
import json
import os

host, port = '', 9999
addr = (host, port)


def receive():
    received = read_message()
    return json.loads(received)


def submit(file):
    con.send(file.encode())


def read_message():
    message = con.recv(1024)
    return message.decode()


def read_data_json():
    with open('data.json', 'r', encoding='utf8') as f:
        return json.load(f)


def data_is_empty():
    file_size = os.stat('data.json').st_size

    if file_size == 0:
        return True
    else:
        return False


def save_json(json_file):
    with open('data.json', 'w') as f:
        json.dump(json_file, f, indent=2)


def save(item):
    data = {}
    if data_is_empty():
        data[item["id"]] = item["content"]
        save_json(data)
        return submit("success")
    else:
        data = read_data_json()
        data[item["id"]] = item["content"]
        save_json(data)
        return submit("success")


def rescue(key):
    data = {}
    if data_is_empty():
        return submit("Error: The data is empty")
    else:
        data = read_data_json()
        if key in data:
            return submit(data[key])
        else:
            return submit("Error: ID not found")


def run(file):
    assignment = file["assignment"]

    if assignment == "save":
        save(file)
    elif assignment == "rescue":
        rescue(file["id"])
    else:
        return print('609')


serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

serv_socket.bind(addr)
serv_socket.listen()


while True:
    con, cliente = serv_socket.accept()
    received_file = receive()
    run(received_file)


serv_socket.close()
