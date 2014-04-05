

#!/usr/bin/env python

import socket,sys,commands,thread              # Import socket module


def receiveFile(info):
    sl = socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
    filename = info[1]
    ip = info[2]
    print filename,ip
    if(ip==commands.getoutput("/sbin/ifconfig").split("\n")[1].split()[1][5:]):
        print "You own the file"
        return
    else:
        try:
            sl.connect((ip,8769))
            print sl.recv(1024)
            sl.send(filename)
            #file_length =int( sl.recv(1024))
            #sl.send("send")

            print "File receiving\n"
            f= open(filename.split('/')[-1],'wb')
            data = sl.recv(1024)
            while(1):
                f.write(data)
                data = sl.recv(1024)
                if data=='DONE':
                    break
            f.close()
            sl.close()
            print "File received\n>"
            return
        except Exception:
            raise
            print "Could not receive file. Error in connection\n>"
            return

def sendFile(sl,c):
    try:
        filename = c.recv(1024)
        print filename
        f = open(filename,'rb')
        data = f.read()
        k = len(data)
        #c.send(str(k))
        #sl.recv(1024)
        print "sending file " + filename
        for i in range(0,k,1024):
            c.send(data[i:min(i+1023,k)])
        c.send("DONE")
        f.close()
        print"File sent successfully\n>"
        thread.exit()
    except Exception:
        raise
        print "Could not send file."
        thread.exit()


def startServer():
    try:
        sl = socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
        sl.bind((socket.gethostname(),8769))
        print "started"
    except Exception:
        print "Free port 8769. then run client"
        sys.exit(0)
    try:
        sl.listen(5)
        while True:
            c,addr = sl.accept()
            c.send("Downloading File\n")
            #print "\nPlease Wait. Sending file to "+addr[0]
            #filename = c.recv(1024)
            #print filename
            thread.start_new_thread(sendFile,(sl,c))
    except Exception:
        raise
    return


thread.start_new_thread(startServer,())

cl = socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)        # Create a socket object
cl.connect((sys.argv[1], int(sys.argv[2])))
print cl.recv(1024)
while True:
    try:
        A =  cl.recv(1024)
        if(A=='end'):
            print "Connection closed"
            cl.close()
            sys.exit(0)
        elif(A[0]=='$'):
            print A
            receiveFile(A.split())
        else:
	    print A,
        cl.send(raw_input())
    except KeyboardInterrupt:
        cl.send('QUIT')
        cl.close()
        print "Connection Closed"
        sys.exit(0)

