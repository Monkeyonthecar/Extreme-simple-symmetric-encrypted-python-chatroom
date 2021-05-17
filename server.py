import time, socket

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Util.Padding import pad

#change this key if you want, as long it is the same on client and server and 16bytes(128bits) or 24(192bits) or 32byte(256bits)
key = b'16bytepasswordd!'# key is for symmetric encryption

#basic socket server
print('Setup Server...')
time.sleep(1)
#Get the hostname, IP Address from socket and set Port
soc = socket.socket()
host_name = socket.gethostname()
ip = socket.gethostbyname(host_name)
port = input("Please enter the port the server has to listen on: ")
port = int(port)
soc.bind((host_name, port))
print(host_name, '({})'.format(ip))
name = input('Enter server\'s name: ')
soc.listen(1) #Try to locate using socket
print('Waiting for incoming connections...')
connection, addr = soc.accept()
print("Received connection from ", addr[0], "(", addr[1], ")\n")
print('Connection Established. Connected From: {}, ({})'.format(addr[0], addr[0]))
#get a connection from client side
client_name = connection.recv(1024)
client_name = client_name.decode()
print(client_name + ' has connected.')
print('Type !leave to leave the chat room')
connection.send(name.encode())

while True:
    # User input
    message = input(str("Me > "))
    message = message.encode()  # turn into bytes
    if message == b'!leave':
        print("Goodbye!")
        break
    
    # Encrypt message towards client
    cipher = AES.new(key, AES.MODE_CBC)
    used_iv = cipher.iv
    ciphermessage = cipher.encrypt(pad(message,AES.block_size))  # TAKE MAX OF 1008 CHARS PER TIME, OTHERWISE ERROR, IF THIS GETS FIXED ITS NOT SIMPLE ENOUGH
    connection.send(used_iv)
    connection.send(ciphermessage)

    # Decrypt message from server
    used_iv = connection.recv(1024)
    totalciphermessage = connection.recv(1024)
    cipher = AES.new(key, AES.MODE_CBC, used_iv)
    decoded_mess = unpad(cipher.decrypt(totalciphermessage), AES.block_size)
    decoded_mess = decoded_mess.decode()
    print(client_name, '>', decoded_mess)
    
    #THESE PRINT STATEMENTS ARE FOR LEARNING PURPOSES, SO YOU CAN SEE THAT THE CIPHERTEXT AND IV ARE THE SAME AND GET CHANGED AFTER EVERY MESSAGE
    # print("CIPHER: " + str(cipher))
    # print("TOTAL CIPHER " + str(totalciphermessage))
    # print("USED IV: " + str(used_iv))
