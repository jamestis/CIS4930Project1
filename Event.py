#add finish_time as member variable
class Event:
    def __init__(self, arrival_time, size, file_id,):
        self.arrival_time = arrival_time
        self.size = size
        self.file_id = file_id
        self.finish_time = None


    def __str__(self):
        time = "Arrival time : {} s,".format(str(self.arrival_time))
        size = "Size : {} MB,".format(str(self.size))
        file_id = "file_id {} ".format(str(self.file_id))
        time_sat = "Time finished {} s".format(str(self.finish_time))
        return time + size + file_id + time_sat

