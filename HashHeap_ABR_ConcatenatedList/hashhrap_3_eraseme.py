class Dizionario_HashHeap:

    def __init__(self, size=7):
        self.hash_table = [_Lista_concatenata] * size
        for i in range(size):
            self.hash_table[i] = _Lista_concatenata()
        self.table_size = size
        self.heap = []

    def _hash(self, key):
        # valore di A secondo Knuth
        A = 0.61803398875
        hash_key = self.table_size * ((key * A) % 1)
        # parte intera inferiore
        hash_key = int(hash_key)
        return hash_key

    def insert(self, key, value):
        table_index = self._hash(key)
        # Se la chiave esiste già non viene effettuato nulla
        if self.hash_table[table_index].search(key) is not None:
            return
        # Se la chiave non esiste viene inserita
        x = _Heap_node(key, value)
        self.heap.append(x)
        self.hash_table[table_index].insert(key, len(self.heap) - 1)
        self._heapify_max(len(self.heap) - 1)

    def search(self, key):
        table_index = self._hash(key)
        x = self.hash_table[table_index].search(key)
        if x is not None:
            return self.heap[x.index]
        return None

    def delete(self, key):
        table_index = self._hash(key)
        # Se la chiave non esiste già non viene effettuato nulla
        x = self.hash_table[table_index].search(key)
        if x is None:
            return
        index = x.index
        self._swap(index, len(self.heap) - 1)
        self.hash_table[table_index].delete(key)
        del self.heap[len(self.heap) - 1]
        self._heapify_min(index)

    def size(self):
        return len(self.heap)

    def _heapify_max(self, i):
        while i > 0:
            parent_index = self._heap_parent(i)
            if self.heap[parent_index].value > self.heap[i].value:
                self._swap(parent_index, i)
                i = parent_index
            else:
                break

    def _heapify_min(self, i):
        while True:
            left_child = self._heap_left_child(i)
            right_child = self._heap_right_child(i)
            smallest_index = i

            if (left_child < len(self.heap) - 1) and self.heap[left_child].value < self.heap[smallest_index].value:
                smallest_index = left_child
            if (right_child < len(self.heap) - 1) and self.heap[right_child].value < self.heap[smallest_index].value:
                smallest_index = right_child
            if smallest_index != i:
                self._swap(i, smallest_index)
                i = smallest_index
            else:
                break

    def _swap(self, i, j):
        # cambio indici nel hashtable
        key = self.heap[i].key
        table_index = self._hash(key)
        x = self.hash_table[table_index].search(key)
        x.index = j

        key = self.heap[j].key
        x = self.hash_table[self._hash(key)].search(key)
        x.index = i
        # swap elementi nel heap
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def _heap_parent(self, i):
        return (i - 1) // 2

    def _heap_left_child(self, i):
        return 2 * i + 1

    def _heap_right_child(self, i):
        return 2 * i + 2


class _Lista_concatenata:
    head = None

    def insert(self, key, index):
        x = _List_node(key, index)
        x.next = self.head
        if self.head != None:
            self.head.prev = x
        self.head = x
        x.prev = None

    def search(self, key):
        x = self.head
        while x != None and x.key != key:
            x = x.next
        return x

    def delete(self, key):
        x = self.search(key)
        if x == None:
            return
        if x.prev != None:
            x.prev.next = x.next
        else:
            self.head = x.next
        if x.next != None:
            x.next.prev = x.prev


class _List_node:

    def __init__(self, key, index):
        self.key = key
        self.index = index
        self.next = None
        self.prev = None


class _Heap_node:

    def __init__(self, key, value):
        self.key = key
        self.value = value