import threading
import socket

# defining the host server(attributes can change)
host = '127.0.0.1'  # localhost
port = 55555

# defining the server to use Internet sockets and use TCP protocol
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((host, port))  # binding server

server.listen()  # opening server to listening traffic

clients = []  # keeping temporary log of the client's ip
usernames = []  # keeping temporary log of the client's username


# defining broadcast function to send the message to all the clients

def broadcast(message):
    for client in clients:
        client.send(message)


#  managing the clients connected to the server

def handle(client):
    while True:
        # checking the connection with the client
        try:
            message = client.recv(1024)  # listening the client
            broadcast(message)
        # deleting the client from the list if the connection with client fails
        except:
            index = clients.index(client)  
            clients.remove(client)
            client.close()  # closing the connection with the client
            username = usernames[index]
            broadcast(f'{username} left the chat! '.encode('ascii'))
            usernames.remove(username)
            break


# receiving messages from the client

def receive():
    while True:
        client, address = server.accept()  # accepting the client's connection
        print(f"Connected with {str(address)}")

        client.send("NICK".encode('ascii'))  # trigger to ask the client for the user details
        username = client.recv(1024).decode('ascii')
        usernames.append(username)
        clients.append(client)  # adding the details of user in the list

        print(f"username of the client is {username}!")
        broadcast(f'{username} joined the chat!'.encode('ascii'))  # tell the clients in the server about new user
        client.send('connected to the server!'.encode('ascii'))  # share any new message

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print('server is listening')
receive()
