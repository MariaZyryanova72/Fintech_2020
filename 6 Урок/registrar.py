from subprocess import check_output
import re
from web3 import Web3
import argparse
from time import sleep
import requests
from json import load, loads, dump
import os

solc_output = check_output(["solc", "--optimize", "--bin", "--abi", "contracts/registrar.sol"]).decode()

registar_contract_bytecode = re.findall("Binary:\\n(.*?)\\n", solc_output)[0]
registar_contract_abi = loads(re.findall("Contract JSON ABI\\n(.*?)\\n", solc_output)[0])

WEB3_URL = "https://sokol.poa.network"
GASPRICE_ORACLE_URL = "https://gasprice.poa.network"

if os.path.isfile("network.json"):
    with open("network.json") as nw:
        nw_cfg = load(nw)
        WEB3_URL = nw_cfg['rpcUrl']
        GASPRICE_ORACLE_URL = nw_cfg['gasPriceUrl']

w3 = Web3(Web3.HTTPProvider(WEB3_URL))


def create_parser():
    parser = argparse.ArgumentParser(
        description='Solution to registrar assignment'
    )

    parser.add_argument(
        '--deploy', required=False, action='store_true',
        help='Deploy a contract'
    )

    parser.add_argument(
        '--add', type=str, required=False, metavar='JSON',
        help='Creates connection with yor name and address'
    )

    parser.add_argument(
        '--del', required=False, action='store_true',
        help='Deletes connection with yor name and address'
    )

    parser.add_argument(
        '--getacc', type=str, required=False,
        help='Gets mapping of address to name'
    )

    parser.add_argument(
        '--getname', type=str, required=False,
        help='Get mapping of name to address'
    )

    parser.add_argument(
        '--list', required=False, action='store_true',
        help='Get list of all connections'
    )

    return parser


parser = create_parser()
args = parser.parse_args()


def load_acc():
    with open("account.json") as ac:
        priv_key = load(ac)
    return w3.eth.account.privateKeyToAccount(priv_key['account'])


def get_fast_price():
    resp = requests.get(GASPRICE_ORACLE_URL)
    return loads(resp.text)['fast']


def get_contract():
    with open("database.json") as database:
        contract_address = load(database)["registrar"]
    contract = w3.eth.contract(address=contract_address, abi=registar_contract_abi)
    return contract


def deploy():
    contract = w3.eth.contract(abi=registar_contract_abi, bytecode=registar_contract_bytecode)

    construct_txn = contract.constructor().buildTransaction({
        'from': account.address,
        'nonce': w3.eth.getTransactionCount(account.address),
        'gas': 4 * 10 ** 6,
        'gasPrice': int(get_fast_price() * w3.toWei('1', 'gwei'))})

    signed = account.signTransaction(construct_txn)
    txHash = w3.eth.sendRawTransaction(signed.rawTransaction)
    w3.eth.waitForTransactionReceipt(txHash)
    txn_receipt = w3.eth.getTransactionReceipt(txHash)
    contract_address = txn_receipt['contractAddress']
    block = txn_receipt['blockNumber']
    print('Contract address: ' + contract_address)
    with open('database.json', 'w') as file:
        dump({"registrar": contract_address, "startBlock": block}, file)


def add_name(name):
    contract = get_contract()

    if contract.functions.getName(account.address).call() != "":
        print("One account must correspond one name")
        return

    raw_tx = contract.functions.registerName(name).buildTransaction({
        'from': account.address,
        'nonce': w3.eth.getTransactionCount(account.address),
        'gas': 4 * 10 ** 6,
        'gasPrice': int(get_fast_price() * w3.toWei('1', 'gwei'))})

    signed = account.signTransaction(raw_tx)
    try:
        txHash = w3.eth.sendRawTransaction(signed.rawTransaction)
        print("Successfully added by", txHash.hex())
    except:
        print("No enough funds to add name")


def get_name():
    contract = get_contract()
    print(contract.functions.getName(account.address).call())


def get_list():
    contract = get_contract()
    with open("database.json") as database:
        fromBlock = load(database)["startBlock"]

    filter_on_reg = contract.events.NameRegistered.build_filter()
    filter_on_reg.fromBlock = fromBlock
    filter_on_reg = filter_on_reg.deploy(w3)
    filter_on_del = contract.events.NameUnregistered.build_filter()
    filter_on_del.fromBlock = fromBlock
    filter_on_del = filter_on_del.deploy(w3)
    event_list_on_reg = filter_on_reg.get_all_entries()
    event_list_on_del = filter_on_del.get_all_entries()
    events = []
    for event in event_list_on_reg:
        event_args = event['args']
        address, name, block = event_args['_address'], event_args['_name'], event['blockNumber']
        events.append((address, name, block))

    for event in event_list_on_del:
        event_args = event['args']
        address, block = event_args['_address'], event['blockNumber']
        events.append((address, block))

    events.sort(key=lambda x: x[-1])
    pairs = {}
    for event in events:
        if len(event) == 3:
            pairs[event[0]] = event[1]
        else:
            del pairs[event[0]]

    for pair in pairs:
        print(f'"{pairs[pair]}": {pair}')


def remove_name_and_address():
    contract = get_contract()
    name = contract.functions.getName(account.address).call()
    if name == "":
        print("No name found for your account")
        return

    raw_tx = contract.functions.unregisterName().buildTransaction({
        'from': account.address,
        'nonce': w3.eth.getTransactionCount(account.address),
        'gas': 4 * 10 ** 6,
        'gasPrice': int(get_fast_price() * w3.toWei('1', 'gwei'))})

    signed = account.signTransaction(raw_tx)
    try:
        txHash = w3.eth.sendRawTransaction(signed.rawTransaction)
        print("Successfully deleted by", txHash.hex())
    except:
        print("No enough funds to delete name")


def get_addresses_by_name(name):
    contract = get_contract()
    array = contract.functions.getAddresses(name).call()
    if len(array) == 0:
        print("No account registered for this name")
        return
    if len(array) == 1:
        print("Registered account is", array[0])
        return
    print("Registered accounts are:")
    for address in array:
        print(address)


def get_name_by_address(address):
    contract = get_contract()
    name = contract.functions.getName(address).call()
    if name == "":
        print("No name registered for this account")
    else:
        print("Registered account is \"{}\"".format(name))


account = load_acc()

if args.deploy:
    deploy()

if args.add:
    add_name(args.add)

if vars(args)['del']:
    remove_name_and_address()

if args.list:
    get_list()

if args.getacc:
    get_addresses_by_name(args.getacc)

if args.getname:
    get_name_by_address(args.getname)