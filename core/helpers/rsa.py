from Crypto.PublicKey import RSA
from hashlib import sha512, sha256


def generateKeyPair():
    return RSA.generate(2048)


def generateSignature(data, keyPair):
    hash = int.from_bytes(sha512(data).digest(), byteorder='big')
    return hex(pow(hash, keyPair.d, keyPair.n))


def generateAddress(privkey: int):
    return hex(int.from_bytes(sha256(hex(privkey).encode('utf-8')).digest(), byteorder='big'))


def verifyKeyPairAndSignature(data, signature: str, pubkey: int):
    hash = int.from_bytes(sha512(data).digest(), byteorder='big')
    hashFromSignature = pow(int(signature, 16), 65537, int(pubkey, 16))
    return hash == hashFromSignature


# keyPair = generateKeyPair()
# data = b'Brecht'
# signature = generateSignature(data, keyPair)
# print(signature)

# wrongData = b'Xander'
# correct = verifyKeyPairAndSignature(wrongData, signature, keyPair)

# print(correct)
