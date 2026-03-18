from web3 import Web3
import json
import os

# -----------------------------------------------
# Connect to Ganache
# -----------------------------------------------
GANACHE_URL = "http://127.0.0.1:7545"
w3 = Web3(Web3.HTTPProvider(GANACHE_URL))

# Check connection
if w3.is_connected():
    print("✅ Connected to Ganache blockchain")
else:
    print("❌ Connection failed — is Ganache running?")

# -----------------------------------------------
# Load contract ABI and address
# -----------------------------------------------

# ABI = Application Binary Interface
# It tells Python HOW to talk to your smart contract
# Truffle generates this automatically when you compile

ABI_PATH = os.path.join("build", "contracts", "RentalAgreement.json")

with open(ABI_PATH) as f:
    contract_json = json.load(f)
    CONTRACT_ABI = contract_json["abi"]

# Paste your contract address from Step 13 here
CONTRACT_ADDRESS = "0x9B62d692B241c475751C6c5f13e9eC83b26D04A3"

# Create contract instance
contract = w3.eth.contract(
    address=CONTRACT_ADDRESS,
    abi=CONTRACT_ABI
)

# Use first Ganache account as the sender
DEFAULT_ACCOUNT = w3.eth.accounts[0]

# -----------------------------------------------
# FUNCTION: Store agreement hash on blockchain
# -----------------------------------------------
def store_agreement(agreement_hash, landlord_name, 
                    tenant_name, property_address, rent_amount):
    try:
        tx_hash = contract.functions.storeAgreement(
            agreement_hash,
            landlord_name,
            tenant_name,
            property_address,
            int(rent_amount)
        ).transact({'from': DEFAULT_ACCOUNT})

        # Wait for transaction to be mined
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        
        # Get the agreement ID (total count after storing)
        agreement_id = contract.functions.getTotalAgreements().call()
        
        return {
            'success': True,
            'agreement_id': agreement_id,
            'transaction_hash': receipt['transactionHash'].hex(),
            'block_number': receipt['blockNumber']
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}


# -----------------------------------------------
# FUNCTION: Get agreement from blockchain
# -----------------------------------------------
def get_agreement(agreement_id):
    try:
        result = contract.functions.getAgreement(
            int(agreement_id)
        ).call()
        
        return {
            'success': True,
            'agreement_id': result[0],
            'hash': result[1],
            'landlord': result[2],
            'tenant': result[3],
            'property': result[4],
            'rent': result[5],
            'timestamp': result[6],
            'is_active': result[7]
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}


# -----------------------------------------------
# FUNCTION: Verify agreement on blockchain
# -----------------------------------------------
def verify_on_blockchain(agreement_id, hash_to_verify):
    try:
        is_authentic = contract.functions.verifyAgreement(
            int(agreement_id),
            hash_to_verify
        ).transact({'from': DEFAULT_ACCOUNT})

        # Get stored agreement to compare
        stored = get_agreement(agreement_id)
        
        if stored['success']:
            is_match = stored['hash'] == hash_to_verify
            return {
                'success': True,
                'is_authentic': is_match,
                'stored_hash': stored['hash'],
                'provided_hash': hash_to_verify
            }
    except Exception as e:
        return {'success': False, 'error': str(e)}