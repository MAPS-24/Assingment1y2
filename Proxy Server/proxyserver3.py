from socket import *
import sys


# Cache
cache = {}

# Example: python ex3.py localhost
# Example URL: http://localhost:8080/www.cubadebate.cu
if len(sys.argv) <= 1:
   print('Usage : "python proxy.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server]\n')
   sys.exit(2)

IP = sys.argv[1]

tcp_ser_sock = socket(AF_INET, SOCK_STREAM)
tcp_ser_sock.bind((IP, 8080))
tcp_ser_sock.listen(5)

while True:
   print('Ready to serve...')
   tcp_cli_sock, addr = tcp_ser_sock.accept()
   print('Received a connection from:', addr)

   message = tcp_cli_sock.recv(4096).decode()

   if not message:
       continue

   print('Message: ' + message)

   route = message.split()[1]
   filename = route.partition("/")[2]
   if len(filename) > 0 and filename[-1] == '/':
       filename = filename[:-1]

   if filename in cache:
       for head in cache[filename]:
           tcp_cli_sock.send(head)

       print('Read from cache')
   else:
       sock = socket(AF_INET, SOCK_STREAM)
       hostn = filename.replace("www.", "", 1)

       server_name = filename.partition("/")[0]
       ask_file = 'http://' + server_name if ''.join(filename.partition('/')[1:]) == '' else ''.join(
           filename.partition('/')[1:])

       try:
           sock.connect((server_name, 80))
           file_obj = sock.makefile('rwb', None)
           header = "GET " + ask_file + " HTTP/1.1\r\nHost: " + server_name + '\r\n\r\n'
           file_obj.write(header.encode())
           file_obj.flush()

           headers = file_obj.readlines()

           status_line = headers[0].decode()
           status_code = int(status_line.split()[1])

           if status_code == '404':
               print('404')
               tcp_cli_sock.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
               tcp_cli_sock.close()
               continue
           else:
               for head in headers:
                  tcp_cli_sock.send(head)

               # save in cache
               cache[filename] = headers
       except:
           print("Illegal request")

   print()

   tcp_cli_sock.close()