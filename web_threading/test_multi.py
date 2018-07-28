#!/usr/bin/python3

import multiprocessing
import subprocess
import os

domains_list = []
domains = []

fwr = open('DOMAINS_FOR_NS_CHECK')
for line in fwr:
    line = line.strip().lower()
    domains_list.append(line)
fwr.close()

def host(domain):
    try:
        ns = (subprocess.check_output("host -t ns "+domain, shell=True).strip()).lower()
    except:
        return
    if b".dnsnb.ru" in ns:
        soa = (subprocess.check_output("host -t soa "+domain, shell=True).strip()).lower().split()[6]
        if soa[:4] == b"2018":
            print ("%s in dnsnb.ru" % (domain,))
            return domain
    if b".firstvds.ru" in ns:
        soa = (subprocess.check_output("host -t soa "+domain, shell=True).strip()).lower().split()[6]
        if soa[:4] == b"2018":
            print ("%s in firstvds.ru" % (domain,))
            return domain
    if b".r01.ru" in ns:
        soa = (subprocess.check_output("host -t soa "+domain, shell=True).strip()).lower().split()[6]
        if soa[:4] == b"2018":
            print ("%s in r01.ru" % (domain,))
            return domain
    if b".selectel.org" in ns:
        soa = (subprocess.check_output("host -t soa "+domain, shell=True).strip()).lower().split()[6]
        if soa[:4] == b"2018":
            print ("%s in selectel.org" % (domain,))
            return domain
    if b".zomro." in ns:
        soa = (subprocess.check_output("host -t soa "+domain, shell=True).strip()).lower().split()[6]
        if soa[:4] == b"2018":
            print ("%s in .zomro." % (domain,))
            return domain
    if b".spaceweb.ru" in ns:
        soa = (subprocess.check_output("host -t soa "+domain, shell=True).strip()).lower().split()[6]
        if soa[:4] == b"2018":
            print ("%s in spaceweb.ru" % (domain,))
            return domain

pool = multiprocessing.Pool(multiprocessing.cpu_count()*2)
result = [ x for x in pool.map(host, domains_list) if x!=None]
pool.close()
pool.join()

print(result)
print ("Main process exited!")
