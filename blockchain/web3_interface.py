# # blockchain/web3_interface.py

# import os
# from web3 import Web3
# from dotenv import load_dotenv
# import json

# load_dotenv()

# PRIVATE_KEY = os.getenv("PRIVATE_KEY")
# WALLET_ADDRESS = os.getenv("WALLET_ADDRESS")
# RPC_URL = os.getenv("RPC_URL")

# # ✅ Connect to Sepolia or Ganache
# w3 = Web3(Web3.HTTPProvider(RPC_URL))

# # ✅ Load compiled ABI
# with open("blockchain/LoanAgent_abi.json", "r") as f:
#     abi = json.load(f)

# CONTRACT_ADDRESS = "0xYourDeployedContractAddress"
# contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)

# def trigger_loan_contract(borrower: str, amount: int) -> str:
#     nonce = w3.eth.get_transaction_count(WALLET_ADDRESS)

#     txn = contract.functions.approveLoan(borrower, amount).build_transaction({
#         "from": WALLET_ADDRESS,
#         "gas": 200000,
#         "gasPrice": w3.to_wei("10", "gwei"),
#         "nonce": nonce
#     })

#     signed_txn = w3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
#     tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
#     return tx_hash.hex()

# from web3 import Web3
# import json
# import os

# # Load env
# rpc_url = "http://127.0.0.1:8545"
# private_key = "0x41f84dc5ed06eb782e3178ca96cb12e77c4530d153269858071b6f7fcfcd6f86"
# wallet_address = "0xb0F4588216deE8a384f39b4519A9aF3258De7361"

# # Connect to Ganache
# w3 = Web3(Web3.HTTPProvider(rpc_url))

# # Load contract
# with open("blockchain/LoanAgent_abi.json") as f:
#     abi = json.load(f)

# contract_address = "0x218832E5fD62caBcA09839b9eA4Fc81f6f128960"
# contract = w3.eth.contract(address=contract_address, abi=abi)

# def simulate_transaction():
#     nonce = w3.eth.get_transaction_count(wallet_address)
#     txn = contract.functions.someFunction().build_transaction({
#         "from": wallet_address,
#         "nonce": nonce,
#         "gas": 2000000,
#         "gasPrice": w3.to_wei("20", "gwei")
#     })

#     signed_txn = w3.eth.account.sign_transaction(txn, private_key=private_key)
#     tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

#     return tx_hash.hex()

from web3 import Web3
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Load environment variables
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
RPC_URL = os.getenv("RPC_URL")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

if not all([PRIVATE_KEY, RPC_URL, CONTRACT_ADDRESS]):
    raise ValueError("❌ Missing one or more required .env variables (PRIVATE_KEY, RPC_URL, CONTRACT_ADDRESS)")

# Derive the wallet address from private key
account = Web3().eth.account.from_key(PRIVATE_KEY)
WALLET_ADDRESS = account.address

# Connect to Web3
w3 = Web3(Web3.HTTPProvider(RPC_URL))

# Load ABI
with open("blockchain/LoanAgent_abi.json") as f:
    abi = json.load(f)

# Set up contract instance
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)

def simulate_transaction():
    nonce = w3.eth.get_transaction_count(WALLET_ADDRESS)

    txn = contract.functions.approveLoan(
        WALLET_ADDRESS, 5000
    ).build_transaction({
        "from": WALLET_ADDRESS,
        "nonce": nonce,
        "gas": 2000000,
        "gasPrice": w3.to_wei("20", "gwei")
    })

    signed_txn = w3.eth.account.sign_transaction(txn, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)  # <-- FIXED HERE

    return tx_hash.hex()



