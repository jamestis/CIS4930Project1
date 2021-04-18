from collections import OrderedDict

class OrderedQueue:
    def __init__(self, capcity, FIFO):
        self.cache = OrderedDict()
        self.capcity = capcity
        self.current_memory_used = 0
        self.FIFO = FIFO
    def search(self, key):
        if key not in self.cache:
            return -1
        else:
            return self.cache[key]

    def put(self, file_id, file_size):
        while self.current_memory_used + file_size > self.capcity:
            removed = None
            if self.FIFO:
                removed = self.cache.popitem(last = False)
            else:
                removed = self.cache.popitem(last = True)
            self.current_memory_used -= removed[1]
            print("Removed file with id {}".format(removed))
        self.cache[file_id] = file_size
        self.current_memory_used += file_size
    
    def print_contents(self):
        for key in self.cache:
            print("File id {} with size {}".format(key, self.cache[key]))