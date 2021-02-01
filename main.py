from core.core import Core
from api.server import Server

if __name__ == "__main__":
    WSBChain = Core()
    WSBChain.loadParams()
    WSBChain.loadChain()
    WSBChain.loadTxPool()

    server = Server(WSBChain)
    server.run(8000)
