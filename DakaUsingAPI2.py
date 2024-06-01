from web3 import Web3
from mnemonic import Mnemonic
from eth_account import Account
from bip32utils import BIP32Key
import codecs
import ecdsa
from Crypto.Hash import keccak
import random
import os
from PIL import Image
import numpy as np
import time

Account.enable_unaudited_hdwallet_features()
mnemo = Mnemonic("english")
def generate_mnemonic():
    mnemo = Mnemonic("english")
    words = mnemo.generate(strength=128)  # 128 bits for 12 words, 256 for 24 words
    return words

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

print("*" * 70)
print('OK')
print("*" * 70)
start_time = time.time()
for _ in range(1000):
    print("Index:", _)
    seed_phrase = generate_mnemonic()
    # print("Mnemonic:", seed_phrase)
    seed_bytes = mnemo.to_seed(seed_phrase)
    master_key = BIP32Key.fromEntropy(seed_bytes)
    ethereum_key = master_key.ChildKey(44 + 2**31).ChildKey(60 + 2**31).ChildKey(0 + 2**31).ChildKey(0).ChildKey(0)
    private_key = ethereum_key.PrivateKey().hex()
    private_key = private_key.zfill(64)
    # print(private_key)
    ethereum_address = (PK_TO_W(private_key))
    balance = get_address_balance(web3, ethereum_address)
    if balance > 0.000001:
        print('\n')
        print(private_key)
        print(ethereum_address)
        print(balance)
        print("-" * 40)
        break
    else:
        print(balance)


print('\n')
end_time = time.time()
runtime = end_time - start_time
print(f"Script runtime: {runtime} seconds")