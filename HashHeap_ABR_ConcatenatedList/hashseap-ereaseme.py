class HashHeap():
    '''max heap'''

    def __init__(self):
        self.mapping = {}
        # stores lists of [freq, key]
        self.A = []

    def top(self):
        if len(self.A) == 0:
            return None
        return self.A[0][0]

    def pop(self):
        self.A[0], self.A[-1] = self.A[-1], self.A[0]
        self.A.pop()
        self.siftDown_(0)
        return

    def siftUp_(self, i):
        while i > 0 and self.A[(i - 1) // 2] <= self.A[i]:
            self.A[(i - 1) // 2], self.A[i] = self.A[i], self.A[(i - 1) // 2]
            # update mapping as well
            self.updateMapping_(i)
            self.updateMapping_((i - 1) // 2)
            i = (i - 1) // 2
        return i

    def siftDown_(self, i):
        while 2 * i + 2 < len(self.A) and \
                (self.A[i] <= self.A[2 * i + 1] or self.A[i] <= self.A[2 * i + 2]):
            if self.A[2 * i + 1] > self.A[2 * i + 2]:
                self.A[i], self.A[2 * i + 1] = self.A[2 * i + 1], self.A[i]
                self.updateMapping_(i)
                self.updateMapping_(2 * i + 1)
                i = 2 * i + 1
            else:
                self.A[i], self.A[2 * i + 2] = self.A[2 * i + 2], self.A[i]
                self.updateMapping_(i)
                self.updateMapping_(2 * i + 2)
                i = 2 * i + 2

        if 2 * i + 1 < len(self.A) and self.A[i] <= self.A[2 * i + 1]:
            self.A[i], self.A[2 * i + 1] = self.A[2 * i + 1], self.A[i]
            self.updateMapping_(i)
            self.updateMapping_(2 * i + 1)
            i = 2 * i + 1

        return i

    def updateMapping_(self, i):
        self.mapping[self.A[i][1]] = i
        return

    def push(self, key, val):
        self.A.append([val, key])
        self.mapping[key] = len(self.A) - 1
        return self.siftUp_(len(self.A) - 1)

    def getVal(self, key):
        if key not in self.mapping:
            return 0

        idx = self.mapping[key]
        return self.A[idx][0]

    def setVal(self, key, val):
        if key not in self.mapping:
            idx = self.push(key, val)
            return
        idx = self.mapping[key]
        self.A[idx][0] = val
        idx = self.siftUp_(idx)
        idx = self.siftDown_(idx)
        return

    def remove(self, key):
        if key not in self.mapping:
            return
        idx = self.mapping[key]
        self.A[idx], self.A[-1] = self.A[-1], self.A[idx]
        self.updateMapping_(idx)
        self.A.pop()
        del self.mapping[key]


if __name__ == "__main__":
    hhobj = HashHeap()
    hhobj.setVal('a', 1)
    hhobj.setVal('b', 2)
    hhobj.setVal('c', 3)
    hhobj.setVal('b', 4)
    print(hhobj.top())
    print(hhobj.getVal('a'))
    print(hhobj.getVal('b'))
    hhobj.remove('b')
    print(hhobj.top())