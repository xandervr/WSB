class LinkedList:
    def __init__(self):
        self.head = None

    def printList(self):
        if self.head is None:
            return

        def traverse(node):
            print(f"{node.index}: {node.value}")
            if node.next is not None:
                traverse(node.next)
        traverse(self.head)

    def getLast(self):
        if self.head is None:
            return self.head

        def traverse(node):
            if node.next is not None:
                return traverse(node.next)
            else:
                return node
        return traverse(self.head)

    def addNode(self, value):
        lastN = self.getLast()
        if lastN is None:
            n = Node(1, value)
            self.head = n
        else:
            n = Node(lastN.index+1, value)
            lastN.next = n


class Node:
    def __init__(self, index=1, val=None):
        self.index = index
        self.value = val
        self.next = None
