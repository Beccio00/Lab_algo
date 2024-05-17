import random
import sys
import timeit
import matplotlib.pyplot as plt
import pandas as pd

sys.setrecursionlimit(100000)


# Lista concatenata
class NodeLinkedList:
    def __init__(self, key, value, next=None):
        self.value = value
        self.next = next
        self.key = key


class LinkedList:
    def __init__(self):
        self.head = None

    def add(self, key, value):
        if self.search(key) is not None:
            print("La chiave ", key, " esiste già")
            return None
        new_node = NodeLinkedList(key, value, self.head)
        self.head = new_node

    def search(self, key):
        current = self.head
        while current is not None:
            if current.key == key:
                return current
            current = current.next
        return None

    def remove(self, key):
        current = self.head
        previous = None
        while current is not None:
            if current.key == key:
                if previous is not None:
                    previous.next = current.next
                else:
                    self.head = current.next
                return True
            previous = current
            current = current.next
        return False

    def size(self):
        current = self.head
        count = 0
        while current is not None:
            count = count + 1
            current = current.next
        return count

    def print(self):
        current = self.head
        print("List: ", end="")
        while current is not None:
            print("--> k: ", current.key, ", v: ", current.value, " ", end="")
            current = current.next
        print("")

    def copy(self):
        copy = LinkedList()
        current = self.head
        while current is not None:
            copy.add(current.key, current.value)
            current = current.next
        return copy


# Albero binario di ricerca
class NodeABR:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None


class ABR:
    def __init__(self):
        self.root = None

    def set_root(self, key, value):
        self.root = NodeABR(key, value)

    def insert(self, key, value):
        def _insert_node(currentNode, key, value):
            if key <= currentNode.key:
                if currentNode.left:
                    _insert_node(currentNode.left, key, value)
                else:
                    currentNode.left = NodeABR(key, value)
            else:
                if currentNode.right:
                    _insert_node(currentNode.right, key, value)
                else:
                    currentNode.right = NodeABR(key, value)

        if self.root is None:
            self.set_root(key, value)
        else:
            _insert_node(self.root, key, value)

    def remove(self, key):
        def _remove_node(currentNode, key):
            if currentNode is None:
                return currentNode
            if key < currentNode.key:
                currentNode.left = _remove_node(currentNode.left, key)
            elif key > currentNode.key:
                currentNode.right = _remove_node(currentNode.right, key)
            elif key == currentNode.key:
                # nel caso avesse un solo figlio
                if currentNode.left is None:
                    return currentNode.right
                elif currentNode.right is None:
                    return currentNode.left

                previousNode = self._find_maximum(currentNode.left)
                currentNode.key = previousNode.key
                currentNode.value = previousNode.value
                currentNode.left = _remove_node(currentNode.left, previousNode.key)
            return currentNode

        self.root = _remove_node(self.root, key)

    def search(self, key):
        def _search_node(currentNode, key):
            if currentNode is None:
                return None
            else:
                if key == currentNode.key:
                    return currentNode
                elif key < currentNode.key:
                    return _search_node(currentNode.left, key)
                else:
                    return _search_node(currentNode.right, key)

        return _search_node(self.root, key)

    def inorder(self):
        def _inorder(v):
            if v is None:
                return
            if v.left is not None:
                _inorder(v.left)
            print("--> k: ", v.key, " v: ", v.value, end="")
            if v.right is not None:
                _inorder(v.right)

        print("ABR: ", end="")
        _inorder(self.root)
        print("")

    def copy(self):
        def _copyNode(node):
            if node is None:
                return None
            copyNode = NodeABR(node.key, node.value)
            copyNode.left = _copyNode(node.left)
            copyNode.right = _copyNode(node.right)
            return copyNode

        copy = ABR()
        if self.root is not None:
            copy.root = _copyNode(self.root)
        return copy


# Hash 
class Hash:
    def __init__(self, size=5):
        self.hash_map = [LinkedList() for _ in range(size)]
        self.table_size = size

    def _hash(self, key):
        # scelgo A come secondo Knuth
        A = 0.61803398875
        hash_key = int(self.table_size * ((float(key) * A) % 1))
        return hash_key

    def insert(self, key, value):
        index = self._hash(key)
        if self.hash_map[index].search(key) is None:
            self.hash_map[index].add(key, value)
        else:
            return KeyError("Provato a inserire una chiave già presente")

    def delete(self, key):
        index = self._hash(key)
        node = self.hash_map[index].search(key)
        if node:
            self.hash_map[index].remove(key)

    def update(self, key, new_value):
        index = self._hash(key)
        node = self.hash_map[index].search(key)
        if node is not None:
            node.value = new_value
        else:
            return print("Elemento da modificare con chiave " + key + " non trovato")

    def search(self, key):
        index = self._hash(key)
        return self.hash_map[index].search(key)

    def print(self):
        print("Hash: ", end="")
        for i in range(self.table_size):
            currentNode = self.hash_map[i].head
            while currentNode is not None:
                print("{ " + str(currentNode.key) + ": " + str(currentNode.value) + "}", end="")
                currentNode = currentNode.next
        print()

    def copy(self):
        hash_copy = Hash(self.table_size)
        for i in range(self.table_size):
            currentNode = self.hash_map[i].head
            while currentNode is not None:
                hash_copy.insert(currentNode.key, currentNode.value)
                currentNode = currentNode.next
        return hash_copy



