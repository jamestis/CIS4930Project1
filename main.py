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
from MRU_Cache import MRU_Cache
from OrderedQueue import OrderedQueue

def main(lamb, num_files, alpha_s, alpha_p, num_requests, cache_capacity, R_a, R_c, cache_policy):
	round_trip_prop_time = .4 #s

	#generate events with probabilities and timings determined from parameters. Note that events are not generated
	#dynamically, as we can resemble the poisson process during preprocessing and account for queueing
	#behavior in a manner that is explained later.
	event_times = poisson_process(lamb,num_requests)
	file_sizes = pareto_random_samples(alpha_s,int(num_files))
	file_qis = pareto_random_samples(alpha_p,num_files)
	file_pis = file_qis / numpy.sum(file_qis)

	event_list = []
	for time in event_times:
		file_id = numpy.random.choice(len(file_pis), 1, True,file_pis)
		file_size = file_sizes[file_id]
		event_list.append(Event(time, file_size, file_id))

	#determine caching policy
	cache = None
	if cache_policy == "MRU":
		cache = MRU_Cache(cache_capacity)
	elif cache_policy == "LRU":
		cache = LRU_Cache(cache_capacity)
	elif cache_policy == "LIFO":
		cache = OrderedQueue(cache_capacity, True)
	else:
		cache = OrderedQueue(cache_capacity, False)

	cache_util = []
	current_time = 0
	next_event = None

	#iterate over the events. In place of a queue, we determine the time we begin processing requests depending on
	#the finish time of the current process. This is accounted for in line
	#current_time += max(processing_time, next_event.arrival_time. By adding this,
	#we simulate that events enter a queue and must wait for prior events to be processes before running.

	for i in range(0,len(event_list)):
		current_event = event_list[i]
		if i == 0:
			current_time = current_event.arrival_time
		if i == len(event_list) -1:
			next_event = None
		else:
			next_event = event_list[i+1]
		if cache.search(current_event.file_id[0]) == -1:
			cache.put(current_event.file_id[0], current_event.size[0])
			current_event.finish_time = current_time + round_trip_prop_time + file_size / R_a + file_size / R_c
		else:
			current_event.finish_time = current_time + current_event.size / R_c
		if next_event is not None:
			current_time = max(current_event.finish_time, next_event.arrival_time)
		else:
			current_time = current_event.finish_time
	mean_turnaround_time = sum((event.finish_time - event.arrival_time) for event in event_list) / len(event_list)
	return mean_turnaround_time

#program to call a single time:
if __name__ == "__main__":
	t = check_inputs(sys.argv)