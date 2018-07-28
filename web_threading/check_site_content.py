#!/usr/bin/python3
"""
Check site's content.
fw_404 - suspicious sites.
"""


import subprocess
import requests
import multiprocessing

fw_404 = open("405_DOMAINS", 'w')
fw_201 = open("202_DOMAINS", 'w')

for domain in open("201_DOMAINS"):
    try:
        r = requests.get("http://"+domain.strip())
    except:
        print("NoAnswer: ", domain.strip())
        fw_404.write(domain)
        continue
    if domain.strip() == r.text:
        fw_404.write(domain)
        continue
    if len(r.text) == 0:
        fw_404.write(domain)
        continue
    if domain.strip() in r.text and "Powered by VESTA</a>" in r.text:
        fw_404.write(domain)
        continue
    if "Проверка установки и работоспособности скрипта...<br>" in r.text:
        fw_404.write(domain)
        continue
    if "403 Forbidden" in r.text:
        fw_404.write(domain)
        continue
    #print (domain.strip(), r.status_code)
    fw_201.write(domain)

fw_404.close()
fw_201.close()
