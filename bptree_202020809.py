'''
1. Replace folder name "202212345" with your student ID !!
2. Also, replace this file name "bptree_202212345" with your student ID !
3. Implement operations with "B_PLUS_TREE" class.
4. Run the code "python bptree_202212345.py < test_bp.txt > result.txt" in terminal to test.
'''

import sys


class Node:
    def __init__(self):
        # each node can have |order - 1| keys
        self.keys = []

        # |order| / 2 <= # of subTree pointers <= |order|
        self.subTrees = []

        self.parent = None
        self.isLeaf = False

        # leaf node has next node pointer
        self.nextNode = None
        self.values = []


class B_PLUS_TREE:
    '''
    Implement below functions
    '''

    def __init__(self, order):
        self.order = order
        self.root = Node()
        self.root.isLeaf = True
        pass

    def insert(self, k):
        leaf = self.root
        while leaf.isLeaf == False:
            next = -1
            for idx, value in enumerate(leaf.keys):
                if k < value:
                    next = idx
                    break
                if idx == len(leaf.keys)-1:
                    next = idx
            leaf = leaf.subTrees[next]
        leaf.values.append(k)
        leaf.values.sort()
        if len(leaf.values) >= self.order:
            mid = self.order//2
            leftnode = Node()
            leftnode.isLeaf = True
            leftnode.values = leaf.values[:mid]
            rightnode = Node()
            rightnode.isLeaf = True
            rightnode.values = leaf.values[mid:]
            leftnode.nextNode = rightnode
            rightnode.nextNode = leaf.nextNode
            tempkey = leaf.values[mid]
            parent = leaf.parent
            if parent is None:
                parent = Node()
            parent.keys.append(tempkey)
            parent.keys.sort()
            tempkeyidx = parent.keys.index(tempkey)
            parent.subTrees.insert(tempkeyidx, leftnode)
            parent.subTrees.insert(tempkeyidx+1, rightnode)
            while len(parent.keys) >= self.order:
                leftparent = Node()
                leftparent.keys = parent.keys[:mid]
                rightparent = Node()
                rightparent.keys = parent.keys[mid+1:]
                leftparent.subTrees = parent.subTrees[:mid+1]
                rightparent.subTrees = parent.subTrees[mid+1:]
                midkey = parent.keys[mid]
                parent = parent.parent
                if parent is None:
                    parent = Node()
                parent.keys.append(midkey)
                parent.keys.sort()
                midkeyidx = parent.keys.index(midkey)
                parent.subTrees.insert(midkeyidx, leftparent)
                parent.subTrees.insert(midkeyidx+1, rightparent)
                leftparent.parent = parent
                rightparent.parent = parent
            self.root = parent

    def delete(self, k):
        leafnode = self.root
        chk = 0
        leftsibling = None
        rightsibling = None
        parentidx = -1
        while leafnode.isLeaf == False:
            for idx, key in enumerate(leafnode.keys):
                if idx > 0:
                    leftsibling = leafnode.subTrees[idx-1]
                if idx < len(leafnode.subTrees)-1:
                    rightsibling = leafnode.subTrees[idx+1]
                parentidx = idx
                if k < key:
                    leafnode = leafnode.subTrees[idx]
                    break
                if k == key:
                    chk = 1
                if idx == len(leafnode.keys)-1:
                    leafnode = leafnode.subTrees[idx+1]
        if k not in leafnode.values:
            return
        leafnode.values.remove(k)
        minimum = self.order//2
        if len(leafnode.values) < minimum:
            if leafnode.parent is None:
                if not leafnode.values:
                    self.root = None
                return

            if leftsibling is not None and len(leftsibling.values) > minimum:

            elif rightsibling is not None and len(rightsibling.values) > minimum:

            elif leftsibling is not None:

            elif rightsibling is not None:

    def print_root(self):
        l = "["
        for k in self.root.keys:
            l += "{},".format(k)
        l = l[:-1] + "]"
        print(l)
        pass

    def print_tree(self):

        pass

    def find_range(self, k_from, k_to):
        pass

    def find(self, k):
        pass


def main():
    '''
    Input: test_bp.txt
    Output: result.txt
    '''
    sys.stdin = open("test_bp.txt", 'r')
    sys.stdout = open("result.txt", "w")
    myTree = None

    while (True):
        comm = sys.stdin.readline()
        comm = comm.replace("\n", "")
        params = comm.split()
        if len(params) < 1:
            continue

        print(comm)

        if params[0] == "INIT":
            order = int(params[1])
            myTree = B_PLUS_TREE(order)

        elif params[0] == "EXIT":
            return

        elif params[0] == "INSERT":
            k = int(params[1])
            myTree.insert(k)

        elif params[0] == "DELETE":
            k = int(params[1])
            myTree.delete(k)

        elif params[0] == "ROOT":
            myTree.print_root()

        elif params[0] == "PRINT":
            myTree.print_tree()

        elif params[0] == "FIND":
            k = int(params[1])
            myTree.find(k)

        elif params[0] == "RANGE":
            k_from = int(params[1])
            k_to = int(params[2])
            myTree.find_range(k_from, k_to)

        elif params[0] == "SEP":
            print("-------------------------")


if __name__ == "__main__":
    main()
