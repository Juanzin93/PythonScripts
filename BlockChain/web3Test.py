
from web3 import Web3
import requests
import time
import json

infura_url = 'https://mainnet.infura.io/v3/f2bad4da0b61436d990b6d0d7db4007f'

cryptocompare_url = 'https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD'

account_address = '0xf9504E70A13827dad99EC674f1bb17Ea933b8a57'

private_key = ''

web3 = Web3(Web3.HTTPProvider(infura_url))
eth_price = requests.get(cryptocompare_url).json()

def transaction(receiver_address, amount):
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
    print(tx_receipt)

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
