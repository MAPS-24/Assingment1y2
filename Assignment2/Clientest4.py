from socket import *
import time

serverName = '10.0.0.1'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)

for i in range(10):
    time1 = time.time()
    outputdata = 'Ping ' + str(i) + " " + str(time1)
    clientSocket.settimeout(1)
    clientSocket.sendto(outputdata.encode(), (serverName, serverPort))

    try:
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
        timeDiff = time.time() - time1
        print(modifiedMessage.decode() + " RTT: " + str(timeDiff))
    except timeout:
        print(f'Request timed out for Ping {i}')

time.sleep(10)

clientSocket.close()
