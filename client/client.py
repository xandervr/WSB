from Crypto.PublicKey import RSA
from hashlib import sha256, sha512
import http.client
import json


class Client:
    def __init__(self):
        self.private_key: RSA.RsaKey
        try:
            fPriv = open('priv.key', 'r')
            self.private_key = RSA.import_key(fPriv.read())
            fPriv.close()
        except Exception:
            keypair = RSA.generate(2048)
            self.private_key = keypair
            fPriv = open('priv.key', 'w')
            fPriv.write(self.private_key.export_key().decode('utf-8'))

    def generateAddress(self):
        return hex(int.from_bytes(sha256(self.private_key.publickey().exportKey()).digest(), byteorder='big'))

    def generateSignature(self, data):
        hash = int.from_bytes(sha512(data).digest(), byteorder='big')
        return hex(pow(hash, self.private_key.d, self.private_key.n))

    def signTransaction(self, receiver: str, amount: float, fee: float, message: str):
        data = f"{self.generateAddress()}{receiver}{amount}{fee}{message}".encode('utf-8')
        signature = self.generateSignature(data)
        tx = {
            'sender': self.generateAddress(),
            'receiver': receiver,
            'amount': amount,
            'fee': fee,
            'message': message,
            'signature': signature,
            'pubkey': hex(self.private_key.n)
        }
        self.sendTransaction(json.dumps(tx))

    def sendTransaction(self, json: bytes):
        try:
            conn = http.client.HTTPConnection('localhost', 8000)
            headers = {'Content-type': 'application/json'}
            conn.request('POST', '/transactions', json, headers)
            response = conn.getresponse()
            print(response.status)
            print(response.read().decode())
            conn.close()
        except Exception as e:
            print(e)


c = Client()
print(c.generateAddress())
c.signTransaction('test', 100, 1, 'Suck a huge dick!!!')
