# importing necessary items
import os
import subprocess
import json

from bit import PrivateKeyTestnet
from bit.network import NetworkAPI
from constants import *
from dotenv import load_dotenv
from eth_account import Account
from web3 import Web3



w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

#calling mnemonic in .env file
load_dotenv()
mnemonic = os.getenv('MNEMONIC')


#deriving wallet
def derive_wallets(coin=BTC, mnemonic=mnemonic, depth=3):
    p = subprocess.Popen(f"./derive -g --mnemonic='{mnemonic}' --coin={coin} --numderive={depth} --format=json",
        stdout=subprocess.PIPE, shell=True)
    (out, err) = p.communicate()
    #commented out code that kept giving error
    # p_status = p.wait()
    return json.loads(out)


# setting private key
def priv_key_account(coin, priv_key):
    if coin == ETH:
        return Account.privateKeyToAccount(priv_key)
    if coin == BTCTEST:
        return PrivateKeyTestnet(priv_key)

#setting up transaction requirements
def create_tx(coin, account, recipient, amount):
    if coin ==ETH:
        gasEstimate = w3.eth.estimateGas(
            {"from": account.address, "to": recipient, "value": amount}
        )
        tx_data = {
            "to": recipient,
            "from": account.address,
            "value": amount,
            "gasPrice": w3.eth.gasPrice,
            "gas": gasEstimate,
            "nonce": w3.eth.getTransactionCount(account.address)
        }
        return tx_data
    if coin == BTCTEST:
        return PrivateKeyTestnet.prepare_transaction(account.address, [(recipient, amount, BTC)])

#sending transation
def send_tx(coin,account, recipient, amount):
    raw_tx = create_tx(coin,account,recipient,amount)
    signed_tx = account.sign_transaction(raw_tx)
    if coin == ETH:
        result = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        return result.hex()
    elif coin == BTCTEST:
        return NetworkAPI.broadcast_tx_testnet(signed_tx)

# completing BTCTEST transaction

btc_acc = priv_key_account(BTCTEST, priv_key='cPATqqavHDLmsLX2Ej7SR5gvF3u9QJHLAC7taSQEcSuYucC6NGnG')
create_tx(BTCTEST,btc_acc,"mmPmSpyY8JFvr6JPF1xv4Xae5k7GwXvouS", 0.000001)
send_tx(BTCTEST, btc_acc, 'mfkGhz6m2tMwETDU6sgEHY2gp2qcuHaioH', 0.000001)