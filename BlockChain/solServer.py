import socket
import threading
from base58 import b58decode, b58encode
from solana.rpc.api import Client
from solana.system_program import TransferParams, transfer
from solana.publickey import PublicKey
from solana.transaction import Transaction
from solana.keypair import Keypair
import spl
import requests
import time
import json

HEADER = 160
PORT = 9317
#SERVER = "0.0.0.0"
SERVER = "127.0.0.1"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!Disconnect"

DBHOST = "68.205.37.3"
DBUSER = "juanzin"
DBPASSWORD = "rionovo123"
DBDATABASE = "JtTech"
DBPORT = "3306"

mainnet_beta_url = "https://api.mainnet-beta.solana.com"

solana_client = Client(mainnet_beta_url)


PRIVATE_KEY = "4N9wYbjLpyF5ZFmVvpLDf6EzGLn8dF8mi6ZMXuKWhkRZw1VukRqEPfJmQtGCj9G9rTme1VsdD7cuKQz3XarGC44Z"

WALLET_ADDRESS = "3sWfSQWw84BWbhhrTv3CuhSzAhkhYTGvyCnECbDgtXxm"

recipient_address = "9Jnk2yBKUspwA9g57JmYzFqQxBZbSFr3WY4YQvnt3Xu9"

encoded_private_key = PRIVATE_KEY
keypair = b58decode(encoded_private_key)

private_key = keypair[:32]
public_key = keypair[32:]

#wallet_address = b58encode(public_key).decode()
#print(wallet_address)

#get wallet balance
def get_wallet_balance(address):
    wallet_balance = solana_client.get_balance(address)['result']['value']
    display_balance = round(wallet_balance*10**(-9), 9)
    print(display_balance)
    return display_balance

def transfer_funds(senderPrivKey, recipient, amount):
    senderPriv = b58decode(senderPrivKey)[:32]
    sender = b58decode(senderPrivKey)[32:]
    amount = float(amount)
    transfer_params = TransferParams(
        from_pubkey = PublicKey(sender),
        to_pubkey = PublicKey(recipient),
        lamports=int(amount*(10**9)),
    )
    sol_transfer = transfer(transfer_params)
    transaction = Transaction().add(sol_transfer)
    transaction_result = solana_client.send_transaction(transaction, Keypair.from_seed(senderPriv))
    print("Transaction Hash: ",transaction_result['result'])
    return transaction_result['result']

def create_wallet():
    keypair = Keypair()
    public_key = keypair.public_key.to_base58().decode()
    private_key = b58encode(keypair.secret_key).decode()
    print(f"Public Key: {public_key}")
    print(f"Private Key: {private_key}")
    return public_key, private_key

# sample to fetch data from create_wallet()
#new_wallet_info = create_wallet()
#new_pubkey = new_wallet_info[0]
#new_private_key = new_wallet_info[1]

#def get_recent_transactions(address):
#    recent_transactions = Transaction().recent_blockhash(address)#['result']
#    print(recent_transactions)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handleClient(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        msg = conn.recv(HEADER).decode(FORMAT)
        if msg:
            #msgLength = int(msgLength)
            #msg = conn.recv(msgLength).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                print(f"[{addr}] Disconnected from the server.")
                connected = False
            else:
                print(f"[{addr}] Sent: {msg}")
                splitmsg = msg.split(',')
                if splitmsg[0] == 'new_wallet':                   
                    new_wallet_info = create_wallet()
                    new_pubkey = new_wallet_info[0]
                    new_private_key = new_wallet_info[1]
                    send_wallet_info = f"new_wallet,{new_pubkey},{new_private_key}"
                    conn.send(str.encode(send_wallet_info))
                elif splitmsg[0] == 'get_balance':
                    conn.send(str.encode(str(get_wallet_balance(splitmsg[1]))))
                elif splitmsg[0] == 'transfer_funds':
                    transfered = transfer_funds(splitmsg[1], splitmsg[2], splitmsg[3])
                    conn.send(str.encode(str(transfered)))
               
    conn.close()

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handleClient, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

print("[STARTING] Server is starting...")
start()
