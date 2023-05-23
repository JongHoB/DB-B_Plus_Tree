import sys


class Node:
    def __init__(self):
        # each node can have |order - 1| keys
        self.keys = []

        # |order| / 2 <= # of subTree pointers <= |order|
        self.subTrees: list(Node) = []

        self.parent: Node = None
        self.isLeaf = False

        # leaf node has next node pointer
        self.nextNode: Node = None
        self.values = []


class B_PLUS_TREE:
    '''
    Implement below functions
    '''

    def __init__(self, order):
        self.order = order
        self.root = None
        pass

    def insert(self, k):
        if self.root is None:
            self.root = Node()
            self.root.isLeaf = True
        leaf = self.root
        while leaf.isLeaf == False:
            next = -1
            for idx, value in enumerate(leaf.keys):
                if k < value:
                    next = idx
                    break
                if idx == len(leaf.keys)-1:
                    next = idx+1
            leaf = leaf.subTrees[next]
        leaf.values.append(k)
        leaf.values.sort()
        if len(leaf.values) >= self.order:
            beforenode: Node = None
            leafidx = leaf.parent.subTrees.index(leaf) if leaf.parent else None
            if leaf.parent and leafidx > 0:
                beforenode = leaf.parent.subTrees[leafidx-1]
            mid = self.order//2
            leftnode = Node()
            leftnode.isLeaf = True
            leftnode.values = leaf.values[:mid]

            rightnode = Node()
            rightnode.isLeaf = True
            rightnode.values = leaf.values[mid:]

            if beforenode:
                beforenode.nextNode = leftnode
            leftnode.nextNode = rightnode
            rightnode.nextNode = leaf.nextNode
            tempkey = leaf.values[mid]
            parent = leaf.parent
            if parent is None:
                parent = Node()
            else:
                parent.subTrees.remove(leaf)
            parent.keys.append(tempkey)
            parent.keys.sort()
            tempkeyidx = parent.keys.index(tempkey)
            leftnode.parent = parent
            rightnode.parent = parent
            parent.subTrees.insert(tempkeyidx, leftnode)
            parent.subTrees.insert(tempkeyidx+1, rightnode)

            while len(parent.keys) >= self.order:
                leftparent = Node()
                leftparent.keys = parent.keys[:mid]
                rightparent = Node()
                rightparent.keys = parent.keys[mid+1:]
                leftparent.subTrees = parent.subTrees[:mid+1]
                for n in leftparent.subTrees:
                    n.parent = leftparent
                rightparent.subTrees = parent.subTrees[mid+1:]
                for n in rightparent.subTrees:
                    n.parent = rightparent
                midkey = parent.keys[mid]
                grandparent = parent.parent
                if grandparent is not None:
                    grandparent.subTrees.remove(parent)
                if grandparent is None:
                    grandparent = Node()
                grandparent.keys.append(midkey)
                grandparent.keys.sort()
                midkeyidx = grandparent.keys.index(midkey)
                grandparent.subTrees.insert(midkeyidx, leftparent)
                grandparent.subTrees.insert(midkeyidx+1, rightparent)
                leftparent.parent = grandparent
                rightparent.parent = grandparent
                parent = grandparent
            while parent is not None:
                node = parent
                parent = parent.parent
            self.root = node

    def delete(self, k):
        leafnode = self.root
        indexnode: Node = None
        indexnodeidx = -1
        leftsibling: Node = None
        rightsibling: Node = None
        parentidx = -1

        while leafnode.isLeaf == False:
            for idx, key in enumerate(leafnode.keys):
                leftsibling = None
                if idx > 0:
                    leftsibling = leafnode.subTrees[idx-1]
                if idx < len(leafnode.subTrees)-1:
                    rightsibling = leafnode.subTrees[idx+1]
                parentidx = idx
                if k < key:
                    leafnode = leafnode.subTrees[idx]
                    break
                if k == key:
                    indexnode = leafnode
                    indexnodeidx = idx
                if idx == len(leafnode.keys)-1:
                    leftsibling = leafnode.subTrees[idx]
                    rightsibling = None
                    leafnode = leafnode.subTrees[idx+1]

        if k not in leafnode.values:
            return
        leafnode.values.remove(k)
        minimum = self.order//2

        if len(leafnode.values) < minimum:
            if leafnode.parent is None:

                if len(leafnode.values) <= 0:

                    self.root = None
                return

            if leftsibling is not None and len(leftsibling.values) > minimum:

                borrowkey = leftsibling.values.pop()
                leafnode.values.insert(0, borrowkey)

                leafnode.parent.keys[parentidx if rightsibling is None else parentidx-1] = borrowkey

            elif rightsibling is not None and len(rightsibling.values) > minimum:

                borrowkey = rightsibling.values.pop(0)
                leafnode.values.append(borrowkey)

                leafnode.parent.keys[parentidx] = rightsibling.values[0]

            elif leftsibling is not None:

                leftsibling.values.extend(leafnode.values)
                leftsibling.nextNode = leafnode.nextNode
                leafnode.parent.keys.pop(
                    parentidx if rightsibling is None else parentidx-1)
                leafnode.parent.subTrees.pop(
                    parentidx + 1 if rightsibling is None else parentidx)
                leafnode = leftsibling
                if not leafnode.parent.keys and not leafnode.parent.parent:

                    self.root = leafnode
                    self.root.isLeaf = True
                    self.root.parent = None

            elif rightsibling is not None:

                leafnode.values.extend(rightsibling.values)
                leafnode.nextNode = rightsibling.nextNode
                leafnode.parent.keys.pop(parentidx)
                leafnode.parent.subTrees.pop(parentidx+1)
                if not leafnode.parent.keys and not leafnode.parent.parent:

                    self.root = leafnode
                    self.root.isLeaf = True
                    self.root.parent = None
            if indexnode is not None and indexnode.keys:
                indexnode.keys[indexnodeidx] = leafnode.values[0]
            self.rebalance(leafnode.parent)
        else:
            if indexnode is not None:

                indexnode.keys[indexnodeidx] = leafnode.values[0]

    def print_root(self):
        if not self.root or (self.root.isLeaf and not self.root.values) or (not self.root.isLeaf and not self.root.keys):
            return
        l = "["
        if self.root.isLeaf == False:
            for k in self.root.keys:
                l += "{},".format(k)
        else:
            for k in self.root.values:
                l += "{},".format(k)
        l = l[:-1] + "]"
        print(l)
        pass

    def print_tree(self):
        node: Node = self.root
        if node is None:
            return
        if node.isLeaf == True:
            self.print_root()
        q: list(Node) = []
        q.append(node)
        while q:
            n: Node = q.pop(0)
            l = "["
            if n.isLeaf == True:
                continue
            else:
                for k in n.keys:
                    l += "{},".format(k)
                l = l[:-1] + "]-"
                for s in n.subTrees:
                    q.append(s)
                    l += "["
                    if s.isLeaf == False:
                        for sk in s.keys:
                            l += "{},".format(sk)
                    else:
                        for sk in s.values:
                            l += "{},".format(sk)
                    l = l[:-1]+"],"
                l = l[:-1]
            print(l)

    def find_range(self, k_from, k_to):
        leaf = self.root
        if not leaf or (leaf.isLeaf and not leaf.values) or (not leaf.isLeaf and not leaf.keys):
            return
        while leaf.isLeaf == False:
            next = -1
            for idx, value in enumerate(leaf.keys):
                if k_from < value:
                    next = idx
                    break
                if idx == len(leaf.keys)-1:
                    next = idx+1
            leaf = leaf.subTrees[next]
        l = ""
        while leaf and leaf.values:
            chk = 0
            for v in leaf.values:
                if v >= k_from and v <= k_to:
                    l += "{},".format(v)
                if v > k_to:
                    chk = 1
                    break
            if chk == 0:
                leaf = leaf.nextNode
            else:
                break
        l = l[:-1]
        print(l)

    def find(self, k):
        leaf = self.root
        if not leaf or (leaf.isLeaf and not leaf.values) or (not leaf.isLeaf and not leaf.keys):
            print("NONE")
            return
        chk = 0
        l = ""
        while leaf.isLeaf == False:
            next = -1
            l += str(leaf.keys).replace(" ", "") + '-'
            for idx, value in enumerate(leaf.keys):
                if k < value:
                    next = idx
                    break
                if idx == len(leaf.keys)-1:
                    next = idx+1
            leaf = leaf.subTrees[next]

        if k in leaf.values:
            chk = 1
            l += str(leaf.values).replace(" ", "")
        if chk:
            print(l)
        else:
            print("NONE")

    def rebalance(self, node: Node):
        if node is None:

            return
        minimum = self.order//2
        if len(node.keys) < minimum:

            if node.parent is None:

                if len(node.keys) <= 0:

                    self.root = None
                return

            parent: Node = node.parent
            nodeidx = parent.subTrees.index(node)
            parentidx = parent.subTrees.index(node)
            chk = 0
            if parentidx > 0:
                parentidx = parentidx-1
                chk = 1
            leftsibling: Node = parent.subTrees[nodeidx -
                                                1] if nodeidx > 0 else None
            rightsibling: Node = parent.subTrees[nodeidx +
                                                 1] if nodeidx < len(parent.subTrees)-1 else None

            if leftsibling is not None and len(leftsibling.keys) > minimum:

                tempkey = leftsibling.keys.pop()
                borrowsubTree = leftsibling.subTrees.pop()
                node.keys.insert(0, parent.keys[parentidx-1])
                node.subTrees.insert(0, borrowsubTree)
                borrowsubTree.parent = node
                parent.keys[parentidx-1] = tempkey
            elif rightsibling is not None and len(rightsibling.keys) > minimum:

                tempkey = rightsibling.keys.pop(0)
                borrowsubTree = rightsibling.subTrees.pop(0)
                node.keys.append(parent.keys[parentidx])
                node.subTrees.append(borrowsubTree)
                borrowsubTree.parent = node
                parent.keys[parentidx] = tempkey
            elif leftsibling is not None:

                leftsibling.keys.append(parent.keys[parentidx])
                leftsibling.keys.extend(node.keys)
                leftsibling.subTrees.extend(node.subTrees)
                for n in node.subTrees:
                    n.parent = leftsibling
                parent.keys.pop(parentidx)
                parent.subTrees.pop(parentidx+1)
                node = leftsibling
            elif rightsibling is not None:

                node.keys.append(parent.keys[parentidx])
                node.keys.extend(rightsibling.keys)
                node.subTrees.extend(rightsibling.subTrees)
                for n in rightsibling.subTrees:
                    n.parent = node
                parent.keys.pop(parentidx)
                parent.subTrees.pop(parentidx+1)
            if not parent.keys:

                node.parent = None
                parent = node
                self.root = node
            self.rebalance(parent)


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
