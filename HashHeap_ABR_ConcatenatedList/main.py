# Hash heap
class NodeHeap:
    def __init__(self, k, v):
        self.key = k
        self.value = v

class HashHeap:
    def __init__(self, size):
        self.heap = []
        self.size = size
        self.hash_table = [LinkedList] * size
        for i in range(size):
            self.hash[i] = LinkedList()

    def hash(self, k):
        # È stato scelto A = (sqrt(5) -1)/2 secondo Knuth
        A = 0.61803398875
        key = int(self.size * ((k * A) % 1))
        return key


    def max_heapify(self, i):
        l = self.left(i)
        r = self.right(i)
        max = i

        if l <= self.size and self.heap[l].value > self.heap[i].value:
            max = l

        if r <= self.size and self.heap[r].value > self.heap[max].value:
            max = r

        if max != i:
            self.swap(max, i)
            self.max_heapify(max)

    def min_heapify(self, i):
        l = self.left(i)
        r = self.right(i)
        min = i

        if l <= self.size and self.heap[l].value < self.heap[i].value:
            min = l

        if r <= self.size and self.heap[r].value < self.heap[min].value:
            min = r

        if min != i:
            self.swap(min, i)
            self.max_heapify(min)

    def insert(self, k, v):
        index = self.hash(k)
        if self.hash_table[index].search(k) is not None:
            return
        x = NodeHeap(k, v)
        self.heap.append(x)
        self.hash_table[index].insert(k, len(self.heap) - 1)
        self.max_heapify(len(self.heap) - 1)

    def swap(self, i, j):
        #scambia gli indici
        k1 = self.heap[i].key
        index1 = self.hash(k1)
        element1 = self.hash_table[index1].search(k1)
        element1.index = j

        k2 = self.heap[j].key
        index2 = self.hash(k2)
        element2 = self.hash_table[index2].search(k2)
        element2.index = j

        #scambia i valori nell heap
        self.heap[i], self.heap[j] = self.heap[j] = self.heap[i]








    def parent(self, i):
        return (i - 1)//2

    def left(self, i):
        return i*2 + 1

    def right(self, i):
        return i*2 + 2












# Lista concatenata
class NodeLinkedList:
    def __init__(self, init_data):
        self.data = init_data
        self.next = None

    def get_data(self):
        return self.data

    def get_next(self):
        return self.next

    def set_data(self, new_data):
        self.data = new_data

    def set_next(self, new_next):
        self.next = new_next


class LinkedList:
    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head == None

    def add(self, item):
        temp = NodeLinkedList(item)
        temp.set_next(self.head)
        self.head = temp

    def size(self):
        current = self.head
        count = 0
        while current != None:
            count = count + 1
            current = current.get_next()
        return count

    # Cerchiamo  elementi e stampiamo la lista
    def search(self, item):
        current = self.head
        found = False
        while current != None and not found:
            if current.get_data() == item:
                found = True
            else:
                current = current.get_next()
        return found

    def PrintL(self):
        current = self.head
        previous = None
        while current != None:
            print('..', current.get_data())
            current = current.get_next()

    # cancelliamo elemento

    def remove(self, item):
        current = self.head
        previous = None
        found = False
        while not found:
            if current.get_data() == item:
                found = True
            else:
                previous = current
                current = current.get_next()
        if previous == None:
            self.head = current.get_next()
        else:
            previous.set_next(current.get_next())

# Albero binario di ricerca
class NodeABR:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

    def get(self):
        return self.key

    def set(self, key):
        self.key = key

    def getChildren(self):
        children = []
        if (self.left != None):
            children.append(self.left)
        if (self.right != None):
            children.append(self.right)
        return children


class ABR:
    def __init__(self):
        self.root = None

    def setRoot(self, key):
        self.root = NodeABR(key)

    def insert(self, key):
        if (self.root is None):
            self.setRoot(key)
        else:
            self.insertNode(self.root, key)

    def insertNode(self, currentNode, key):
        if (key <= currentNode.key):
            if (currentNode.left):
                self.insertNode(currentNode.left, key)
            else:
                currentNode.left = NodeABR(key)
        elif (key > currentNode.key):
            if (currentNode.right):
                self.insertNode(currentNode.right, key)
            else:
                currentNode.right = NodeABR(key)

    def find(self, key):
        return self.findNode(self.root, key)

    def findNode(self, currentNode, key):
        if (currentNode is None):
            return False
        elif (key == currentNode.key):
            return True
        elif (key < currentNode.key):
            return self.findNode(currentNode.left, key)
        else:
            return self.findNode(currentNode.right, key)

    def inorder(self):
        def _inorder(v):
            if (v is None):
                return
            if (v.left is not None):
                _inorder(v.left)
            print(v.key)
            if (v.right is not None):
                _inorder(v.right)

        _inorder(self.root)
