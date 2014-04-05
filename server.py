#!/usr/bin/env python

import socket,sys,commands,thread,os,json

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 20  # Normally 1024, but we want fast response
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((TCP_IP, TCP_PORT))
s.listen(10)
def recieveData(s,conn):
	print "Recieving data"
	f=open('recieveFile','w')
	data = conn.recv(1024)
	print data
	json.dump(data,f)
	print "data recieved"
	f.close()
	conn.close()
#conn, addr = s.accept()
#thread.start_new_thread(recieveFile,(sl,c))
while True:
    conn, addr = s.accept()
    print 'Connection address:', addr
    conn.send("Connection Established")
    thread.start_new_thread(recieveData,(s,conn))
    #data = conn.recv(BUFFER_SIZE)
    #if not data: break
    #print "received data:", data

conn.close()
sock.close()
