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
        self.key = key
        self.next = next


class LinkedList:
    def __init__(self):
        self.head = None

    def insert(self, key, value):
        if self.search(key) is not None:
            print("La chiave ", key, " è già presente nella lista")
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

    def delete(self, key):
        current = self.head
        previous = None
        while current is not None:
            if current.key == key:
                if previous is not None:
                    previous.next = current.next
                else:
                    self.head = current.next
                return
            previous = current
            current = current.next
        print("Elemento da cancellare con chiave ", key, " non presente nella lista")

    def copy(self):
        copy = LinkedList()
        current = self.head
        while current is not None:
            copy.insert(current.key, current.value)
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
            if key < currentNode.key:
                if currentNode.left:
                    _insert_node(currentNode.left, key, value)
                else:
                    currentNode.left = NodeABR(key, value)
            elif key > currentNode.key:
                if currentNode.right:
                    _insert_node(currentNode.right, key, value)
                else:
                    currentNode.right = NodeABR(key, value)
            else:
                print("La chiave ", key, " è già presente nell'albero")

        if self.root is None:
            self.set_root(key, value)
        else:
            _insert_node(self.root, key, value)

    def delete(self, key):
        def _delete_node(currentNode, key):
            if currentNode is None:
                print("Elemento da cancellare con chiave ", key, " non è presente nell'albero")
                return currentNode
            if key < currentNode.key:
                currentNode.left = _delete_node(currentNode.left, key)
            elif key > currentNode.key:
                currentNode.right = _delete_node(currentNode.right, key)
            elif key == currentNode.key:
                # nel caso avesse un solo figlio
                if currentNode.left is None:
                    return currentNode.right
                elif currentNode.right is None:
                    return currentNode.left

                previousNode = self._find_maximum(currentNode.left)
                currentNode.key = previousNode.key
                currentNode.value = previousNode.value
                currentNode.left = _delete_node(currentNode.left, previousNode.key)
            return currentNode

        self.root = _delete_node(self.root, key)

    def search(self, key):
        def _search_node(currentNode, key):
            if currentNode is None:
                print("La chiave ", key, " non è presente nell'albero")
                return None
            else:
                if key == currentNode.key:
                    return currentNode
                elif key < currentNode.key:
                    return _search_node(currentNode.left, key)
                else:
                    return _search_node(currentNode.right, key)

        return _search_node(self.root, key)

    def copy(self):
        def _copy_node(node):
            if node is None:
                return None
            copyNode = NodeABR(node.key, node.value)
            copyNode.left = _copy_node(node.left)
            copyNode.right = _copy_node(node.right)
            return copyNode

        copy = ABR()
        if self.root is not None:
            copy.root = _copy_node(self.root)
        return copy

    def _find_maximum(self, currentNode):
        if currentNode.right is not None:
            return self._find_maximum(currentNode.right)
        else:
            return currentNode


