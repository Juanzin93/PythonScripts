
import socket

HEADER = 160
PORT = 9315
SERVER = "68.205.37.3"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!Disconnect"

walletData = []
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
        new_wallet = from_server.split(",")
        if new_wallet[0] == "new_wallet":
            global walletData
            walletData.append(new_wallet[1])
            walletData.append(new_wallet[2])
            print(walletData)
            walletData = []

send("get_balance,3sWfSQWw84BWbhhrTv3CuhSzAhkhYTGvyCnECbDgtXxm")

send(DISCONNECT_MESSAGE)