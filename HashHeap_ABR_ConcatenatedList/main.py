from abc import ABC, abstractmethod


# Classi astratte per le liste concatenate

class AbstractNodeLinkedList(ABC):
    def __init__(self, value):
        self.value = value
        self.next = None

    @abstractmethod
    def set_value(self, *args, **kwargs):
        pass

    @abstractmethod
    def set_next(self, *args, **kwargs):
        pass

    def get_value(self):
        return self.value

    def get_next(self):
        return self.next


class AbstractLinkedList(ABC):
    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head is None

    @abstractmethod
    def add(self, *args, **kwargs):
        pass

    @abstractmethod
    def remove(self, input):
        pass

    @abstractmethod
    def search(self, input):
        pass

    def size(self):
        current = self.head
        count = 0
        while current is not None:
            count = count + 1
            current = current.get_next()
        return count


# Lista concatenata
class NodeLinkedList(AbstractNodeLinkedList):
    def __init__(self, value):
        super().__init__(value)

    def set_value(self, new_value, *args, **kwargs):
        self.value = new_value

    def set_next(self, new_next, *args, **kwargs):
        self.next = new_next


class LinkedList(AbstractLinkedList):
    def __init__(self):
        super().__init__()

    def add(self, item, *args, **kwargs):
        temp = NodeLinkedList(item)
        temp.set_next(self.head)
        self.head = temp

    def search(self, item):
        current = self.head
        found = False
        while current is not None and not found:
            if current.get_value() == item:
                found = True
            else:
                current = current.get_next()
        return found

    def remove(self, item):
        current = self.head
        previous = None
        found = False
        while not found:
            if current.get_value() == item:
                found = True
            else:
                previous = current
                current = current.get_next()
        if previous is None:
            self.head = current.get_next()
        else:
            previous.set_next(current.get_next())

    def find_maximum(self):
        current = self.head.get_next()
        max = self.head.get_value()
        while current is not None:
            if current.get_value > max:
                max = current.get_value()
            else:
                current = current.get_next()
        return max

    def find_minimum(self):
        current = self.head.get_next()
        min = self.head.get_value()
        while current is not None:
            if current.get_valu < min:
                min = current.get_value()
            else:
                current = current.get_next()
        return min

    def print_l(self):
        current = self.head
        previous = None
        while current is not None:
            print('..', current.get_value())
            current = current.get_next()


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


# Hash heap

class HashHeap:
    def __init__(self, size=10):
        self.hash_map = [LinkedListForHash() for _ in range(size)]
        self.heap = []
        self.table_size = size

    def _hash(self, key):
        #scelgo A come secondo Knuth
        A = 0.61803398875
        hash_key = int(self.table_size * ((float(key) * A) % 1))
        return hash_key

    def insert(self, key, value):
        hash_index = self._hash(key)
        self.hash_map[hash_index].add(key, value)
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
        hash_index_i = self._hash(i)
        x = self.hash_map[hash_index_i].search(i)
    #      if i is not None:
     #       x.set_value(hash_index_i, j)

        hash_index_j = self._hash(j)
        y = self.hash_map[hash_index_j].search(j)
       # if j is not None:
        #    y.set_value(hash_index_j, i)

        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def search(self, key):
        hash_index = self._hash(key)
        node = self.hash_map[hash_index].search(key)
        if node is not None:
            return node.get_key()
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


class NodeLinkedListForHash(AbstractNodeLinkedList):
    def __init__(self, key, value):
        super().__init__(value)  #In questo caso però value è la posizione dell' array heap
        self.key = key

    def get_key(self):
        return self.key

    def set_value(self, key, new_value, *args, **kwargs):
        if self.key == key:
            self.value = new_value

    def set_next(self, key, new_next, *args, **kwargs):
        if self.key == key:
            self.next = new_next


class LinkedListForHash(AbstractLinkedList):
    def __init__(self):
        super().__init__()

    def add(self, value, key, *args, **kwargs):
        new_node = NodeLinkedListForHash(key, value)
        new_node.next = self.head
        self.head = new_node

    def search(self, key):
        current = self.head
        while current is not None:
            if current.get_value() == key:
                return current
            current = current.next
        return

    def remove(self, key):
        current = self.head
        previous = None
        while current is not None:
            if current.get_key() == key:
                if previous is not None:
                    previous.next = current.next
                else:
                    self.head = current.next
                return True
            previous = current
            current = current.next
        return False


#Main
def main():
    hashHeap = HashHeap()
    linkedList = LinkedList()
    abr = ABR()

    hashHeap.insert(1, 10)
    hashHeap.insert(2, 20)
    hashHeap.insert(3, 30)
    hashHeap.insert(3, 40)

    linkedList.add(10)
    linkedList.add(20)
    linkedList.add(30)

    abr.insert(10)
    abr.insert(20)
    abr.insert(30)

    print(hashHeap.search(2))
    print(hashHeap.find_maximum())
    print(hashHeap.find_minimum())
    print('ciao')


if __name__ == "__main__":
    main()
