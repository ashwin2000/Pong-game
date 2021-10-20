import socket, select, sys, time, simplejson
sys.dont_write_bytecode = True
from lib import settings
 
buffer = 2000
delay = 0.01
users = {}
 
class Server:
 
   def __init__(self, host, port):
       self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       self.server.bind((host, port))
       self.server.listen(0)
 
   def main_loop(self):
       self.input_list.append(self.server)
       while 1:
           # TODO: disconnect new clients if the number is > 2
           time.sleep(delay)
           inputr, outputr, exceptr = select.select(self.input_list, [], [])
           for self.s in inputr:
               if self.s == self.server:
                   self.on_accept()
                   break
               else:
                   self.data = self.s.recv(buffer)
               if len(self.data) == 0:
                   self.on_close()
               else:
                   self.on_recv()
 
   def on_accept(self):
       clientsock, clientaddr = self.server.accept()
       print(f"{clientaddr} has connected")
 
 
server = Server(settings.SERVER_IP, settings.SERVER_PORT)
print("Server listening...")
try:
server.main_loop()
except KeyboardInterrupt:
      print("Ctrl C - Stopping server")
      sys.exit(1)
