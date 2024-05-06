# Hash heap
class HashMapListNode:
    def __init__(self, key, value, next=None):
        self.key = key
        self.value = value  #rappresenta la posizione dell'elemento nell'heap
        self.next = next


class HashHeap:
    def __int__(self, size=100):
        self.hash_map = [None] * size
        self.heap = []
        self.table_size = size

    def _hash(self, key):
        #scelgo A come secondo Knuth
        A = 0.61803398875
        hash_key = int(self.table_size * ((key * A) % 1))
        return hash_key

    def insert(self, key, value):
        hash_index = self._hash(key)
        #creo un nodo dell'hash map che è formato dalla chiave,
        #la lunghezza dell'heap dato che value rappresenta, il next il nodo corrente
        #perciò ci possono essere collisioni
        node = HashMapListNode(key, len(self.heap), self.hash_map[hash_index])
        self.hash_map[hash_index] = node
        self.heap.append(value)
        self.max_heapify_parent(len(self.heap) - 1)

    def delete(self, key):
        hash_index = self._hash(key)
        prev = None
        current = self.hash_map[hash_index]
        while current:
            if current.key == key:
                index = current.value
                if prev:
                    prev.next = current.next
                else:
                    self.hash_map[index] = current.next
            prev, current = current, current.next
        else:
            return KeyError("Elemento da eliminare con chiave " + key + " non trovato")
        self.swap(index, len(self.heap) - 1)
        del self.heap[-1]
        self.max_heapify_child(index)

    def update(self, key, new_value):
        hash_index = self._hash(key)
        current = self.hash_map[hash_index]
        while current:
            if current.key == key:
                index = current.value
                self.heap[index] = new_value
                break
            current = current.next
        else:
            return KeyError("Elemento da modificare con chiave " + key + " non trovato")
        if new_value > self.heap[index]:
            self.max_heapify_parent(index)
        elif new_value < self.heap[index]:
            self.max_heapify_child(index)

    def max_heapify_parent(self, i):
        if i > 0:
            p = (i - 1) // 2
            if self.heap[i] > self.heap[p]:
                self.swap(i, p)
                self.max_heapify_parent(p)
        else:
            return

    def max_heapify_child(self, i):
        l = 2 * i + 1  #Figlio sinistro
        r = 2 * i + 2  #Figlio destro
        max = i
        if l < len(self.heap) and self.heap[l] > self.heap[i]:
            max = l
        if r < len(self.heap) and self.heap[r] > self.heap[max]:
            max = r
        if max != i:
            self.swap(i, max)
            self.max_heapify_child(max)
        else:
            return

    def swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def search(self, key):
        hash_index = self._hash(key)
        current = self.hash_map[hash_index]
        while current is not None:
            if self.heap[current] == key:
                return self.heap[current]
            current = current.next
        return None

    def find_maximum(self):
        if not self.heap:
            return None
        return self.heap[0]
        #Siccome è un max heap il massimo sta alla radice

    def find_minimum(self):
        if not self.heap:
            return None
        min = self.heap[0]
        for value in self.heap:
            if value < min:
                min = value
        return min



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
        while current is not None:
            count = count + 1
            current = current.get_next()
        return count

    def search(self, item):
        current = self.head
        found = False
        while current is not None and not found:
            if current.get_data() == item:
                found = True
            else:
                current = current.get_next()
        return found

    def find_maximum(self):
        current = self.head.get_next()
        max = self.head.get_data()
        while current is not None:
            if current.get_data > max:
                max = current.get_data
            else:
                current = current.get_next()
        return max

    def find_minimum(self):
        current = self.head.get_next()
        min = self.head.get_data()
        while current is not None:
            if current.get_data < min:
                min = current.get_data
            else:
                current = current.get_next()
        return min

    def print_l(self):
        current = self.head
        previous = None
        while current is not None:
            print('..', current.get_data())
            current = current.get_next()

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
        if previous is None:
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

    def get_children(self):
        children = []
        if (self.left != None):
            children.append(self.left)
        if (self.right != None):
            children.append(self.right)
        return children


class ABR:
    def __init__(self):
        self.root = None

    def set_root(self, key):
        self.root = NodeABR(key)

    def insert(self, key):
        if (self.root is None):
            self.set_root(key)
        else:
            self.insert_node(self.root, key)

    def insert_node(self, currentNode, key):
        if (key <= currentNode.key):
            if (currentNode.left):
                self.insert_node(currentNode.left, key)
            else:
                currentNode.left = NodeABR(key)
        elif (key > currentNode.key):
            if (currentNode.right):
                self.insert_node(currentNode.right, key)
            else:
                currentNode.right = NodeABR(key)

    def search(self, key):
        return self.search_node(self.root, key)

    def search_node(self, currentNode, key):
        if (currentNode is None):
            return False
        elif (key == currentNode.key):
            return True
        elif (key < currentNode.key):
            return self.search_node(currentNode.left, key)
        else:
            return self.search_node(currentNode.right, key)

    def find_minimum(self):
        def _searchMinimum(currentNode):
            if currentNode.left is not None:
                return _searchMinimum(currentNode.left)
            else:
                return currentNode

        _searchMinimum(self.root)

    def find_maximum(self):
        def _find_maximum(currentNode):
            if currentNode.right is not None:
                return _find_maximum(currentNode.right)
            else:
                return currentNode

        _find_maximum(self.root)

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


#Main
def main():
    hashHeap = HashHeap()
    linkedList = LinkedList()
    abr = ABR()

    if __name__ == "__main__":
        main()
