from hashlib import sha256

def gen_hash(*args):
    # SHA-256 hash function
    text = f'{args}'
    return int(sha256(text.encode('utf-8')).hexdigest(), base=16)
