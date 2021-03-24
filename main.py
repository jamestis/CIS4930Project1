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



cache_used = 0
tree = Tree()

R_a = 15
#for event in event_list:
    #if found in cache
    #time = Si/Ra

    #if not found in cache

        ## FILE SIZE POLICY : largest goes:
            #while cache_used + event.file_size > cache_capacity:
                #gone = tree.delete_maximum()
                #cache_used -= gone.file_size
        ## FILE SIZE POLICY: smalled goes:
            #while cache_used + event.file_size > cache_capacity:
                #gone = tree.delete_minimum()
                #cache_used -= gone.file_size

        ## FILE SIZE POLICY: LRU:
            #for each file_id in cache:
                #(TUPLES OF : ARRIVAL, ID)
                    #(0,0), (1,2), (2,2), (3,0), (4,3)
                    #GROUP FILE_ID = 0 - > (0,0), (3,0)
                    #GROUP FILE_ID = 1 - > 
                    #GROUP FILE_ID = 2 - > (1,2),(2,2)
                    #GROUP FILE_ID = 3 - > (4,3)

                #delete the file with the smallest maximum time
        ## MRU

        ## CLEAR CACHE PERIODICALLY

        
    #look for what to replace:
    #insert into cache
    #calculate timing    


    #after all have finished: 
    
    #sum_of_waiting = 0
    #for event in event list:
        #sum_of_waiting += event.finished - event.time
    #avg = sum_of_waiting / len(event_list)
exit()