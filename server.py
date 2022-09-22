import socket
import threading

#Variables for holding information about connections
connections = []
total_connections = 0
ACK_TEXT = 'text_received'

#Client class, new instance created for each connected client
#Each instance has the socket and address that is associated with items
#Along with an assigned ID and a name chosen by the client
class Client(threading.Thread):
    def __init__(self, socket, address, id, name, signal):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.id = id
        self.name = name
        self.signal = signal
    
    def __str__(self):
        return str(self.id) + " " + str(self.address)
    
    #Attempt to get data from client
    #If unable to, assume client has disconnected and remove him from server data
    #If able to and we get data back, print it in the server and send it back to every
    #client aside from the client that has sent it
    #.decode is used to convert the byte data into a printable string
    def run(self):
        while self.signal:
            try:
                data = self.socket.recv(32)
            except:
                print("Client " + str(self.address) + " has disconnected")
                self.signal = False
                connections.remove(self)
                break
            if data != "":
                sendTextViaSocket(f"Daulet " + ": " + str(data.decode("utf-8")), self.socket)
                for client in connections:
                    if client.id != self.id:
                        client.socket.sendall(data)

#Wait for new connections
def newConnections(socket):
    while True:
        sock, address = socket.accept()
        global total_connections
        connections.append(Client(sock, address, total_connections, "Name", True))
        connections[len(connections) - 1].start()
        sendTextViaSocket("Daulet connected to the chat", sock)
        total_connections += 1

def sendTextViaSocket(message, sock):
    # encode the text message
    encodedMessage = bytes(message, 'utf-8')

    # send the data via the socket to the server
    sock.sendall(encodedMessage)

    # receive acknowledgment from the server
    encodedAckText = sock.recv(1024)
    ackText = encodedAckText.decode('utf-8')

    # log if acknowledgment was successful
    if ackText == ACK_TEXT:
        print('server acknowledged reception of text')
    else:
        print('error: server has sent back ' + ackText)
    # end if
# end function

def main():
    #Get host and port
    host = input("Host: ")
    port = int(input("Port: "))

    #Create new server socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(5)

    #Create new thread to wait for connections
    newConnectionsThread = threading.Thread(target = newConnections, args = (sock,))
    newConnectionsThread.start()
    
main()