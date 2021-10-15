import hashlib
import random

THRESHOLD = '0'


def proof_of_work(block):
    '''calculate proof of work of a temp block'''
    nonce = random.randint(2, 100)
    adder = random.randint(2, 100)
    n = len(THRESHOLD)
    while True:
        hash_str = str(block.header['prev_hash']) + str(block.header['mkl_root']) + str(nonce) + str(block.header['timestamp'])
        pow_hash = hashlib.sha256(hash_str.encode()).hexdigest()
        if pow_hash[:n] == THRESHOLD:
            break
        else:
            nonce = nonce + adder
    block.header['nonce'] = nonce
    block.header['block_hash'] = pow_hash

    return


def check_pow(block):
    '''check proof of work of old block'''
    hash_str = str(block.header['prev_hash']) + str(block.header['mkl_root']) + str(block.header['nonce']) + str(
        block.header['timestamp'])
    if block.header['block_hash'] == hashlib.sha256(hash_str.encode()).hexdigest():
        return True
    else:
        return False
