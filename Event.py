#add finish_time as member variable
class Event:
    def __init__(self, arrival_time, size, file_id,):
        self.arrival_time = arrival_time
        self.size = size
        self.file_id = file_id
        self.finish_time = None


    def __str__(self):
        time = "Arrival time : {} ,".format(str(self.arrival_time))
        size = "Size : {} ,".format(str(self.size))
        file_id = "file_id {} ".format(str(self.file_id))
        time_sat = "Time finished {}".format(str(self.finish_time))
        return time + size + file_id + time_sat

    def __lt__(self, other):
        return self.file_id < other.file_id

    def __gt__(self, other):
        return self.file_id> other.file_id

    #this is bad practice but will make using our tree much easier.
    def __eq__(self,other):
        return self.file_id == other.file_id
    
