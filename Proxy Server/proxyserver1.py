from socket import *
import sys

# Example: python ex1.py localhost
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

   file_exist = False

   try:
       print('File: ' + filename)
       f = open(filename, "r", encoding='utf-8')
       file_exist = True

       output_data = f.readlines()

       tcp_cli_sock.send("HTTP/1.0 200 OK\r\n".encode())
       tcp_cli_sock.send("Content-Type:text/html\r\n".encode())

       for out in output_data:
           tcp_cli_sock.send(out.encode())

       print('Read from cache')
       print()
   except IOError:
       if not file_exist:
           sock = socket(AF_INET, SOCK_STREAM)
           hostn = filename.replace("www.", "", 1)

           server_name = filename.partition("/")[0]
           ask_file = 'http://' + server_name if ''.join(filename.partition('/')[1:]) == '' else ''.join(filename.partition('/')[1:])

           try:
               sock.connect((server_name, 80))
               file_obj = sock.makefile('rwb', None)
               header = "GET " + ask_file + " HTTP/1.1\r\nHost: " + server_name + '\r\n\r\n'
               file_obj.write(header.encode())
               file_obj.flush()

               headers = file_obj.readlines()

               if headers[0] == b'404':
                   print('404')
                   tcp_cli_sock.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
                   tcp_cli_sock.close()
                   continue

               for head in headers:
                  tcp_cli_sock.send(head)

               tmp_file = open(filename, "wb")

               for head in headers:
                   tmp_file.write(head)

               tmp_file.close()
           except:
               print("Illegal request")
       else:
           tcp_cli_sock.send("HTTP/1.0 404 NOT FOUND\r\n".encode())
           tcp_cli_sock.send("Content-Type:text/html\r\n".encode())
           tcp_cli_sock.send("<html><head><title>Not Found</title></head><body><h1>Not Found</h1></body></html>".encode())
   finally:
       print()

   tcp_cli_sock.close()
input("  aa")