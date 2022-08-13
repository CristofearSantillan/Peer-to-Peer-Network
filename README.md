# Peer-to-Peer-Network

## Project Description

The main goal of this project is to have all nodes synchronize files across a local area network (LAN). The math theory of this project is down below!

> Nodes $P_{1},P_{2},\ldots P_{n}$ have clients $C_{1},C_{2},\ldots C_{n}$ installed on each node respectively. $F_{1},F_{2},\ldots F_{n}$ are sets of files where $F_{1}$ is the set of files on node $P_{1}, F_{2}$ is the set of files on node $P_{2}$, and so forth.

> The goal will be the unification of all sets of files, $F$, so that $P_{i},C_{i}\cup \{ F_{j}\}$ on each client.

Project process structure: 
1. Finding nodes in the network by broadcasting a message in the network using a specific subnet
2. Create a client and server section for each node (peer)
3. The client side will connect to all the nodes it found in the network and receive files from them
4. The server side will accept as many clients as it can and start transfering files to them

For each connection between client and server, I used the *socket* library to make a TCP connection for file tranfers. For the broadcasting part, I used a UDP socket to send a message to all the nodes in the network. Lastly, I used the *thread* library to handle the server and client section of the program.

## Environment

I used Docker as my network environment and created four nodes as a start (you can modify the program to add as many as you want). Along with Docker, I added a Dockerfile to create an image to make a container (node) for the network and a docker-compose.yml to build and run multiple containers simultaneously. For each node in the network, they will have their own file directory that is attached to the hosts, so any modifications that happen within the node will also happen to the host's file directory. You are able to modify the docker-compose.yml to include more containers as you please but just know that as you add more containers, you need to create more file directories in your host computer to make the file synchronization work properly.

## Before you run

**You must have Docker installed into your computer to make this work.** Below are download links for Docker for each OS.

+ Mac: https://docs.docker.com/docker-for-mac/install/
+ Windows: https://docs.docker.com/docker-for-windows/install/
+ Linux: https://docs.docker.com/install/linux/docker-ce/binaries/

## How to run

1. Clone the repo
   ```sh
   git clone https://github.com/CristofearSantillan/Peer-to-Peer-Network.git
   ```
2. Open a command prompt or terminal and change directories to where you cloned the repo
   ```sh
   cd "location of repo"
   ```
3. Run the docker-compose command
   ```sh
   docker-compose run --build
   ```
