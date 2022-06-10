
import socket

HEADER = 64
PORT = 9316
SERVER = "68.205.37.3"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!Disconnect"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msgLength = len(message)
    sendLength = str(msgLength).encode(FORMAT)
    sendLength += b' ' * (HEADER - len(sendLength))
    client.send(sendLength)
    client.send(message)
    from_server = client.recv(HEADER).decode(FORMAT)
    if from_server:
        print(f"msg from server: {from_server}")

send("getDatabaseHost")
send("getDatabaseUser")
send("getDatabasePassword")
send("getDatabaseTable")
send("getDatabasePort")
send(DISCONNECT_MESSAGE)