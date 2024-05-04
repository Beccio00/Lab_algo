# Hash heap
class HashMapListNode:
    def __init__(self, key, value, next = None):
        self.key = key
        self.value = value #rappresenta la posizione dell'elemento nell'heap
        self.next = next

class HashHeap:
    def __int__(self, size):
        self.hash_map = [None] * size
        self.heap = []

    def _hash(self, key):
        #scelgo A come secondo Knuth
        A = 0.61803398875
        hash_key = int(self.table_size*((key * A) % 1))
        return hash_key

    def insert(self, key, value):
        hash_index = self._hash(key)
        #creo un nodo dell'hash map che è formato dalla chiave,
        #la lunghezza dell'heap dato che value rappresenta, il next il nodo corrente
        #perciò ci possono essere collisioni
        node = HashMapListNode(key, len(self.heap), self.hash_map[hash_index])
        self.hash_map[hash_index] = node
        self.heap.append(value)
        self.max_heapify(len(self.heap) - 1)

    def delete(self, key):
        hash_index = self._hash(key)
        prev = None
        curr = self.hash_map[hash_index]
        while curr:
            if curr.key == key:
                index = curr.value
                if prev:
                    prev.next = curr.next
                else:
                    self.hash_map[index] = curr.next
            prev, curr = curr, curr.next
        else:
            return KeyError("Elemento da eliminare con chiave " + key + " non trovato")
        self.swap(index, len(self.heap) - 1)
        del self.heap[-1]
        self.min_heapify(index)

    def update(self, key, new_value):
        hash_index = self._hash(key)
        curr = self.hash_map[hash_index]
        while curr:
            if curr.key == key:
                index = curr.value
                self.heap[index] = new_value
                break
            curr = curr.next
        else:
            return KeyError("Elemento da modificare con chiave " + key + " non trovato")
        if new_value > self.heap[index]:
            self.max_heapify(index)
        elif new_value < self.heap[index]:
            self.min_heapify(index)

    def max_heapify(self, i):
        if i > 0:
            p = (i - 1) // 2
            if self.heap[i] > self.heap[p]:
                self.swap(i, p)
                self.max_heapify(p)
        else:
            return

    def min_heapify(self, i):
        l = 2*i + 1 #Figlio sinistro
        r = 2*i + 2 #Figlio destro
        min = i
        if l < len(self.heap) and self.heap[l] < self.heap[i]:
            min = l
        if r < len(self.heap) and self.heap[r] < self.heap[min]:
            min = r
        if min != i:
            self.swap(i, min)
            self.min_heapify(self, min)
        else:
            return

    def _swap(self, i , j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]


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
