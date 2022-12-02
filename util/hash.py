from hashlib import sha256

def gen_hash(*args):
    text = f'{args}'
    return int(sha256(text.encode('utf-8')).hexdigest(), base=16)
