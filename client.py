#!/usr/bin/env python

import socket,sys,commands,thread,os,json      

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024
MESSAGE = "Hello, World!"
def sendData(s):
	#have to tune it according to our data then will uncomment the lines
	log = open ('sendLog','r+')
	logs = log.readlines()
	line = int(logs[0])
	log.seek(0)
	log.write(str(int(line)+1))
	log.truncate()
	log.close()
	dataFile = open('databaseFile','r')
	dataFileLines = dataFile.readlines()
	data = dataFileLines[line]
	#convert required datafiles line into a tuple and save it as a json
	# send the json file this would make easier to feed into database at the server
	#data = "1,simple,list1"	
	print data[:-1]
	jsonfile = open('f','w')
	json.dump(data,jsonfile)
	jsonfile.close()
	jsonfile = open('f','r')
	data = jsonfile.read()
	k = len(data)
	for i in range(0,k,1024):
#		print data
		try:
			s.send(data[i:min(i+1023,k)])
		except socket.error:
			exit
	#s.send("\nDONE")
	jsonfile.close()
	thread.exit()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
data = s.recv(BUFFER_SIZE)
#print data
#print "here"
if data == 'Connection Established':
#	print "hello"
	sendData(s)
#s.send(MESSAGE)
s.close()

#print "received data:", data
