'''
Server for package listening 
by using sockets

Functioning but currently not in use, needs to be conformed to scp

'''
import socket
import tqdm
import os

# reachable on all ip
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5001

BUFFER_SIZE = 4092
SEPARATOR = "<SEPARATOR>"

s = socket.socket()
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(10)
print(f"Listening as {SERVER_HOST}:{SERVER_PORT}")

client_socket, address = s.accept()
print(f"[+] {address} is connected.")

# receive the file infos
# receive using client socket, not server socket
received = client_socket.recv(BUFFER_SIZE).decode()
print(received)
#filename, filesize = received.split(SEPARATOR)
# remove absolute path if there is
filename = os.path.basename(received)
# convert to integer
#filesize = int(filesize)

# start receiving the file from the socket
# and writing to the file stream
#progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "wb") as f:
    while True:
        # read 1024 bytes from the socket (receive)
        bytes_read = client_socket.recv(BUFFER_SIZE)
        if not bytes_read:    
            # nothing is received
            # file transmitting is done
            break
        # write to the file the bytes we just received
        f.write(bytes_read)
        # update the progress bar
        #progress.update(len(bytes_read))

# close the client socket
client_socket.close()
# close the server socket
s.close()
