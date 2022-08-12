
import socket
import time
import os
import datetime
from threading import Thread
#from scapy.all import ARP, Ether, srp

#-----------------------------------------------------------------------------#
                            # Locating Nodes Part #
#-----------------------------------------------------------------------------#

# 1st Method to find nodes in the network using socket

print(f"\nNode IP address {socket.gethostbyname(socket.gethostname())}")

nodes = [] # list of all the active nodes
FORMAT = 'utf-8' # format to encode/decode byte to string and vice versa
PORT = 65434 # shared port in all the nodes

# Purpose: Broadcast to every node in the subnet desired with the message of sender's own IP address
def broadcast_LAN():
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # using a UDP socket
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # reused same address 
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # tells the network stack that the socket will be used as a broadcast
    s.sendto(socket.gethostbyname(socket.gethostname()).encode(FORMAT), ("192.168.0.255", PORT)) # sends IP address to a broadcast address to be received from everyone

# Purpose: Listens in for any broadcast message in the network to build up their nodes list. Its agrument is the stop function to kill the thread.
def listen_broadcast(stop):
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.bind(("", PORT)) # binds to all interfaces if left "" for the address argument

    # Keeps looping to receive message from every node in the network
    while True:
        
        data, addr = s.recvfrom(1024) # returns back a tuple of "(socket connection, src address)"
        node = data.decode(FORMAT); # decodes data received to obtain a string type

        # kill the thread from looping forever
        if stop():
            break

        # checks if we already have the node in the list of nodes and if that node is not ourselves
        if node not in nodes and node != socket.gethostbyname(socket.gethostname()):
            nodes.append(node) # adds the node to our list

stop = False # function for killing a thread

# Loops twice to fully obtain all the nodes in the network and creates two threads (one for broadcasting message and the other for listening for that broadcasted message)
for x in range(2):
    
    time.sleep(1)
    Thread(target = listen_broadcast, args = (lambda: stop,)).start() # creates a thread and starts it to listen for broadcasted messages and passes a stop argument to kill the thread
    time.sleep(1)
    Thread(target = broadcast_LAN).start() # creates a thread and starts it to broadcast a message to each node in the network
    
stop = True

# 2nd Method to find nodes in the network using scapy

##print(f"\nNode socket address = {socket.gethostbyname(socket.gethostname())}:PORT")
##
##time.sleep(1)
### Using ARP request broadcast to find nodes in the network. This way who ever response back are active nodes
##result = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst="192.168.0.0/24"), timeout=3, verbose=0)[0]
### Filter the result to only the src address of the responses
##nodes = [received.psrc for sent, received in result[1:]]

#-----------------------------------------------------------------------------#
               # Printing Network Nodes and Files (before sync) #
#-----------------------------------------------------------------------------#
               
PATH = "/files"               
                            
print("\nAvailable devices in the network:")
print(nodes)

print("\nLists of all the files before sync:")
print(os.listdir(PATH))
    
#-----------------------------------------------------------------------------#
                            # File Synchronization Part #
#-----------------------------------------------------------------------------#

SLASH = "/"

# Purpose: To keep receiving files from the node's server and creating a new file in a specific directory if we don't have the file or the content/timestamps are different. Its argument is the socket connection to the node.
def server_handler(s):

    #files = os.listdir(PATH)
    #print(f"\nClient: {files}")

    # infinite loop to keep obtaining files
    while True:
        
        filename_size = s.recv(16).decode(FORMAT) # returns either the file's name size or an empty message indicating there is no more files to receive
        # checks if we received the file's name size or an empty byte
        if not filename_size:
            break
        #print(f"Client: {filename_size}")
        filename_size = int(filename_size, 2) # converts the fixed binary file's name size to an integer
        #print(f"Client: {filename_size}")
        
        filename = s.recv(filename_size).decode(FORMAT) # passes the file's name size integer to the socket.recv function to obtain the full file's name
        #print(f"Client: {filename}")
        
        filesize = s.recv(32).decode(FORMAT) # obtains the file's size and decodes the byte to a string type
        #print(f"Client: {filesize}")
        filesize = int(filesize, 2) # converts the fixed binary file's size to an integer
        #print(f"Client: {filesize}")
        
        mtime = s.recv(42).decode(FORMAT) # gets the file's modification date and decodes the byte to a string type
        #print(f"Client: {mtime}")
        mtime = int(mtime, 2) # converts the fixed binary file's modification date to an integer
        #print(f"Client: {mtime}")
        
        same = True # tells whether there is a file with the same name but different details found
        found = False # tells whether the file is already in the directory
        
        for file in os.listdir(PATH):
            if file == filename:
                if os.path.getsize(PATH+SLASH+file) != filesize or os.stat(PATH+SLASH+file).st_mtime != mtime:
                    same = False
                found = True

        # checks the node we already have the file in the directory. If we do then it tells the node we already have it, else we tell the node we need that file.
        if same and found:
            #print("THIS RAN")
            s.send(b'HAVE_FILE')
            continue
        else:
            #print("HELLO WORLD")
            s.send(b'NEED_FILE')
        
        file = open(PATH+SLASH+filename, 'wb') # opens the file to start writing bytes into it
        CHUNKSIZE = 4096 # default bytes received from the node

        # loops to obtain all the file's data until the file's size is met
        while filesize > 0:

            # checks if the default byte is too large than the file's size
            if filesize < CHUNKSIZE:
                CHUNKSIZE = filesize
                
            data = s.recv(CHUNKSIZE) # receives the data from the node
            file.write(data) # writes that data into the file
            
            filesize -= len(data) # decrease the file's size since we add that byte data into the file

        file.close() # closes the file
        os.utime(PATH+SLASH+filename,(mtime,mtime)) # changes the new file's modification and access date to the original file so it can resemble the same file
        
    #print("Finished at Client side")

    s.close() # closes the socket connection

