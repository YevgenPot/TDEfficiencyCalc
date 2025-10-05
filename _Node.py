class Node:
    def __init__(self, name, data = None):
        self.name = name          # e.g., "placement", "up1-1"
        self.data = data          # stat dictionary
        self.next = None         # pointer to next node
        self.prev = None          # (optional) for doubly linked


class LinkedDataList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.depth = 0

    def attach(self, name, data):
        new_node = Node(name, data)
        self.depth += 1
        if not self.head:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail  # for doubly linked list support
            self.tail = new_node
    
    def __iter__(self):
        current = self.head
        while current:
            yield current
            current = current.next
    
    def find(self, name):
        for node in self:
            if node.name == name:
                return node
        return None
    

class MasterNode:
    def __init__(self, name, data = None):
        self.name = name
        self.data = data
        self.path = [None] # intended to be a list of linked lists

    def attachPath(self, path):
        if isinstance(path, LinkedDataList):
            self.path.append(path)
        else:
            print("Error!!!")
    

    
    



    