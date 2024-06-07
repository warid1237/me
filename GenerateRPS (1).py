import random
import time
import codecs
import ecdsa
from Crypto.Hash import keccak
from web3 import Web3

def get_address_balance(web3, address):
    """Fetch balance of an Ethereum address using Alchemy."""
    try:
        # Convert to checksum address
        checksum_address = web3.to_checksum_address(address)
        balance = web3.eth.get_balance(checksum_address)
        # Convert balance from Wei to Ether
        return web3.from_wei(balance, 'ether')
    except Exception as e:
        print(f"Error fetching balance for address {address}: {e}")
        return 0

alchemy_api_key = 'SAqD2yn4YlvjkEY1BLNGaKFM0Sj5UNx-'
alchemy_url = f"https://eth-mainnet.g.alchemy.com/v2/{alchemy_api_key}"
web3 = Web3(Web3.HTTPProvider(alchemy_url))
if not web3.is_connected():
    print("Failed to connect to Alchemy")

print("*" * 70)
print('OK')
print("*" * 70)

def PK_TO_W(private_key):
    private_key_bytes = codecs.decode(private_key, 'hex')
    # Get ECDSA public key
    key = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1).verifying_key
    key_bytes = key.to_string()
    key_hex = codecs.encode(key_bytes, 'hex')
    public_key_bytes = codecs.decode(key_hex, 'hex')
    keccak_hash = keccak.new(digest_bits=256)
    keccak_hash.update(public_key_bytes)
    keccak_digest = keccak_hash.hexdigest()
    # Take the last 20 bytes
    wallet_len = 40
    wallet = '0x' + keccak_digest[-wallet_len:]
    return wallet

# Define the range for 2^256
min_value = 1
max_value = 2**256 - 1

num_pages = 5  # Number of random pages to check
addresses_per_page = 128

start_time = time.time()

for _ in range(num_pages):
    P_random_number = random.randint(min_value, max_value // addresses_per_page)
    
    # Print the random page number
    page_number = P_random_number
    print(f"Page number: {page_number}")

    End_value = (P_random_number + 1) * addresses_per_page - 1
    start_value = P_random_number * addresses_per_page
    
    # Print the start and end values in hex
    start_value_hex = hex(start_value)[2:].zfill(64)
    end_value_hex = hex(End_value)[2:].zfill(64)
    
    print(f"\nStart value: {start_value_hex}, \nEnd value: {end_value_hex}")
    
    for value in range(start_value, End_value + 1):
        private_key = hex(value)[2:].zfill(64)  # Ensure the private key is 64 digits long
        ethereum_address = PK_TO_W(private_key)
        balance = get_address_balance(web3, ethereum_address)
        balance_float = float(balance)  # Convert balance to float
        
        if balance_float > 0.00001:
            print('\n')
            print(f"Non-zero balance found!")
            print(f"Private key: {private_key}")
            print(f"Ethereum address: {ethereum_address}")
            print(f"Balance: {balance} Ether")
            print("-" * 40)
            break

print('\n')
end_time = time.time()
runtime = end_time - start_time
print(f"Script runtime: {runtime} seconds")
