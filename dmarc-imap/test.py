#/use/bin/python3
""" IMAP client and DMARC reports parser. """

import email
import imaplib
from pyunpack import Archive
import os
import os.path
import shutil
import time
#import xml.etree.ElementTree as ET
import lxml.etree as ET
import subprocess
import MySQLdb

server = "imap.ukr.net"
port = "993"
login = ""
password = ""
box = imaplib.IMAP4_SSL(server, port)
box.login(login, password)
db = MySQLdb.connect(host='localhost',user="user",db='DMARC',passwd='') #connect to MySQL
cursor = db.cursor()
number_of_processed_files = 0


""" Save to a disk all arhives from messages. """
box.select()
status, msg_set = box.search(None, 'SEEN') # ищем письма
print (status, "Total count of messages in Incoming is %s" % len(msg_set[0].split()))
for unread_msg in msg_set[0].split():
#for msg in msg_set[0].split()[8].decode():
 status, msg = box.fetch(unread_msg, '(BODY[])')
 #print (status, msg[0])
 mail = email.message_from_bytes(msg[0][1])
 #print (mail)
 #print ("From: {0}, Subject: {1}, Date: {2}\n".format(mail["From"], mail["Subject"], mail["Date"]))
 """ Extract archive from message. """
 for part in mail.walk():
    ctype = part.get_content_type()
    if 'application' in ctype:
        archive_name = part.get_filename()
        open(archive_name, 'wb').write(part.get_payload(decode=True))
 try: Archive(archive_name).extractall(os.getcwd())
 except: continue
 os.remove(archive_name)

 if os.path.splitext(archive_name)[1] in (".gz"):
    xmlfile_name = (os.path.splitext(archive_name)[0])
 else:
    xmlfile_name = (os.path.splitext(archive_name)[0]) + '.xml'

 try:
    xml_doc = ET.parse(xmlfile_name).getroot()
 except:
    xmlfile_name = [filename for filename in os.listdir(os.getcwd()) if '.xml' in filename ][0]
    try:
        xml_doc = ET.parse(xmlfile_name).getroot()
    except:
        print ("Smth. wrong with ", xmlfile_name)
        try: shutil.move(xmlfile_name, "fail/")
        except: os.remove(xmlfile_name)
        continue

 reporter_name = xml_doc.find("report_metadata/org_name").text
 if reporter_name == None: reporter_name = "Absent"
 reporter_messages = 0

 """ Extract information from .xml file. """
 #print ("START: ", xmlfile_name, " from ", reporter_name)
 for item in xml_doc.findall("record"):
    ip = item.find("row/source_ip").text
    num_count = item.find("row/count").text
    reporter_messages += int(num_count)
    h_from = item.find("identifiers/header_from").text
    if h_from == None: h_from = "NONE"
    try:
        spf_domain = item.find("auth_results/spf/domain").text
        if spf_domain == None: spf_domain = "NONE"
        spf_result = item.find("auth_results/spf/result").text
    except: spf_domain = "Absent"; spf_result = "Absent"
    try:
        dkim_domain = item.find("auth_results/dkim/domain").text
        if dkim_domain == None: dkim_domain = "NONE"
        dkim_result = item.find("auth_results/dkim/result").text
    except: dkim_domain = "Absent"; dkim_result = "Absent"
    if (dkim_result == 'temperror') and (ip=='212.42.77.199'):
        print (reporter_name, ip, num_count, dkim_domain, dkim_result)
    #print (ip, num_count, h_from, spf_domain, spf_result, dkim_domain, dkim_result)
    #INSERT_REPORT = "INSERT INTO report SET ip=%s, num_count=%s, h_from=%s, spf_domain=%s, spf_result=%s, dkim_domain=%s, dkim_result=%s ON DUPLICATE KEY UPDATE num_count=num_count+%s"
    #cursor.execute(INSERT_REPORT,(ip, num_count, h_from, spf_domain, spf_result, dkim_domain, dkim_result, num_count))
 os.remove(xmlfile_name)
 #INSERT_REPORTERS = "INSERT INTO reporters SET name=%s, num_count=%s ON DUPLICATE KEY UPDATE num_count=num_count+%s"
 #cursor.execute(INSERT_REPORTERS,(reporter_name, reporter_messages, reporter_messages))
 #db.commit()
 #print ("END:   ", xmlfile_name, " from ", reporter_name)
 number_of_processed_files += 1
 box.store(unread_msg, '+FLAGS', '\Seen')
 if not (number_of_processed_files % 200):
    print("Sleeping...")
    time.sleep(30)
    #break


print ("Number of processed files: ", number_of_processed_files, "Number of messages: ", len(msg_set[0].split()))
box.close()
box.logout()
cursor.close()
db.close()

#if __name__ == "__main__":
    #from_spam_to_incoming()
#    box.logout()