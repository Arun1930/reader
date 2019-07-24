import socket
import time
import binascii

data="\x04\x00\x44\x72\x5E"
client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.1.252',27011))
while True:
	client.send(data)
	y=binascii.hexlify(data).decode()
	print(y)
	time.sleep(10)
client.close()
