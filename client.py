import socket
import threading

# choosing a username 
username = input("choose a username: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))  # connecting to the server


# defining a function to receive data form the server
def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == "NICK":
                client.send(username.encode('ascii'))
            else:
                print(message)
        except:
            print("error occurred!")
            client.close()
            break


# defining a function to write messages
def write():
    while True:
        message = f'{username}: {input("")}'
        client.send(message.encode('ascii'))


# starting a thread for receive function

receive_thread = threading.Thread(target=receive)
receive_thread.start()


# starting a thread for write function

write_thread = threading.Thread(target=write)
write_thread.start()
