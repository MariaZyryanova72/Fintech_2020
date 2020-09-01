from eth_account import Account
from web3 import Web3, HTTPProvider
import time
acct = Account.privateKeyToAccount('8342d4b7ff2f57cd41bb866da3135934bddfafd9adc6f0a68112006b6cf80d4a')
"""
tx = { 'to': '0xBF3d6f830CE263CAE987193982192Cd990442B53',
       'value': 100000000000000,
       'gas': 21000,
       'gasPrice': 1000000000,
       'nonce': 1}
singed_tx = acct.signTransaction(tx)
print(singed_tx.rawTransaction)"""

w3 = Web3(HTTPProvider("https://sokol.poa.network"))
tx = {'to': '0x3f970A90cA5a71Eb84277030b941dD31795b019b',
      'value': 2000000000000000000,
      'gas': 21000,
      'gasPrice': Web3.toWei(10, "gwei"),
      'nonce': w3.eth.getTransactionCount(acct.address)}
singed_tx = acct.signTransaction(tx)
print(singed_tx.rawTransaction)
txhash = w3.eth.sendRawTransaction(singed_tx.rawTransaction)
print(txhash)
time.sleep(5)
print(w3.eth.getTransactionReceipt(txhash))
print(w3.eth.getTransactionReceipt(txhash).status)