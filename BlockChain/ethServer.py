import socket
import threading
from web3 import Web3
import requests
import time
import json

HEADER = 64
PORT = 9317
SERVER = "0.0.0.0"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!Disconnect"

DBHOST = "68.205.37.3"
DBUSER = "juanzin"
DBPASSWORD = "rionovo123"
DBDATABASE = "JtTech"
DBPORT = "3306"

#infura_url = 'https://mainnet.infura.io/v3/f2bad4da0b61436d990b6d0d7db4007f' # blockchain network
ganache_url = 'http://127.0.0.1:8545' # local network

cryptocompare_url = 'https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD'

#account_address = '0xFF01AF887b018BC8adA5dD12B0a513eF925eC725' # ot main wallet
account_address = '0xa8607A729650bF7062f78c024b04346cC85cc413' # ot ganache main wallet

#private_key = '0d20bb119eeea7ba19bf40f4d541306f4d2a6385a426bd86a644c4bd5e54d5a7' # ot main pvt key
private_key = '59563767e3b33b3a99b0e468e1d3d9e983795393859c4e50bcc54a13a5dc5651' # ot ganache main pvt key

#web3 = Web3(Web3.HTTPProvider(infura_url))
web3 = Web3(Web3.HTTPProvider(ganache_url))
eth_price = requests.get(cryptocompare_url).json()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def ethTransaction(receiver_address, amount):
    # get nonce
    nonce = web3.eth.getTransactionCount(account_address)
    # build transaction
    txn_dict = {
        'to': receiver_address,
        'value': web3.toWei(amount,'ether'),
        'gas': 2000000,
        'gasPrice': web3.toWei('10','gwei'),
        'nonce': nonce
    }
    # sign the transaction
    signed_txn = web3.eth.account.signTransaction(txn_dict, private_key)
    # send the transaction
    result = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    # get the transaction hash
    tx_receipt = web3.eth.getTransactionReceipt(result) 
    while tx_receipt is None:
        time.sleep(1)
        tx_receipt = web3.eth.getTransactionReceipt(result)
    print(f"Transaction Receipt: {tx_receipt}")

try:
    acc_balance_in_eth = web3.fromWei(web3.eth.getBalance(account_address), 'ether')
except:
    print("Error: Account address is unsafe")
    acc_balance_in_eth = web3.fromWei(web3.eth.getBalance(Web3.toChecksumAddress(account_address)), 'ether')


acc_balance_in_usd = eth_price['USD'] * float(acc_balance_in_eth)

print('Web3 Connection: ', web3.isConnected())
print('Web3 Block Number: ', web3.eth.blockNumber)
#while True:
print('Account ETH Balance: ', acc_balance_in_eth)
print('Account USD Balance: ', acc_balance_in_usd)
 #   time.sleep(1)


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
                print(f"message:\nToken: {splitmsg[0]}\nAddress: {splitmsg[1]} \nAmount: {splitmsg[2]}")
                if splitmsg[0] == 'ETH':
                    print('ETH')
                    ethTransaction(splitmsg[1], splitmsg[2])
                elif splitmsg[0] == 'SOL':
                    print('SOL')
                
                try:
                    acc_balance_in_eth = web3.fromWei(web3.eth.getBalance(account_address), 'ether')
                except:
                    print("Error: Account address is unsafe")
                    acc_balance_in_eth = web3.fromWei(web3.eth.getBalance(Web3.toChecksumAddress(account_address)), 'ether')
                acc_balance_in_usd = eth_price['USD'] * float(acc_balance_in_eth)
                
                print('Main Account New ETH Balance: ', acc_balance_in_eth)
                print('Main Account New USD Balance: ', acc_balance_in_usd)
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