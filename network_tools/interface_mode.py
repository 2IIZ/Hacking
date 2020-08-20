#!/usr/bin/env python

import subprocess
import optparse
import re

# execute with python 2.7
# inline execution -> "python2.7 interface_mode.py -i wlan0 -m monitor"
parser = optparse.OptionParser()
parser.add_option("-i", "--interface", dest="interface", help="Interface (eth0, wlan0...)")
parser.add_option("-m", "--mode", dest="mode", help="Mode (Monitor, Managed...)")

(options, arguments) = parser.parse_args()

interface = options.interface
new_mode = options.mode


def check_mode():
    iw_info = subprocess.check_output(["iw", interface, "info"])
    iw_info_type = re.search(r"(?:type )(.+)", iw_info)
    if iw_info_type:
        return str(iw_info_type.group(1))
    else:
        return "Could not found MAC address"


print("Old mode : " + check_mode())
old_mode = check_mode()


if new_mode.lower() == "monitor":
    print("[+] Changing to Monitor Mode for " + interface)
    subprocess.call(["ip", "link", "set", interface, "down"])
    subprocess.call(["airmon-ng", "check", "kill"])
    subprocess.call(["iw", interface, "set", "monitor", "control"])
    subprocess.call(["ip", "link", "set", interface, "up"])
elif new_mode.lower() == "managed":
    print("[+] Changing to Managed Mode for " + interface)
    subprocess.call(["ip", "link", "set", interface, "down"])
    subprocess.call(["iw", interface, "set", "type", "managed"])
    subprocess.call(["ip", "link", "set", interface, "up"])
    subprocess.call(["systemctl", "start", "NetworkManager"])
else:
    print("error, try with : 'monitor' or 'managed'")

print("New mode : " + check_mode())

if check_mode() == new_mode.lower():
    print("Mode successfully changed.")
else:
    print("Something went wrong...")

