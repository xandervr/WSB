from Crypto.PublicKey import RSA
from hashlib import sha512


def generateKeyPair():
    return RSA.generate(4096)


def generateSignature(data, keyPair):
    hash = int.from_bytes(sha512(data).digest(), byteorder='big')
    return hex(pow(hash, keyPair.d, keyPair.n))


def verifyKeyPairAndSignature(data, signature, keyPair):
    hash = int.from_bytes(sha512(data).digest(), byteorder='big')
    hashFromSignature = pow(int(signature, 16), keyPair.e, keyPair.n)
    return hash == hashFromSignature


# keyPair = generateKeyPair()
# data = b'Brecht'
# signature = generateSignature(data, keyPair)
# print(signature)

# wrongData = b'Xander'
# correct = verifyKeyPairAndSignature(wrongData, signature, keyPair)

# print(correct)
