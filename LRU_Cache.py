from collections import OrderedDict


class LRU_Cache:
    # initialising capacity
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity
        self.current_memory_used = 0
    # we return the value of the key
    # that is queried in O(1) and return -1 if we don't find the key in out dict / cache.
    # And also move the key to the end to show that it was recently used.
    '''Move an existing element to the end (or beginning if last is false).
       Raise KeyError if the element does not exist.'''
    def search(self, key: int) -> int:
        if not self.cache.get(key):
            return -1
        else:
            self.cache.move_to_end(key)
            return self.cache[key]

    # first, we add / update the key by conventional methods.
    # And also move the key to the end to show that it was recently used.
    # But here we will also check whether the length of our
    # ordered dictionary has exceeded our capacity,
    # If so we remove the first key (least recently used)
    def put(self, key: int, file_size: float) -> None:
        #This method is only called after search, so we do not need to search again.
        #We remove elements from the front until we have the memory available to add
        #our element.
        while self.current_memory_used + file_size > self.capacity:
            removed = self.cache.popitem(last=False)
            self.current_memory_used -= removed[1]
        
        #add element to back.
        self.cache[key] = file_size
        self.current_memory_used += file_size
        self.cache.move_to_end(key)


    def print_contents(self):
        for key in self.cache:
            print("File_id : {} , file_size: {}".format(str(key), str(self.cache.get(key))))

