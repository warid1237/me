import random
import time
import codecs
import ecdsa
from Crypto.Hash import keccak
from web3 import Web3

def get_address_balance(web3, address):
    """Fetch balance of an Ethereum address using Alchemy."""
    # Convert to checksum address
    checksum_address = web3.to_checksum_address(address)
    balance = web3.eth.get_balance(checksum_address)
    # Convert balance from Wei to Ether
    return web3.from_wei(balance, 'ether')

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

# Define the range
min_value = 1
max_value = 904625697166532776746648320380374280100293470930272690489102837043110636675

start_time = time.time()
for _ in range(1):
    print(_)
    P_random_number = random.randint(min_value, max_value)
    
    End_value = P_random_number * 128
    start_value = End_value - 128
    
    print(start_value)
    print(End_value)
    
    while start_value <= End_value:
        private_key = hex(start_value)[2:]
        private_key = private_key.zfill(64)
        print(private_key)
        ethereum_address = (PK_TO_W(private_key))
        print(ethereum_address)
        balance = get_address_balance(web3, ethereum_address)
        start_value += 1
        if balance > 0.00001:
            print('\n')
            print(private_key)
            print(ethereum_address)
            print(balance)
            print("-" * 40)
            break
        else:
            print('EMPTY')


print('\n')
end_time = time.time()
runtime = end_time - start_time
print(f"Script runtime: {runtime} seconds")