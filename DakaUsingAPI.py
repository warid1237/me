from web3 import Web3
import codecs
import ecdsa
from Crypto.Hash import keccak
import random
import os
from PIL import Image
import numpy as np

def split_bytes_into_groups(bytes_data, chunk_size):
    byte_groups = [bytes_data[i:i+chunk_size] for i in range(0, len(bytes_data), chunk_size)]
    return byte_groups

def PK_TO_W(entropy):
  if (len(entropy) == 64):
    private_key = entropy
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





entropies = set()
LN = 115792089237316195423570985008687907852837564279074904382605163141518161494337
CN = 7237005577332262213973186563042994240829374041602535252466099000494570602496

chunk_size = 32
folder_path = "ABC"
files = os.listdir(folder_path)
image_files = [file for file in files if file.endswith(('.png', '.jpg', '.jpeg', '.gif'))]
for image_file in image_files:
    image_path = os.path.join(folder_path, image_file)
    print(image_file)
    img = Image.open(image_path)
    img_array = np.array(img)
    img.close()
    image_bytes = img_array.tobytes()
    byte_groups = split_bytes_into_groups(image_bytes, chunk_size)

print('byte_groups: ', len(byte_groups))

for private_key_bytes in byte_groups:
    integer_value = int.from_bytes(private_key_bytes, byteorder='big')
    if integer_value < LN and integer_value > 1:
        hex_representation = private_key_bytes.hex()
        hex_representation = hex_representation.zfill(64)
        entropies.add(hex_representation)

print('\n')
print('Total Input Entropies: ', len(entropies))
byte_groups = set()

'''
entropies = set()
print('Preparing Entropies...')
for i in range(20):
    random_bits = [random.choice('10') for _ in range(256)]
    random_string = ''.join(random_bits)
    integer_value = int(random_string, 2)
    entropy = hex(integer_value)[2:]
    entropy = entropy.zfill(64)
    entropies.add(entropy)
print(len(entropies))
'''


for index, entropy in enumerate(entropies):
    print("Attempt:", index)
    address = (PK_TO_W(entropy))
    # address = '0x67f706Db3bbD04a250eed049386C5d09c4eE31F0'
    balance = get_address_balance(web3, address)
    if balance > 0.0001:
        print('\n')
        print(f"Address: {address}")
        print(f"Balance: {balance} ETH")
        print("-" * 40)
        break