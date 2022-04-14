class Node():
    def __init__(self):
        self.arr = []
        self.next = None


class UnrolledLinkedList():
    def __init__(self, max_node_capacity=4):
        self.max_node_capacity = max_node_capacity
        self.length = 0
        self.head = None
        self.tail = None

    def __delitem__(self, index):
        if index < 0:
            absIndex = self.length + index
        else:
            absIndex = index

        if index > self.length - 1:
            raise IndexError(str(index) + ' out of range. ')
        elif absIndex < 0:
            raise IndexError(str(index) + ' out of range. ')

        currentNode = self.head
        currentIndex = 0

        while len(currentNode.arr) - 1 + currentIndex < absIndex:
            currentIndex = currentIndex + len(currentNode.arr)
            currentNode = currentNode.next

        arrIndex = absIndex - currentIndex
        del currentNode.arr[arrIndex]
        self.length = self.length - 1

        nextNode = currentNode.next
        while nextNode:
            if len(currentNode.arr) < self.max_node_capacity // 2 and nextNode is not None:
                numberToTransfer = self.max_node_capacity // 2 - len(currentNode.arr) + 1
                currentNode.arr = currentNode.arr + nextNode.arr[:numberToTransfer]
                nextNode.arr = nextNode.arr[numberToTransfer:]

                if len(nextNode.arr) < self.max_node_capacity // 2:
                    currentNode.arr = currentNode.arr + nextNode.arr
                    currentNode.next = nextNode.next
                    del nextNode
            currentNode = currentNode.next
            if currentNode:
                nextNode = currentNode.next
            else:
                nextNode = None

    def __getitem__(self, index):
        if index < 0:
            absIndex = self.length + index
        else:
            absIndex = index

        if index > self.length - 1:
            raise IndexError(str(index) + 'out of range.')
        elif absIndex < 0:
            raise IndexError(str(absIndex) + 'out of range.')

        currentNode = self.head
        currentIndex = 0

        while len(currentNode.arr) - 1 + currentIndex < absIndex:
            currentIndex = currentIndex + len(currentNode.arr)
            currentNode = currentNode.next

        arrIndex = absIndex - currentIndex
        return currentNode.arr[arrIndex]

    def __setitem__(self, key, value):
        index = key
        if index < 0:
            absIndex = self.length + index
        else:
            absIndex = index

        if index > self.length - 1:  # Over the max
            raise IndexError(str(index) + ' out of range.')
        elif absIndex < 0:  # Below 0
            raise IndexError(str(index) + 'out of range.')

        currentNode = self.head
        currentIndex = 0
        while len(currentNode.arr) - 1 + currentIndex < absIndex:
            currentIndex = currentIndex + len(currentNode.arr)
            currentNode = currentNode.next

        arrIndex = absIndex - currentIndex
        currentNode.arr[arrIndex] = value

    def __iter__(self):
        current = self.head
        while current is not None:
            for x in current.arr:
                yield x
            current = current.next

    def __str__(self):
        if self.length == 0:
            return '{}'

        result = '{'
        current = self.head
        while current is not None:
            result = result + '['
            for i in range(0, len(current.arr)):
                result = result + str(current.arr[i])
                if i < len(current.arr) - 1:
                    result = result + ', '
            result = result + ']'
            if current.next is not None:
                result = result + ', '
            current = current.next
        result = result + '}'
        return result

    def __len__(self):
        return self.length

    def __reversed__(self):
        newL = UnrolledLinkedList(self.max_node_capacity)
        i = self.length - 1
        while i >= 0:
            yield self[i]
            i = i - 1

    def __contains__(self, obj):
        for i in self:
            if i == obj:
                return True
        return False

    # transfer a list into an unrolled linked list
    # def from_list(self, list1):
    #     length = len(list1)
    #     newNode = Node()
    #     self.head = newNode
    #     self.tail = newNode
    #     left = 0
    #     right = 2
    #     if length == 0:
    #         return
    #     else:
    #         while length >= 4:
    #             self.head.arr = list1[left, right]
    #             left += 2
    #             right += 2
    #             length -= 2
    #             newNode = Node()
    #             self.tail.next = newNode
    #             self.tail = newNode
    #         if length == 4:
    #             newNode = Node()
    #             self.head = newNode
    #             self.tail.next = newNode
    #             self.tail = newNode
    #             self.tail.arr.append(list1[-4:])
    #         elif length < 4 :
    #             self.head.arr.append(list1[-length:-length+2])
    #             newNode1 = Node()
    #             self.tail.next = newNode1
    #             self.tail = newNode1
    #             self.tail.arr.append(list1[-length+2:])

    # transfer an unrolled linked list into a list
    def to_list(self):
        res = []
        if self.head is None:
            return res
        else:
            for i in self:
                res.append(i)
            return res

    def append(self, data):
        if self.head is None:
            self.head = Node()
            self.head.arr.append(data)
            self.tail = self.head
        elif len(self.tail.arr) < self.max_node_capacity:
            self.tail.arr.append(data)
        else:
            newNode = Node()
            middle = len(self.tail.arr) // 2
            newNode.arr = self.tail.arr[middle * -1:]
            self.tail.arr = self.tail.arr[:middle * -1]
            self.tail.next = newNode
            self.tail = newNode
            self.tail.arr.append(data)
        self.length = self.length + 1
