import socket

host='10.35.70.3'
port= 33878

storedValue= "Hello"

def setupServer():
    s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket created.")

    try:
        s.bind((host, port))
    except socket.error as msg:
        print(msg)
    
    print("Socket bind complete.")
    return s

def setupConnection():
    s.listen(1) #Allow n connections at a time.
    conn, address = s.accept()
    print("connected to: ", address[0] + ":" + str(address[1]))
    return conn

def GET():
    reply = storedValue
    return reply

def REPEAT(dataMessage):
    reply= dataMessage[1]
    return reply

def dataTransfer(conn):
# A loop that sends/receives data until told not to.
    while True:
        #receive data
        data= conn.recv(1024)
        data= data.decode('utf-8')
        dataMessage= data.split('',1)
        command= dataMessage[0]
        if command == 'GET':
            reply = GET()
        elif command == 'REPEAT':
            reply = REPEAT(dataMessage)
        elif command == 'EXIT':
            print("our client left us")
            break
        elif command == 'KILL':
            print("our sever is shutting down")
            s.close()
            break
        else:
            reply= 'Unknown command'
        #send reply back to client
        conn.sendall(str.encode(reply))
        print("data sent")
    conn.close()

s= setupServer()

while True:
    try:
        conn= setupConnection()
        dataTransfer(conn)
    except:
        break
