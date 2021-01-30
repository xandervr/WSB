
from core.core import Core
import flask
import json


class Server:
    def __init__(self, chain: Core):
        self.chain = chain

    def run(self, port: int):
        app = flask.Flask(__name__)
        app.config["DEBUG"] = True

        @app.route('/transactions', methods=['GET'])
        def transactions():
            return json.dumps(list(map(lambda x: x.__dict__, self.chain.transaction_pool.transactions)))

        @app.route('/transactions', methods=['POST'])
        def addTransaction():
            data = flask.request.data.decode('utf-8')
            tx_json = json.loads(data)
            print(tx_json)
            sender = tx_json['sender']
            receiver = tx_json['receiver']
            amount = tx_json['amount']
            fee = tx_json['fee']
            message = tx_json['message']
            signature = tx_json['signature']
            pubkey = tx_json['pubkey']
            tx = self.chain.addTransaction(sender, receiver, amount, fee, signature, pubkey, message)
            if tx is not None:
                return json.dumps(tx.__dict__)
            else:
                return '', 403

        @app.route('/blocks', methods=['GET'])
        def block():
            return json.dumps(list(map(lambda x: x.__dict__, self.chain.toList())))

        @app.route('/blocks', methods=['POST'])
        def addBlock():
            data = flask.request.data.decode('utf-8')
            block_json = json.loads(data)
            transactions = block_json['transactions']
            nonce = block_json['nonce']
            legitTransactions = []
            for i in range(len(transactions)):
                tx = self.chain.transaction_pool.getTransaction(transactions[i])
                if tx is not None:
                    legitTransactions.append(tx)
            return self.chain.addBlock(legitTransactions, nonce)

        app.run(None, port)
