import socket
import threading
import mysql.connector as mysql

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

SMTPSSL = "smtp.gmail.com"
SMTPPORT = 465
SMTPEMAIL = "jtellotech@gmail.com"
SMTPPASSWORD = "rionovo123"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
databaseData = [DBHOST,DBUSER,DBPASSWORD,DBDATABASE,DBPORT,SMTPSSL,SMTPPORT,SMTPEMAIL,SMTPPASSWORD]
DbClientDatabase = ""


class fetchInfoFromDatabase():
    def getLoginCredentials():
        try: 
            connect = mysql.connect(
                    host = DBHOST,
                    user = DBUSER,
                    passwd = DBPASSWORD,
                    database = DBDATABASE,
                    port = DBPORT,
                    auth_plugin='mysql_native_password'
                    )
        except Exception as e:
            print(e)
            return "unable to access database"

        cursor = connect.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS Users(
                        UserID integer PRIMARY KEY AUTO_INCREMENT,
                        FirstName TEXT,
                        LastName TEXT,
                        Email TEXT,
                        Password TEXT,
                        PhoneNumber TEXT,
                        Address TEXT,
                        City TEXT,
                        State TEXT,
                        ZipCode TEXT,
                        Category TEXT)''')
        
        cursor.execute("SELECT * from Users")
        return cursor.fetchall()

def handleClient(conn, addr):
    global DbClientDatabase
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        msgLength = conn.recv(HEADER).decode(FORMAT)
        if msgLength:
            msgLength = int(msgLength)
            msg = conn.recv(msgLength).decode(FORMAT)
            if msg ==  DISCONNECT_MESSAGE:
                print(f"[{addr}] Disconnected from the server.")
                connected = False
            elif msg == "getDatabaseHost":
                print(f"[{addr}] {msg}")
                conn.send(databaseData[0].encode(FORMAT))
            
            elif msg == "getDatabaseUser":
                print(f"[{addr}] {msg}")
                conn.send(databaseData[1].encode(FORMAT))
                
            elif msg == "getDatabasePassword":
                print(f"[{addr}] {msg}")
                conn.send(databaseData[2].encode(FORMAT))
                
            elif msg == "getDatabaseMainTable":
                print(f"[{addr}] {msg}")
                conn.send(databaseData[3].encode(FORMAT))
            
            elif msg == "getDatabasePort":
                print(f"[{addr}] {msg}")
                conn.send(databaseData[4].encode(FORMAT))
                
            elif msg == "getDatabaseClientTable":
                print(f"[{addr}] {msg}")
                conn.send(DbClientDatabase.encode(FORMAT))

            elif msg == "SMTPSSL":
                print(f"[{addr}] {msg}")
                conn.send(databaseData[5].encode(FORMAT))
                
            elif msg == "SMTPPORT":
                print(f"[{addr}] {msg}")
                conn.send(databaseData[6].encode(FORMAT))
                
            elif msg == "SMTPEMAIL":
                print(f"[{addr}] {msg}")
                conn.send(databaseData[7].encode(FORMAT))
                
            elif msg == "SMTPPASSWORD":
                print(f"[{addr}] {msg}")
                conn.send(databaseData[8].encode(FORMAT))
            else:
                DbClientDatabase = msg
                conn.send("database name received".encode(FORMAT))
                print(f"{DbClientDatabase}")
                
    conn.close()

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