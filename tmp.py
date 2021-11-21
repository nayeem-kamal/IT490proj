import socket
import subprocess

print(socket.gethostname())

subprocess.run(["scp", filepath, 'dmz@192.168.100.4:/home/dmz/packages'])

