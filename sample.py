from web3 import Web3

url = "HTTP://127.0.0.1:7545"

web3 = Web3(Web3.HTTPProvider(url))

from_acc = "0x292435996Ff963D305bbbb479D319B12A062Ed34"
to_acc   = "0x88E30a229347D45731E3aA87213a9cDc3f5FA969"

priv_key = "0xe8fd3d346dc80e2e5437eb13652c39ef781980065ccc8f5859a033c56eebff45"


#Get the nonce to prevent duplicate transactions
nonce = web3.eth.get_transaction_count(from_acc)

#Build the Transaction:
tx = {
    'nonce': nonce,
    'to': to_acc,
    'value': web3.to_wei(0, 'ether'),
    'gas': 2_000_000,
    'gasPrice': web3.to_wei('50', 'gwei')
}

#Sign Transaction
signed_tx = web3.eth.account.sign_transaction(tx, priv_key)
try:
    tx_hash = (web3.eth.send_raw_transaction(signed_tx.rawTransaction))
    print(web3.to_hex(tx_hash))
except ValueError:
    print("Insufficient Funds")


