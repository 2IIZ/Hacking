#!/usr/bin/env python

import requests

def request(url):
    try:
        return requests.get("http://"+url)
    except requests.exceptions.ConnectionError:
        pass

request("google.com")
