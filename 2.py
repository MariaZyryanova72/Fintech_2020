from web3.auto import w3
from eth_account.messages import encode_defunct

msg = "Ethereum uses public key cryptography for authentication."
private_key = bytes.fromhex("f56226b5d46a4c3307ab0283932095716ca5f1ba8d88b19f8ccf4227c09a1d9e")
message = encode_defunct(text=msg)
signed_message = w3.eth.account.sign_message(bytes(msg, 'utf-8'), private_key=private_key)
print(signed_message)