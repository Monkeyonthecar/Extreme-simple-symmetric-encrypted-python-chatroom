import time, socket

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad

#change this key if you want, as long it is the same on client and server and 16bytes(128bits) or 24(192bits) or 32byte(256bits)
key = b'16bytepasswordd!'# key is for symmetric encryption

# Basic socket client
print('Client Server...')
time.sleep(1)
# Get the hostname, IP Address from socket and set Port
soc = socket.socket()
shost = socket.gethostname()
ip = socket.gethostbyname(shost)
# get information to connect with the server
print(shost, '({})'.format(ip))
server_host = input('Enter server\'s IP address:')
port = input("Please enter the port the server is listening on: ")
port = int(port)
name = input('Enter Client\'s name: ')
print('Trying to connect to the server: {}, ({})'.format(server_host, port))
time.sleep(1)
soc.connect((server_host, port))
print("Connected...\n")
soc.send(name.encode())
server_name = soc.recv(1024)
server_name = server_name.decode()
print('{} has joined...'.format(server_name))
print('Type !leave to leave the chat room')

while True:
    # Decrypt message from client
    used_iv = soc.recv(1024)
    totalciphermessage = soc.recv(1024)
    cipher = AES.new(key, AES.MODE_CBC, used_iv)
    decoded_mess = unpad(cipher.decrypt(totalciphermessage), AES.block_size)
    decoded_mess = decoded_mess.decode()
    print(server_name, '>', decoded_mess)
    
    # Ask input
    message = input(str("Me > "))
    message = message.encode()  # turn into bytes
    if message == b'!leave':
        print("Goodbye!")
        break
        
    # Encrypt message from client
    cipher = AES.new(key,AES.MODE_CBC)
    used_iv = cipher.iv
    ciphermessage = cipher.encrypt(pad(message, AES.block_size)) # TAKE MAX OF 1008 CHARS PER TIME, OTHERWISE ERROR, IF THIS GETS FIXED ITS NOT SIMPLE ENOUGH
    soc.send(used_iv)
    soc.send(ciphermessage)
    
    #THESE PRINT STATEMENTS ARE FOR LEARNING PURPOSES, SO YOU CAN SEE THAT THE CIPHERTEXT AND IV ARE THE SAME AND GET CHANGED EVERY TIME
    # print("CIPHER: " + str(cipher))
    # print("TOTAL CIPHER " + str(ciphermessage))
    # print("USED IV: " + str(used_iv))
