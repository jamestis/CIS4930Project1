#takes parameters: lambda, number of files N, F_s params, F_p params,
#consts: access link bandwidth Ra, round trip prop time btw network and serv D, institution network bandwidth Rc
#in cache response time : S_i / R_c
#not in cache = D+ Qd + Si / Ra + Si / Rc
#outputs = avg rtt

import sys
import os
import numpy
from pareto_random_samples import pareto_random_samples
from poisson_process import poisson_process
from Event import Event
import queue as Q
from splay_tree import Tree
from splay_tree import Node
from check_inputs import check_inputs
from LRU_Cache import LRU_Cache
import matplotlib.pyplot as plt
round_trip_prop_time = .4 #s
R_a = 15 #MBs
R_c = 100 #MBs

lamb, num_files, alpha_s, alpha_p, num_requests,cache_capacity,R_a,R_c= [check_inputs(sys.argv)[i] for i in(range(0,8))]
a = check_inputs(sys.argv)
print(a)
event_times = poisson_process(lamb,num_requests)
file_sizes = pareto_random_samples(alpha_s,int(num_files))
file_qis = pareto_random_samples(alpha_p,num_files)
file_pis = file_qis / numpy.sum(file_qis)

event_list = []
for time in event_times:
    file_id = numpy.random.choice(len(file_pis), 1, True,file_pis)
    file_size = file_sizes[file_id]
    event_list.append(Event(time, file_size, file_id))


cache = LRU_Cache(cache_capacity)
cache_util = []
current_time = 0
for i in range(0,len(event_list)):
    this_event = event_list[i]
    next_event = None
    if i != len(event_list) -1:
        next_event = event_list[i+1]
    if cache.search(this_event.file_id[0]) == -1:
        print("File with id {} not found in cache...inserting".format(str(this_event.file_id[0])))
        cache.put(this_event.file_id[0], this_event.size[0])
        this_event.finish_time = current_time + round_trip_prop_time + this_event.size[0] / R_c + this_event.size[0] / R_a
        if next_event:
            current_time = max(this_event.finish_time,next_event.arrival_time)
        else:
            current_time = this_event.finish_time
    else:
        print ("File with id {} found in cache... retreiving".format(str(this_event.file_id[0])))
        this_event.finish_time = current_time + this_event.size[0] / R_c
        if next_event:
            current_time = max(this_event.finish_time,next_event.arrival_time)
        else:
            current_time = this_event.finish_time
    print("CT: {} s".format(str(current_time)))
    print(this_event)
exit()