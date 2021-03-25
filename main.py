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
current_time = 0
for event in event_list:
    #dereference array, numpy is annoying
    file_id = event.file_id[0]
    size = event.size[0]


    #NOT FOUND IN CACHE
    if cache.search(file_id) == -1:
        print("File id {} not found in cache. Inserting...".format(str(file_id)))
        cache.put(file_id,size)
        #current_time += D + ....
        #event.finished_time = current_time
    #FOUND IN CACHE
    else:
        print("File with id {} found in cache... Retreiving".format(str(file_id)))
        #current_time += event.size / R_c
        #event.finished_time = current_time
         

exit()