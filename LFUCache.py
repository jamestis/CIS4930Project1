from collections import defaultdict, OrderedDict


class Node:
    def __init__(self, key, val, freq):
        self.key = key
        self.val = val
        self.freq = freq
    

class LFUCache:

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.min_freq = None
        self.current_memory_used = 0
        # hash map for key-node
        self.key2node = dict()
        
        # doubly-linked hash map
        self.freq2node = defaultdict(OrderedDict)

    def search(self, key: int) -> int:
        if key not in self.key2node:
            return -1
        
        node = self.key2node[key]
        # cuz node has been "get", its frequency would go up
        # remove its old pair in freq2node
        del self.freq2node[node.freq][key]
        
        # further check whether old node.freq is empty in freq2node
        if not self.freq2node[node.freq]:
            del self.freq2node[node.freq]
        
        # update node in freq2node
        node.freq += 1
        self.freq2node[node.freq][key] = node
        
        # update min_freq
        if not self.freq2node[self.min_freq]:
            self.min_freq += 1
    
        return node.val
        

    def put(self, key: int, value: float) -> None: 
        if not self.capacity:
            return 
        
        if key in self.key2node:
            self.key2node[key].val = value
            # update key 
            _ = self.search(key)
            return 
        
        # already reached capacity limit
        if self.current_memory_used + value > self.capacity:
            # remove least frequently used node
            k, node = self.freq2node[self.min_freq].popitem(last=False)
            self.current_memory_used -= self.key2node[k].val
            del self.key2node[k]
                

        self.freq2node[1][key] = self.key2node[key] = Node(key, value, 1)
        self.current_memory_used += value
        self.min_freq = 1
        return 


    def print_contents(self):
        for key in self.key2node:
            print("Key : ", key, " Value : ", self.key2node[key])