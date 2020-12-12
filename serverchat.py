import socket
import threading

host='10.35.70.3'
port= 33878

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients=[]
nicknames=[]

#storedValue= "Hello"

# def setupServer():
#     s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     print("Socket created.")

#     try:
#         s.bind((host, port))
#     except socket.error as msg:
#         print(msg)
    
#     print("Socket bind complete.")
#     return s

# def setupConnection():
#     s.listen() #Allow n connections at a time.
#     conn, address = s.accept()
#     print("connected to: ", address[0] + ":" + str(address[1]))
#     return conn

# Sending Messages To All Connected Clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            broadcast(message)
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break

# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()


# def GET():
#     reply = storedValue
#     return reply

# def REPEAT(dataMessage):
#     reply= dataMessage[1]
#     return reply

# def dataTransfer(conn):
# # A loop that sends/receives data until told not to.
#     while True:
#         #receive data
#         data= conn.recv(1024)
#         data= data.decode('utf-8')
#         dataMessage= data.split('',1)
#         command= dataMessage[0]
#         if command == 'GET':
#             reply = GET()
#         elif command == 'REPEAT':
#             reply = REPEAT(dataMessage)
#         elif command == 'EXIT':
#             print("our client left us")
#             break
#         elif command == 'KILL':
#             print("our sever is shutting down")
#             s.close()
#             break
#         else:
#             reply= 'Unknown command'
#         #send reply back to client
#         conn.sendall(str.encode(reply))
#         print("data sent")
#     conn.close()

# s= setupServer()
# while True:
#     try:
#         conn= setupConnection()
#         dataTransfer(conn)
#     except:
#         break