# Purpose: Creates a new socket each time to connect to every node in the network and each connect is handled by a thread
def start_client():

    # Loops through each node in nodes list
    for node in nodes:
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creates a TCP socket to communicate
        s.connect((node, PORT)) # connects to a specific node through a port
        t1 = Thread(target = server_handler, args = (s, )) # creates a thread to control the receiving file section
        t1.start() # starts the thread
        t1.join() # blocks everything below until the thread is done with its task

# Purpose: To loop through each file in a specific directory and send its details to each node in the network. Its agrument is the socket connection of the node connected.
def client_handler(conn):
    
    #files = os.listdir(PATH)
    #print(f"Server: {files}")

    # loop through each file
    for file in os.listdir(PATH):
        
        filename = file # the name of the file
        #print(f"Server: {filename}")
        filename_size = len(filename) # the length of the file's name
        #print(f"Server: {filename_size}")
        filename_size = bin(filename_size)[2:].zfill(16) # creates a fixed binary length to send to the node so it can receive the file's name completely without any byte loss
        #print(f"Server: {filename_size}")
        conn.send(filename_size.encode(FORMAT)) # sends the file's name size to the node
        conn.send(filename.encode(FORMAT)) # sends the file's name to the node

        filesize = os.path.getsize(PATH+SLASH+filename) # obtains the file's content size
        #print(f"Server: {filesize}")
        filesize = bin(filesize)[2:].zfill(32) # creates a fixed binary length of the file's content size to send to the node
        #print(f"Server: {filesize}")
        conn.send(filesize.encode(FORMAT)) # sends the file's data size
        
        mtime = int(os.stat(PATH+SLASH+filename).st_mtime) # gets the file's modification date (as an integer)
        #print(f"Server: {mtime}")
        mtime = bin(mtime)[2:].zfill(42) # creates a fixed binary length of the file's modification date to send to the node
        #print(f"Server: {mtime}")
        #print(datetime.datetime.fromtimestamp(os.stat(PATH+SLASH+filename).st_mtime))
        conn.send(mtime.encode(FORMAT)) # sends the file's modification date

        # checks if the node already has the file, else it proceeds to sending the data of the file
        if conn.recv(9) == b'HAVE_FILE':
            continue

        _file = open(PATH+SLASH+filename, 'rb') # opens the file to read its data in binary

        data = _file.read() # reads the whole content
        conn.sendall(data) # sends all the data to the node
        
        _file.close() # closes the file
        
        #print("File Sent")
        

    #print("Done sending")
    
    conn.close() # closes the socket connection   

# Purpose: Creates a socket to listen for nodes that wants to connect. Keeps accepting nodes and creates a thread to handle sending file section for that node.
def start_server():
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", PORT))
    s.listen() # listens for any node wanting to connect, if left empty then there is no limit to accepting nodes

    # infinite loop to keep accepting nodes
    while True:
        
        conn, addr = s.accept() # Accepts a node and returns back a tuple of (socket connection, src address). This accept function also blocks everything below until it connects to a node.
        #print("\nGot connection from", addr)
        t1 = Thread(target = client_handler, args = (conn, )) # creates a thread to control sending of files to the connected node
        t1.start() # starts the thread
        t1.join() # waits for the thread to finishing its task

    s.close() # closes the socket

time.sleep(2)
t1 = Thread(target = start_server) # creates a thread to first start up the server part so it can start listening for connections
t1.daemon = True # sets the server thread's daemon to True since the server is in a infinite loop and in a accept blocking state. This way once the process to over, the thread is killed after.
t1.start() # starts the server thread
time.sleep(1)
Thread(target = start_client).start() # creates and starts a client thread to receive new files from other nodes
time.sleep(8)

#-----------------------------------------------------------------------------#
               # Printing Network Nodes and Files (after sync) #
#-----------------------------------------------------------------------------#
                            
print("\nAvailable devices in the network:")
print(nodes)

print("\nLists of all the files after sync:")
print(os.listdir(PATH))
