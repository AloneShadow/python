#!/usr/bin/python3

import multiprocessing
import subprocess
import os

domains_list = []
domains = []

fwr = open('DOMAINS_FOR_NS_CHECK_t')
for line in fwr:
    line = line.strip().lower()
    domains_list.append(line)
fwr.close()

for domain in domains_list:
    try:
        ns = (subprocess.check_output("host -t ns "+domain, shell=True).strip()).lower()
    except:
        continue
    if b".dnsnb.ru" in ns:
        domains.append(domain)
        print ("%s in dnsnb.ru" % (domain,))
    if b".firstvds.ru" in ns:
        domains.append(domain)
        print ("%s in firstvds.ru" % (domain,))
    if b".r01.ru" in ns:
        domains.append(domain)
        print ("%s in r01.ru" % (domain,))
    if b".selectel.org" in ns:
        domains.append(domain)
        print ("%s in selectel.org" % (domain,))
    if b".zomro." in ns:
        domains.append(domain)
        print ("%s in .zomro." % (domain,))
    if b".spaceweb.ru" in ns:
        domains.append(domain)
        print ("%s in spaceweb.ru" % (domain,))

print(domains)
print ("Main process exited!")
