#!/usr/bin/env python

import socket,sys,commands,thread,os,json,csv,MySQLdb

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 20  # Normally 1024, but we want fast response
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((TCP_IP, TCP_PORT))
s.listen(10)
#connect to mysql server 
mydb = MySQLdb.connect(host='localhost',user='rachit',passwd='dolly7',db='rapid')
cursor = mydb.cursor()
a = []
def recieveData(s,conn):
	print "Recieving Record"
	f=open('recieveFile.csv','w')
	data = conn.recv(1024)
	data  = str(data[1:-1])
	a = data[:-2].split(',')
	print a
	q = "INSERT INTO `pollutants_daily` (id,so,no,co,temp,humidity,o3,rspm,fpm) VALUES  ("+a[1]+","+a[2]+","+a[3]+","+a[4]+","+a[5]+","+a[6]+","+a[7]+","+a[8]+","+a[9]+");"
#	print q
	try:
		cursor.execute(q)
		mydb.commit()
	except:
		mydb.rollback()
	f.write(data[:-2])

	print "Record recieved"
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
