import sys, smtplib, string

fromaddr = raw_input("From: ")
toaddrs  = string.splitfields(raw_input("To: "), ',')
print "Enter message, end with ^D:"
msg = ''
while 1:
    line = sys.stdin.readline()
    if not line:
        break
    msg = msg + line

# The actual mail send
server = smtplib.SMTP('localhost')
server.sendmail(fromaddr, toaddrs, msg)
server.quit()
