
from core.models.transaction import transactionFromJSON
from core.consts import BLOCK_REWARD, CHAIN_VERSION, MAX_BLOCK_SIZE, TARGET_DIFF
from core.core import Core
import flask
import json
from core.encoders.blockencoder import BlockEncoder


class Server:
    def __init__(self, chain: Core):
        self.chain = chain

    def run(self, port: int):
        app = flask.Flask(__name__)
        app.config["DEBUG"] = True

        @app.route('/info', methods=['GET'])
        def info():
            lastBlock = self.chain.chain.getLast()
            hash = ""
            if lastBlock is not None:
                hash = lastBlock.value.getHash()

            response = flask.make_response(json.dumps({
                "version": CHAIN_VERSION,
                "previous_hash": hash,
                "difficulty": TARGET_DIFF,
                "block_size": MAX_BLOCK_SIZE,
                "block_reward": BLOCK_REWARD,
                "network_hash_rate": self.chain.calculateNetworkHashrate()
            }))
            response.headers["Content-Type"] = "application/json"
            return response

        @app.route('/transactions', methods=['GET'])
        def transactions():
            response = flask.make_response(json.dumps(
                list(map(lambda x: x.__dict__, self.chain.transaction_pool.transactions))))
            response.headers["Content-Type"] = "application/json"
            return response

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
                response = flask.make_response(json.dumps(tx.__dict__))
                response.headers["Content-Type"] = "application/json"
                return response
            else:
                return '', 403

        @app.route('/blocks', methods=['GET'])
        def block():
            response = flask.make_response(json.dumps(self.chain.toList(), cls=BlockEncoder))
            response.headers["Content-Type"] = "application/json"
            return response

        @app.route('/blocks', methods=['POST'])
        def addBlock():
            data = flask.request.data.decode('utf-8')
            block_json = json.loads(data)
            transactions: list = block_json['transactions']
            nonce = block_json['nonce']
            timestamp = block_json['timestamp']
            legitTransactions = []
            if len(transactions) > 0:
                coinbaseTransaction = transactions[0]
                transactions.remove(coinbaseTransaction)
                coinbaseTransaction = transactionFromJSON(coinbaseTransaction)
                legitTransactions.append(coinbaseTransaction)
                for i in range(len(transactions)):
                    tx = self.chain.transaction_pool.getTransaction(transactions[i]['signature'])
                    if tx is not None:
                        legitTransactions.append(tx)

            block = self.chain.addBlock(legitTransactions, nonce, timestamp)
            if block is None:
                return "", 403
            else:
                response = flask.make_response(json.dumps(block, cls=BlockEncoder))
                response.headers["Content-Type"] = "application/json"
                return response

        app.run("0.0.0.0", port)
