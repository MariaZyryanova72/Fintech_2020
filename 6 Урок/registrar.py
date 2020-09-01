import argparse
import json

from web3 import Web3, HTTPProvider
from solcx import compile_source


def compile_source_file(file_path):
    with open(file_path, 'r') as f:
        source = f.read()
    return compile_source(source)


def deploy_contract(w3, contract_interface):
    tx_hash = w3.eth.contract(
        abi=contract_interface['abi'],
        bytecode=contract_interface['bin']).constructor().transact()

    address = w3.eth.getTransactionReceipt(tx_hash)['contractAddress']
    return address


parser = argparse.ArgumentParser()
parser.add_argument("--deploy", action="store_true")
args = parser.parse_args()

w3 = Web3(HTTPProvider("https://sokol.poa.network"))
args.deploy = True

if args.deploy:

    contract_source_path = 'contract.sol'
    compiled_sol = compile_source_file('contract.sol')

    contract_id, contract_interface = compiled_sol.popitem()

    address = deploy_contract(w3, contract_interface)
    store_var_contract = w3.eth.contract(address=address, abi=contract_interface["abi"])

    gas_estimate = store_var_contract.functions.setVar(255).estimateGas()

    if gas_estimate < 100000:
        tx_hash = store_var_contract.functions.setVar(255).transact()
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        print("Transaction receipt mined:")
        print(dict(receipt))
        print("\nWas transaction successful?")
        print(receipt["status"])
    else:
        print("Gas cost exceeds 100000")

