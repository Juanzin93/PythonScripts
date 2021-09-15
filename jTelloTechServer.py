import socket
import threading
import pickle
HEADER = 64
PORT = 9316
SERVER = "0.0.0.0"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!Disconnect"
DBHOST = "68.205.37.3"
DBUSER = "juanzin"
DBPASSWORD = "rionovo123"
DBDATABASE = "JtTech"
DBPORT = "3306"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
databaseData = [DBHOST,DBUSER,DBPASSWORD,DBDATABASE,DBPORT]
def splitWord(word):
    return [char for char in word]

def handleClient(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    global DBHOST
    global DBUSER
    global DBPASSWORD
    global DBDATABASE
    global DBPORT
    connected = True
    while connected:
        msgLength = conn.recv(HEADER).decode(FORMAT)
        if msgLength:
            msgLength = int(msgLength)
            msg = conn.recv(msgLength).decode(FORMAT)
            if msg ==  DISCONNECT_MESSAGE:
                print(f"[{addr}] Disconnected from the server.")
                connected = False
            else:
                if msg == "getDatabaseHost":
                    print(f"[{addr}] {msg}")
                    conn.send(databaseData[0].encode(FORMAT))
                
                if msg == "getDatabaseUser":
                    print(f"[{addr}] {msg}")
                    conn.send(databaseData[1].encode(FORMAT))
                    
                if msg == "getDatabasePassword":
                    print(f"[{addr}] {msg}")
                    conn.send(databaseData[2].encode(FORMAT))
                    
                if msg == "getDatabaseTable":
                    print(f"[{addr}] {msg}")
                    conn.send(databaseData[3].encode(FORMAT))
                
                if msg == "getDatabasePort":
                    print(f"[{addr}] {msg}")
                    conn.send(databaseData[4].encode(FORMAT))
                else:
                    print(f"[{addr}] {msg}")
                
    conn.close()    
#def send(msg):
#    message = msg.encode(FORMAT)
#    msgLength = len(message)
#    sendLength = str(msgLength).encode(FORMAT)
#    sendLength += b' ' * (HEADER - len(sendLength))
#    server.send(sendLength)
#    server.send(message)

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handleClient, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONENECTIONS] {threading.active_count() - 1}")

print("[STARTING] Server is starting...")
start()