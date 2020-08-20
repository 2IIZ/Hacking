#!/usr/bin/env python

import requests


def download(url):
    get_response = requests.get(url)
    file_name = url.split("/")[-1]
    #  get_response return "<Response [200]>" means server sent everything ok
    with open(file_name, "wb") as out_file:
        out_file.write(get_response.content)


download("https://www.prospecierara.ch/fileadmin/_processed_/6/9/csm_Capra_Sempione_ProSpecieRara_109_400a31a99c.jpg")
