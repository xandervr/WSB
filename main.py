from core.core import Core
from core.models.block import Block
from time import time

if __name__ == "__main__":
    WSBChain = Core()

    brecht = WSBChain.generateWallet()
    xander = WSBChain.generateWallet()

    tx = WSBChain.addTransaction(xander, brecht, 100, 1, "Suck a dick!")

    print(tx.signature)
    print(tx)

    # a = Block("01000000", "", "askldfjlsdfjlasdjfasdf", int(time()), 1, 546456, [])
    # b = Block("01000000", a.getHash(), "asdfjhalskdfhasodfihasdf", int(time()), 1, 548, [])
    # c = Block("01000000", b.getHash(), "asdfasdfqwer", int(time()), 1, 7586, [])
    # WSBChain.addBlock(a)
    # WSBChain.addBlock(b)
    # WSBChain.addBlock(c)
    # WSBChain.printChain()
