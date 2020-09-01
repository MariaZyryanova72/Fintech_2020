import argparse
from eth_account import Account
from web3 import Web3, HTTPProvider
from web3.exceptions import TransactionNotFound

parser = argparse.ArgumentParser()
parser.add_argument("--key")
parser.add_argument("--to")
parser.add_argument("--value", type=int)
parser.add_argument("--tx")
args = parser.parse_args()

w3 = Web3(HTTPProvider("https://sokol.poa.network"))

if args.key and not (args.to and args.value):
    acct = Account.privateKeyToAccount(args.key)
    print(f"Balance on '{acct.address}' is {w3.fromWei(w3.eth.getBalance(acct.address), 'ether')}")

if args.key and args.to and args.value:
    acct = Account.privateKeyToAccount(args.key)
    tx = {'to': '0xBF3d6f830CE263CAE987193982192Cd990442B53',
          'value': args.value,
          'gas': 21000,
          'gasPrice': 1000000000,
          'nonce': w3.eth.getTransactionCount(acct.address)}

    if w3.eth.getBalance(acct.address) - 21000 * 1000000000 - args.value > 0:
        singed_tx = acct.signTransaction(tx)
        print(f"Payment of {w3.fromWei(args.value, 'ether')} poa to '{args.to}'"
              f" scheduled\nTransaction Hash: {singed_tx.rawTransaction.hex()}")
    else:
        print("No enough funds for payment")

if args.tx:
    try:
        transaction = w3.eth.getTransaction(args.tx)
        print(f"Payment of {w3.fromWei(transaction['value'], 'ether')} roa to '{transaction['to']}' confirmed")
    except TransactionNotFound:
        print("No such transaction in the chain")
