#!/usr/bin/env python

import subprocess
import optparse
import re

# execute with python 2.7
# inline execution -> "python2.7 mac_changer.py -i wlan0 -m 00:11:22:33:44:55"
parser = optparse.OptionParser()
parser.add_option("-i", "--interface", dest="interface", help="Interface (eth0, wlan0...)")
parser.add_option("-m", "--mac", dest="new_mac", help="MAC (00:11:22:33:44:55)")

(options, arguments) = parser.parse_args()

interface = options.interface
new_mac = options.new_mac


def check_mac():
    ip_link_show_result = subprocess.check_output(["ip", "link", "show", interface])
    ip_link_show_regex = re.search(r"\w+:\w+:\w+:\w+:\w+:\w+", ip_link_show_result)
    if ip_link_show_regex:
        return str(ip_link_show_regex.group(0))
    else:
        return "Could not found MAC address"


print("Old MAC : "+check_mac())
old_mac = check_mac()

print("[+] Changing MAC address for " + interface + " to " + new_mac)

subprocess.call(["ip", "link", "set", interface, "down"])
subprocess.call(["ip", "link", "set", "dev", interface, "address", new_mac])
subprocess.call(["ip", "link", "set", interface, "up"])


print("New MAC : "+check_mac())
if check_mac() == new_mac.lower():
    print("MAC successfully changed.")
else:
    print("Something went wrong...")