# Main
def main():
    hash = Hash()
    linkedList = LinkedList()
    abr = ABR()
    try:
        hash.insert(1, 10)
        hash.insert(1, 10)
        hash.insert(2, 20)
        hash.insert(3, 30)
        hash.insert(4, 5)

        hash.insert(5, 10)
        hash.insert(6, 20)
        hash.insert(7, 30)
        hash.insert(8, 40)

        hash.insert(9, 10)
        hash.insert(10, 13)
        hash.insert(11, 30)
        hash.insert(12, 40)
    except KeyError as e:
        print(e)

    linkedList.add(1, 10)
    linkedList.add(2, 20)
    linkedList.add(3, 30)
    linkedList.add(4, 120)

    abr.insert(1, 10)
    abr.insert(2, 20)
    abr.insert(3, 30)
    abr.insert(4, 70)

    hash.print()
    print(hash.search(2))
    hash.update(2, 120)
    print(hash.search(2))
    print(hash.search(81))
    hash.print()
    hash.delete(10)
    hash.print()

    linkedList.print()
    print(linkedList.search(4))
    print(linkedList.search(7))
    linkedList.remove(10)
    linkedList.print()

    abr.inorder()
    print(abr.search(4) is not None)
    print(abr.search(27) is not None)
    abr.remove(10)
    abr.inorder()