# Hash 
class Hash:
    def __init__(self, size=16):
        self.hash_map = [LinkedList() for _ in range(size)]
        self.table_size = size

    def _hash(self, key):
        # scelgo A=(sqrt(5)-1)/2 secondo Knuth
        A = 0.61803398875
        # h(k) = inf(m(A mod 1))
        hash_key = int(self.table_size * ((float(key) * A) % 1))
        return hash_key

    def insert(self, key, value):
        index = self._hash(key)
        if self.hash_map[index].search(key) is None:
            self.hash_map[index].insert(key, value)
        else:
            print("La chiave ", key, " è già presente nell'hash map")

    def delete(self, key):
        index = self._hash(key)
        node = self.hash_map[index].search(key)
        if node:
            self.hash_map[index].delete(key)
        else:
            print("Elemento da cancellare con chiave", key, "non presente nell'array hash map")

    def search(self, key):
        index = self._hash(key)
        return self.hash_map[index].search(key)

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
    struct_size = [1, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500, 7000, 7500, 8000,
                   8500, 9000, 9500, 10000]

    insert_list_times = []
    search_list_times = []
    delete_list_times = []

    insert_abr_times = []
    search_abr_times = []
    delete_abr_times = []

    insert_hash_times = []
    search_hash_times = []
    delete_hash_times = []

    for size in struct_size:
        linked_list = LinkedList()
        abr = ABR()
        hash = Hash(16384)

        # Faccio sì che le chiavi siano inseriti all'interno dei dizionari in maniera randomica altrimenti l'albero
        # binario di ricerca sarebbe sbilanciato
        random_key = random.sample(range(size+1), size+1)
        for i in random_key:
            linked_list.insert(i, random.randint(0, size))
            abr.insert(i, random.randint(0, size))
            hash.insert(i, random.randint(0, size))

        list_copy = linked_list.copy()
        insert_list_time = timeit.timeit(
            lambda: list_copy.insert(random.randint(size + 1, size + 10000), random.randint(0, size)), number=5)

        search_list_time = timeit.timeit(lambda: linked_list.search(random.randint(0, size)), number=5)
        delete_list_time = timeit.timeit(lambda: linked_list.delete(random.randint(0, size)), number=5)
        insert_list_times.append(insert_list_time)
        search_list_times.append(search_list_time)
        delete_list_times.append(delete_list_time)

        # Calcolo tempi albero binario di ricerca
        abr_copy = abr.copy()
        insert_abr_time = timeit.timeit(
            lambda: abr_copy.insert(random.randint(size + 1, size + 10000), random.randint(0, size)), number=5)
        search_abr_time = timeit.timeit(lambda: abr.search(random.randint(0, size)), number=5)
        delete_abr_time = timeit.timeit(lambda: abr.delete(random.randint(0, size)), number=5)
        insert_abr_times.append(insert_abr_time)
        search_abr_times.append(search_abr_time)
        delete_abr_times.append(delete_abr_time)

        # Calcolo tempi hash
        hash_copy = hash.copy()
        insert_hash_time = timeit.timeit(
            lambda: hash_copy.insert(random.randint(size + 1, size + 10000), random.randint(0, size)), number=5)
        search_hash_time = timeit.timeit(lambda: hash.search(random.randint(0, size)), number=5)
        delete_hash_time = timeit.timeit(lambda: hash.delete(random.randint(0, size)), number=5)
        insert_hash_times.append(insert_hash_time)
        search_hash_times.append(search_hash_time)
        delete_hash_times.append(delete_hash_time)

    # tabelle lista concatenata
    data_frame = pd.DataFrame({'# Elementi': struct_size, 'Tempo(s)': insert_list_times})
    data_frame = data_frame.iloc[1:]
    data_frame['Tempo(s)'] = data_frame['Tempo(s)'].apply(
        lambda x: '{:.4e}'.format(x))
    plt.figure(figsize=(6.5, 5))
    plt.table(cellText=data_frame.values,
              colLabels=data_frame.columns,
              loc='center',
              cellLoc='center',
              rowLoc='center')
    plt.title('Tabella inserimento lista cancatenata', fontsize=18, fontweight='bold')
    plt.axis('tight')
    plt.axis('off')
    plt.savefig('insert_list_table.png')
    plt.close()

    data_frame = pd.DataFrame({'# Elementi': struct_size, 'Tempo(s)': search_list_times})
    data_frame = data_frame.iloc[1:]
    data_frame['Tempo(s)'] = data_frame['Tempo(s)'].apply(
        lambda x: '{:.4e}'.format(x))
    plt.figure(figsize=(6.5, 5))
    plt.table(cellText=data_frame.values,
              colLabels=data_frame.columns,
              loc='center',
              cellLoc='center',
              rowLoc='center')
    plt.title('Tabella ricerca lista cancatenata', fontsize=18, fontweight='bold')
    plt.axis('tight')
    plt.axis('off')
    plt.savefig('search_list_table.png')
    plt.close()

    data_frame = pd.DataFrame({'# Elementi': struct_size, 'Tempo(s)': delete_list_times})
    data_frame = data_frame.iloc[1:]
    data_frame['Tempo(s)'] = data_frame['Tempo(s)'].apply(
        lambda x: '{:.4e}'.format(x))
    plt.figure(figsize=(6.5, 5))
    plt.table(cellText=data_frame.values,
              colLabels=data_frame.columns,
              loc='center',
              cellLoc='center',
              rowLoc='center')
    plt.title('Tabella eliminazione lista cancatenata', fontsize=18, fontweight='bold')
    plt.axis('tight')
    plt.axis('off')
    plt.savefig('delete_list_table.png')
    plt.close()

    # Grafici lista concatenata
    plt.plot(struct_size, insert_list_times, label='Prestazioni inserimento lista concatenata', marker='o')
    plt.xlabel('Dimensione della lista')
    plt.ylabel('Tempo medio (s)')
    plt.legend()
    plt.savefig('insert_list_plot.png')
    plt.close()

    plt.plot(struct_size, search_list_times, label='Prestazioni ricerca lista concatenata', marker='o')
    plt.xlabel('Dimensione della lista')
    plt.ylabel('Tempo medio (s)')
    plt.legend()
    plt.savefig('search_list_plot.png')
    plt.close()

    plt.plot(struct_size, delete_list_times, label='Prestazioni eliminazione lista concatenata', marker='o')
    plt.xlabel('Dimensione della lista')
    plt.ylabel('Tempo medio (s)')
    plt.legend()
    plt.savefig('delete_list_plot.png')
    plt.close()

    # Tabelle Alberi binari di ricerca
    data_frame = pd.DataFrame({'# Elementi': struct_size, 'Tempo(s)': insert_abr_times})
    data_frame = data_frame.iloc[1:]
    data_frame['Tempo(s)'] = data_frame['Tempo(s)'].apply(
        lambda x: '{:.4e}'.format(x))
    plt.figure(figsize=(6.5, 5))
    plt.table(cellText=data_frame.values,
              colLabels=data_frame.columns,
              loc='center',
              cellLoc='center',
              rowLoc='center')
    plt.title('Tabella inserimento albero binario di ricerca', fontsize=18, fontweight='bold')
    plt.axis('tight')
    plt.axis('off')
    plt.savefig('insert_abr_table.png')
    plt.close()

    data_frame = pd.DataFrame({'# Elementi': struct_size, 'Tempo(s)': search_abr_times})
    data_frame = data_frame.iloc[1:]
    data_frame['Tempo(s)'] = data_frame['Tempo(s)'].apply(
        lambda x: '{:.4e}'.format(x))
    plt.figure(figsize=(6.5, 5))
    plt.table(cellText=data_frame.values,
              colLabels=data_frame.columns,
              loc='center',
              cellLoc='center',
              rowLoc='center')
    plt.title('Tabella ricerca albero binario di ricerca', fontsize=18, fontweight='bold')
    plt.axis('tight')
    plt.axis('off')
    plt.savefig('search_abr_table.png')
    plt.close()

    data_frame = pd.DataFrame({'# Elementi': struct_size, 'Tempo(s)': delete_abr_times})
    data_frame = data_frame.iloc[1:]
    data_frame['Tempo(s)'] = data_frame['Tempo(s)'].apply(
        lambda x: '{:.4e}'.format(x))
    plt.figure(figsize=(6.5, 5))
    plt.table(cellText=data_frame.values,
              colLabels=data_frame.columns,
              loc='center',
              cellLoc='center',
              rowLoc='center')
    plt.title('Tabella eliminazione albero binario di ricerca', fontsize=18, fontweight='bold')
    plt.axis('tight')
    plt.axis('off')
    plt.savefig('delete_abr_table.png')
    plt.close()

    # Grafici alberi binari di ricerca
    plt.plot(struct_size, insert_abr_times, label='Prestazioni inserimento albero binario di ricerca', marker='o')
    plt.xlabel("# di elementi nell'albero")
    plt.ylabel('Tempo medio (s)')
    plt.ylim(0, 0.0001)
    plt.legend()
    plt.savefig('insert_abr_plot.png')
    plt.close()

    plt.plot(struct_size, search_abr_times, label='Prestazioni ricerca albero binario di ricerca', marker='o')
    plt.xlabel("# di elementi nell'albero")
    plt.ylabel('Tempo medio (s)')
    plt.ylim(0, 0.0001)
    plt.legend()
    plt.savefig('search_abr_plot.png')
    plt.close()

    plt.plot(struct_size, delete_abr_times, label='Prestazioni eliminazione albero binario di ricerca', marker='o')
    plt.xlabel("# di elementi nell'albero")
    plt.ylabel('Tempo medio (s)')
    plt.ylim(0, 0.0001)
    plt.legend()
    plt.savefig('delete_abr_plot.png')
    plt.close()

    # Tabelle dell'hash
    data_frame = pd.DataFrame({'# Elementi': struct_size, 'Tempo(s)': insert_hash_times})
    data_frame = data_frame.iloc[1:]
    data_frame['Tempo(s)'] = data_frame['Tempo(s)'].apply(
        lambda x: '{:.4e}'.format(x))
    plt.figure(figsize=(6.5, 5))
    plt.table(cellText=data_frame.values,
              colLabels=data_frame.columns,
              loc='center',
              cellLoc='center',
              rowLoc='center')
    plt.title('Tabella inserimento hash', fontsize=18, fontweight='bold')
    plt.axis('tight')
    plt.axis('off')
    plt.savefig('insert_hash_table.png')
    plt.close()

    data_frame = pd.DataFrame({'# Elementi': struct_size, 'Tempo(s)': search_hash_times})
    data_frame = data_frame.iloc[1:]
    data_frame['Tempo(s)'] = data_frame['Tempo(s)'].apply(
        lambda x: '{:.4e}'.format(x))
    plt.figure(figsize=(6.5, 5))
    plt.table(cellText=data_frame.values,
              colLabels=data_frame.columns,
              loc='center',
              cellLoc='center',
              rowLoc='center')
    plt.title('Tabella ricerca hash', fontsize=18, fontweight='bold')
    plt.axis('tight')
    plt.axis('off')
    plt.savefig('search_hash_table.png')
    plt.close()

    data_frame = pd.DataFrame({'# Elementi': struct_size, 'Tempo(s)': delete_hash_times})
    data_frame = data_frame.iloc[1:]
    data_frame['Tempo(s)'] = data_frame['Tempo(s)'].apply(
        lambda x: '{:.4e}'.format(x))
    plt.figure(figsize=(6.5, 5))
    plt.table(cellText=data_frame.values,
              colLabels=data_frame.columns,
              loc='center',
              cellLoc='center',
              rowLoc='center')
    plt.title('Tabella eliminazione hash', fontsize=18, fontweight='bold')
    plt.axis('tight')
    plt.axis('off')
    plt.savefig('delete_hash_table.png')
    plt.close()

    # Grafici hash
    plt.plot(struct_size, insert_hash_times, label='Prestazioni inserimento hash', marker='o')
    plt.xlabel("# di elementi nel hash")
    plt.ylabel('Tempo medio (s)')
    plt.ylim(0, 0.0001)
    plt.legend()
    plt.savefig('insert_hash_plot.png')
    plt.close()

    plt.plot(struct_size, search_hash_times, label='Prestazioni ricerca hash', marker='o')
    plt.xlabel("# di elementi nel hash")
    plt.ylabel('Tempo medio (s)')
    plt.ylim(0, 0.0001)
    plt.legend()
    plt.savefig('search_hash_plot.png')
    plt.close()

    plt.plot(struct_size, delete_hash_times, label='Prestazioni eliminazione hash', marker='o')
    plt.xlabel("# di elementi nel hash")
    plt.ylabel('Tempo medio (s)')
    plt.ylim(0, 0.0001)
    plt.legend()
    plt.savefig('delete_hash_plot.png')
    plt.close()

    # Grafici di inserimento
    plt.figure(figsize=(10, 6))
    plt.plot(struct_size, insert_list_times, label='Inserimento lista concatenata', marker='o')
    plt.plot(struct_size, insert_abr_times, label='Inserimento albero binario di ricerca', marker='o')
    plt.plot(struct_size, insert_hash_times, label='Inserimento hash', marker='o')
    plt.xlabel('Dimensione della struttura dati')
    plt.ylabel('Tempo medio (s)')
    plt.legend()
    plt.title('Confronto prestazioni di inserimento')
    plt.savefig('insert_comparison_plot.png')
    plt.close()

    # Grafici di ricerca
    plt.figure(figsize=(10, 6))
    plt.plot(struct_size, search_list_times, label='Ricerca lista concatenata', marker='o')
    plt.plot(struct_size, search_abr_times, label='Ricerca albero binario di ricerca', marker='o')
    plt.plot(struct_size, search_hash_times, label='Ricerca hash', marker='o')
    plt.xlabel('Dimensione della struttura dati')
    plt.ylabel('Tempo medio (s)')
    plt.legend()
    plt.title('Confronto prestazioni di ricerca')
    plt.savefig('search_comparison_plot.png')
    plt.close()

    # Grafici di eliminazione
    plt.figure(figsize=(10, 6))
    plt.plot(struct_size, delete_list_times, label='Eliminazione lista concatenata', marker='o')
    plt.plot(struct_size, delete_abr_times, label='Eliminazione albero binario di ricerca', marker='o')
    plt.plot(struct_size, delete_hash_times, label='Eliminazione hash', marker='o')
    plt.xlabel('Dimensione della struttura dati')
    plt.ylabel('Tempo medio (s)')
    plt.legend()
    plt.title('Confronto prestazioni di eliminazione')
    plt.savefig('delete_comparison_plot.png')
    plt.close()



if __name__ == "__main__":
    main()
