#add finish_time as member variable
class Event:
    def __init__(self, arrival_time, size, file_id,):
        self.arrival_time = arrival_time
        self.size = size
        self.file_id = file_id


    def __str__(self):
        time = "Time : {} ,".format(str(self.arrival_time))
        size = "Size : {} ,".format(str(self.size))
        file_id = "file_id {} ".format(str(self.file_id))
        return time + size + file_id

    def __lt__(self, other):
        return self.size < other.size