#     struct_size = [10, 250, 500, 750, 1000, 1250, 1500, 1750, 2000]
#
#     insert_list_times = []
#     search_list_times = []
#     remove_list_times = []
#
#     insert_abr_times = []
#     search_abr_times = []
#     remove_abr_times = []
#
#     insert_hash_times = []
#     search_hash_times = []
#     remove_hash_times = []
#
#     for size in struct_size:
#         linked_list = LinkedList()
#         abr = ABR()
#         hash_heap = Hash()
#         for i in range(size):
#             linked_list.add(i, random.randint(0, size))
#             abr.insert(i, random.randint(0, size))
#             hash_heap.insert(i, random.randint(0, size))
#
#         # Calcolo tempi lista concatenata
#         list_copy = linked_list.copy()
#         insert_list_time = timeit.timeit(
#             lambda: list_copy.add(random.randint(size + 1, size + 100), random.randint(0, size)), number=5)
#         search_list_time = timeit.timeit(lambda: linked_list.search(random.randint(0, size)), number=5)
#         remove_list_time = timeit.timeit(lambda: linked_list.remove(random.randint(0, size)), number=5)
#         insert_list_times.append(insert_list_time)
#         search_list_times.append(search_list_time)
#         remove_list_times.append(remove_list_time)
#
#         # Calcolo tempi albero binario di ricerca
#         abr_copy = abr.copy()
#         insert_abr_time = timeit.timeit(
#             lambda: abr_copy.insert(random.randint(size + 1, size + 100), random.randint(0, size)), number=5)
#         search_abr_time = timeit.timeit(lambda: abr.search(random.randint(0, size)), number=5)
#         remove_abr_time = timeit.timeit(lambda: abr.remove(random.randint(0, size)), number=5)
#         insert_abr_times.append(insert_abr_time)
#         search_abr_times.append(search_abr_time)
#         remove_abr_times.append(remove_abr_time)
#
#         # Calcolo tempi hash heap
#         hash_heap_copy = hash_heap.copy()
#         insert_hashheap_time = timeit.timeit(
#             lambda: hash_heap_copy.insert(random.randint(size + 1, size + 100), random.randint(0, size)), number=5)
#         search_hash_time = timeit.timeit(lambda: hash_heap.search(random.randint(0, size)), number=5)
#         remove_hash_time = timeit.timeit(lambda: hash_heap.delete(random.randint(0, size)), number=5)
#         insert_hash_times.append(insert_hash_time)
#         search_hash_times.append(search_hash_time)
#         remove_hash_times.append(remove_hash_time)
#
#     # tabelle lista concatenata
#     data_frame = pd.DataFrame({'# Elementi': struct_size, 'Tempo(s)': insert_list_times})
#     data_frame = data_frame.iloc[1:]
#     data_frame['Tempo(s)'] = data_frame['Tempo(s)'].apply(
#         lambda x: '{:.4e}'.format(x))
#     plt.figure(figsize=(6.5, 3.5))
#     plt.table(cellText=data_frame.values,
#               colLabels=data_frame.columns,
#               loc='center',
#               cellLoc='center',
#               rowLoc='center')
#     plt.title('Tabella inserimento lista cancatenata', fontsize=18, fontweight='bold')
#     plt.axis('tight')
#     plt.axis('off')
#     plt.savefig('insert_list_table.png')
#     plt.close()
#
#     data_frame = pd.DataFrame({'# Elementi': struct_size, 'Tempo(s)': search_list_times})
#     data_frame = data_frame.iloc[1:]
#     data_frame['Tempo(s)'] = data_frame['Tempo(s)'].apply(
#         lambda x: '{:.4e}'.format(x))
#     plt.figure(figsize=(6.5, 3.5))
#     plt.table(cellText=data_frame.values,
#               colLabels=data_frame.columns,
#               loc='center',
#               cellLoc='center',
#               rowLoc='center')
#     plt.title('Tabella ricerca lista cancatenata', fontsize=18, fontweight='bold')
#     plt.axis('tight')
#     plt.axis('off')
#     plt.savefig('search_list_table.png')
#     plt.close()
#
#     data_frame = pd.DataFrame({'# Elementi': struct_size, 'Tempo(s)': remove_list_times})
#     data_frame = data_frame.iloc[1:]
#     data_frame['Tempo(s)'] = data_frame['Tempo(s)'].apply(
#         lambda x: '{:.4e}'.format(x))
#     plt.figure(figsize=(6.5, 3.5))
#     plt.table(cellText=data_frame.values,
#               colLabels=data_frame.columns,
#               loc='center',
#               cellLoc='center',
#               rowLoc='center')
#     plt.title('Tabella eliminazione lista cancatenata', fontsize=18, fontweight='bold')
#     plt.axis('tight')
#     plt.axis('off')
#     plt.savefig('remove_list_table.png')
#     plt.close()
#
#     # Grafici lista concatenata
#     plt.plot(struct_size, insert_list_times, label='Prestazioni inserimento lista concatenata', marker='o')
#     plt.xlabel('Dimensione della lista')
#     plt.ylabel('Tempo medio (s)')
#     plt.legend()
#     plt.savefig('insert_list_plot.png')
#     plt.close()
#
#     plt.plot(struct_size, search_list_times, label='Prestazioni ricerca lista concatenata', marker='o')
#     plt.xlabel('Dimensione della lista')
#     plt.ylabel('Tempo medio (s)')
#     plt.legend()
#     plt.savefig('search_list_plot.png')
#     plt.close()
#
#     plt.plot(struct_size, remove_list_times, label='Prestazioni eliminazione lista concatenata', marker='o')
#     plt.xlabel('Dimensione della lista')
#     plt.ylabel('Tempo medio (s)')
#     plt.legend()
#     plt.savefig('remove_list_plot.png')
#     plt.close()
#
#     # Tabelle Alberi binari di ricerca
#     data_frame = pd.DataFrame({'# Elementi': struct_size, 'Tempo(s)': insert_abr_times})
#     data_frame = data_frame.iloc[1:]
#     data_frame['Tempo(s)'] = data_frame['Tempo(s)'].apply(
#         lambda x: '{:.4e}'.format(x))
#     plt.figure(figsize=(6.5, 3.5))
#     plt.table(cellText=data_frame.values,
#               colLabels=data_frame.columns,
#               loc='center',
#               cellLoc='center',
#               rowLoc='center')
#     plt.title('Tabella inserimento albero binario di ricerca', fontsize=18, fontweight='bold')
#     plt.axis('tight')
#     plt.axis('off')
#     plt.savefig('insert_abr_table.png')
#     plt.close()
#
#     data_frame = pd.DataFrame({'# Elementi': struct_size, 'Tempo(s)': search_abr_times})
#     data_frame = data_frame.iloc[1:]
#     data_frame['Tempo(s)'] = data_frame['Tempo(s)'].apply(
#         lambda x: '{:.4e}'.format(x))
#     plt.figure(figsize=(6.5, 3.5))
#     plt.table(cellText=data_frame.values,
#               colLabels=data_frame.columns,
#               loc='center',
#               cellLoc='center',
#               rowLoc='center')
#     plt.title('Tabella ricerca albero binario di ricerca', fontsize=18, fontweight='bold')
#     plt.axis('tight')
#     plt.axis('off')
#     plt.savefig('search_abr_table.png')
#     plt.close()
#
#     data_frame = pd.DataFrame({'# Elementi': struct_size, 'Tempo(s)': remove_abr_times})
#     data_frame = data_frame.iloc[1:]
#     data_frame['Tempo(s)'] = data_frame['Tempo(s)'].apply(
#         lambda x: '{:.4e}'.format(x))
#     plt.figure(figsize=(6.5, 3.5))
#     plt.table(cellText=data_frame.values,
#               colLabels=data_frame.columns,
#               loc='center',
#               cellLoc='center',
#               rowLoc='center')
#     plt.title('Tabella eliminazione albero binario di ricerca', fontsize=18, fontweight='bold')
#     plt.axis('tight')
#     plt.axis('off')
#     plt.savefig('remove_abr_table.png')
#     plt.close()
#
#     # Grafici alberi binari di ricerca
#     plt.plot(struct_size, insert_abr_times, label='Prestazioni inserimento albero binario di ricerca', marker='o')
#     plt.xlabel("# di elementi nell'albero")
#     plt.ylabel('Tempo medio (s)')
#     plt.legend()
#     plt.savefig('insert_abr_plot.png')
#     plt.close()
#
#     plt.plot(struct_size, search_abr_times, label='Prestazioni ricerca albero binario di ricerca', marker='o')
#     plt.xlabel("# di elementi nell'albero")
#     plt.ylabel('Tempo medio (s)')
#     plt.legend()
#     plt.savefig('search_abr_plot.png')
#     plt.close()
#
#     plt.plot(struct_size, remove_abr_times, label='Prestazioni eliminazione albero binario di ricerca', marker='o')
#     plt.xlabel("# di elementi nell'albero")
#     plt.ylabel('Tempo medio (s)')
#     plt.legend()
#     plt.savefig('remove_abr_plot.png')
#     plt.close()
#
#     # Tabelle HashHeap
#     data_frame = pd.DataFrame({'# Elementi': struct_size, 'Tempo(s)': insert_hash_times})
#     data_frame = data_frame.iloc[1:]
#     data_frame['Tempo(s)'] = data_frame['Tempo(s)'].apply(
#         lambda x: '{:.4e}'.format(x))
#     plt.figure(figsize=(6.5, 3.5))
#     plt.table(cellText=data_frame.values,
#               colLabels=data_frame.columns,
#               loc='center',
#               cellLoc='center',
#               rowLoc='center')
#     plt.title('Tabella inserimento hash heap', fontsize=18, fontweight='bold')
#     plt.axis('tight')
#     plt.axis('off')
#     plt.savefig('insert_hash_table.png')
#     plt.close()
#
#     data_frame = pd.DataFrame({'# Elementi': struct_size, 'Tempo(s)': search_hash_times})
#     data_frame = data_frame.iloc[1:]
#     data_frame['Tempo(s)'] = data_frame['Tempo(s)'].apply(
#         lambda x: '{:.4e}'.format(x))
#     plt.figure(figsize=(6.5, 3.5))
#     plt.table(cellText=data_frame.values,
#               colLabels=data_frame.columns,
#               loc='center',
#               cellLoc='center',
#               rowLoc='center')
#     plt.title('Tabella ricerca hash heap', fontsize=18, fontweight='bold')
#     plt.axis('tight')
#     plt.axis('off')
#     plt.savefig('search_hash_table.png')
#     plt.close()
#
#     data_frame = pd.DataFrame({'# Elementi': struct_size, 'Tempo(s)': remove_hash_times})
#     data_frame = data_frame.iloc[1:]
#     data_frame['Tempo(s)'] = data_frame['Tempo(s)'].apply(
#         lambda x: '{:.4e}'.format(x))
#     plt.figure(figsize=(6.5, 3.5))
#     plt.table(cellText=data_frame.values,
#               colLabels=data_frame.columns,
#               loc='center',
#               cellLoc='center',
#               rowLoc='center')
#     plt.title('Tabella eliminazione hash heap', fontsize=18, fontweight='bold')
#     plt.axis('tight')
#     plt.axis('off')
#     plt.savefig('remove_heahheap_table.png')
#     plt.close()
#
#     # Grafici hash heap
#     plt.plot(struct_size, insert_hash_times, label='Prestazioni inserimento hash heap', marker='o')
#     plt.xlabel("# di elementi nel hash")
#     plt.ylabel('Tempo medio (s)')
#     plt.legend()
#     plt.savefig('insert_hash_plot.png')
#     plt.close()
#
#     plt.plot(struct_size, search_hash_times, label='Prestazioni ricerca hash heap', marker='o')
#     plt.xlabel("# di elementi nel hash heap")
#     plt.ylabel('Tempo medio (s)')
#     plt.legend()
#     plt.savefig('search_hash_plot.png')
#     plt.close()
#
#     plt.plot(struct_size, remove_abr_times, label='Prestazioni eliminazione hash heap', marker='o')
#     plt.xlabel("# di elementi nel hash heap")
#     plt.ylabel('Tempo medio (s)')
#     plt.legend()
#     plt.savefig('remove_hash_plot.png')
#     plt.close()
#
#
if __name__ == "__main__":
    main()
