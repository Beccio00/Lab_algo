from abc import ABC, abstractmethod


# Classi astratte per le liste concatenate

class AbstractNodeLinkedList(ABC):
    def __init__(self, value):
        self._value = value
        self._next = None

    @abstractmethod
    def set_value(self, *args, **kwargs):
        pass

    @abstractmethod
    def set_next(self, *args, **kwargs):
        pass

    def get_value(self):
        return self._value

    def get_next(self):
        return self._next


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
        self._value = new_value

    def set_next(self, new_next, *args, **kwargs):
        self._next = new_next


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
    def __init__(self, size=5):
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
        self.heap.append(HeapNode(key, value))
        self.hash_map[hash_index].add(key, len(self.heap) - 1)
        self.max_heapify()

    def delete(self, key):
        hash_index = self._hash(key)
        prev = None
        current = self.hash_map[hash_index]
        while current:
            if current.get_key() == key:
                index = current.get_value()
                if prev:
                    prev.set_next(prev.get_key(), current.get_next())
                else:
                    self.hash_map[index] = current.get_next()
            prev, current = current, current.get_next()
        else:
            return KeyError("Elemento da eliminare con chiave " + key + " non trovato")
        self.swap(index, len(self.heap))
        del self.heap[-1]
        self.max_heapify()

    def update(self, key, new_value):
        hash_index = self._hash(key)
        current = self.hash_map[hash_index]
        while current:
            if current.key == key:
                index = current.get_value()
                self.heap[index].value = new_value
                break
            current = current.get_next()
        else:
            return KeyError("Elemento da modificare con chiave " + key + " non trovato")
        self.max_heapify()

    def max_heapify_parent(self, i):
        if i > 0:
            p = (i - 1) // 2
            if self.heap[i].value > self.heap[p].value:
                self.swap(i, p)
                self.max_heapify()
        else:
            return

    def max_heapify_child(self, i):
        l = 2 * i + 1  #Figlio sinistro
        r = 2 * i + 2  #Figlio destro
        max = i
        if l < len(self.heap) and self.heap[l].value > self.heap[i].value:
            max = l
        if r < len(self.heap) and self.heap[r].value > self.heap[max].value:
            max = r
        if max != i:
            self.swap(i, max)
            self.max_heapify()
        else:
            return

    def max_heapify(self):
        def _max_heapify(i):
            l = 2 * i + 1  # Figlio sinistro
            r = 2 * i + 2  # Figlio destro
            max = i
            if l < len(self.heap) and self.heap[l].value > self.heap[i].value:
                max = l
            if r < len(self.heap) and self.heap[r].value > self.heap[max].value:
                max = r
            if max != i:
                self.swap(i, max)
                self.max_heapify()
            else:
                return

        _max_heapify(0)
    #FIXME non funziona perchè si blocca solo al primo




    def swap(self, i, j):
        hash_index_i = self._hash(self.heap[i].key)
        x = self.hash_map[hash_index_i].search(self.heap[i].key)
        x.set_value(self.heap[i].key, j)

        hash_index_j = self._hash(self.heap[j].key)
        y = self.hash_map[hash_index_j].search(self.heap[j].key)
        y.set_value(self.heap[j].key, i)

        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def search(self, key):
        hash_index = self._hash(key)
        node = self.hash_map[hash_index].search(key)
        if node is not None:
            return self.heap[node.get_value()].value
        return None

    def find_maximum(self):
        if not self.heap:
            return None
        return self.heap[0].value
        #Siccome è un max heap il massimo sta alla radice

    def find_minimum(self):
        if not self.heap:
            return None
        min = self.heap[0].value
        for node in self.heap:
            if node.value < min:
                min = node.value
        return min

    def print(self):
        print("Heap: [", end="")
        for node in self.heap:
            print(str(node.value) + ", ", end="")
        print("]")



class NodeLinkedListForHash(AbstractNodeLinkedList):
    def __init__(self, key, value):
        super().__init__(value)  #In questo caso però value è la posizione dell' array heap
        self.key = key

    def get_key(self):
        return self.key

    def set_value(self, key, new_value, *args, **kwargs):
        if key == self.key:
            self._value = new_value
        else:
            return KeyError("È stato provato a modificare un nodo nella lista senza aver inserito la chiave corretta.")

    def set_next(self, key, new_next, *args, **kwargs):
        if self.key == key:
            self._next = new_next
        else:
            return KeyError("È stato provato a modificare un nodo nella lista senza aver inserito la chiave corretta.")


class LinkedListForHash(AbstractLinkedList):
    def __init__(self):
        super().__init__()

    def add(self, key, value, *args, **kwargs):
        new_node = NodeLinkedListForHash(key, value)
        new_node.set_next(key, self.head)
        self.head = new_node

    def search(self, key):
        current = self.head
        while current is not None:
            if current.get_key() == key:
                return current
            current = current.get_next()
        return

    def remove(self, key):
        current = self.head
        previous = None
        while current is not None:
            if current.get_key() == key:
                if previous is not None:
                    previous.set_next(previous.get_key(), current.get_next())
                else:
                    self.head = current.get_next()
                return True
            previous = current
            current = current.get_next()
        return False


class HeapNode: #È che l'heap salvi anche la chiave inserita dell'utente
    def __init__(self, key, value):
        self.key = key
        self.value = value



#Main
def main():
    hashHeap = HashHeap()
    linkedList = LinkedList()
    abr = ABR()

    hashHeap.insert(1, 10)
    hashHeap.insert(2, 20)
    hashHeap.insert(3, 30)
    hashHeap.insert(4, 40)

    hashHeap.insert(5, 10)
    hashHeap.insert(6, 20)
    hashHeap.insert(7, 30)
    hashHeap.insert(8, 40)

    hashHeap.insert(9, 10)
    hashHeap.insert(10, 20)
    hashHeap.insert(11, 30)
    hashHeap.insert(12, 40)

    linkedList.add(10)
    linkedList.add(20)
    linkedList.add(30)

    abr.insert(10)
    abr.insert(20)
    abr.insert(30)

    print(hashHeap.search(2))
    print(hashHeap.find_maximum())
    print(hashHeap.find_minimum())
    hashHeap.print()



if __name__ == "__main__":
    main()
