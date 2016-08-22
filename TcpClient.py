import socket
import sys
import threading
import struct
import Queue
#import Image
import time

HOST, PORT = "localhost", 5551
#message = "hello from python"
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

try:
	#sock.sendall(message)
	while(1):
		msg = sock.recv(1024)
		#print "Received: {}".format(msg)
		msg = msg.strip()
		if("CurrFrame" in msg):
			print "got frame request"
			#Tell server we will send the image
			sock.sendall("SendingFrame\n")
			
			#TODO: now grab image from device (e.g., gopro)
			#Instead I'm just using an example image here
			
			with open("testimage.jpg", "rb") as imageFile:
				f = imageFile.read()
				b = bytearray(f)
			
			sock.send(b)
			
			print "finished sending frame"
			
except KeyboardInterrupt:
	print "Ctrl-c pressed ..."
	sock.close()
	sys.exit(1)
finally:
	sock.close()