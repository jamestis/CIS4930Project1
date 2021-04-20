#this function runs all four schemes on the same generated events

import sys
import os
import numpy
from pareto_random_samples import pareto_random_samples
from poisson_process import poisson_process
from Event import Event
import queue as Q
from check_inputs import check_inputs
from LRU_Cache import LRU_Cache
from MRU_Cache import MRU_Cache
from OrderedQueue import OrderedQueue
from datetime import datetime
import collections
import numpy as np
from generate_files import generate_files
from LFUCache import LFUCache

def test_with_same_parameters(lamb, num_files, alpha_s, alpha_p, num_requests, cache_capacity, R_c, R_a):
	round_trip_prop_time = .1 #s
	#generate events with probabilities and timings determined from parameters. Note that events are not generated
	#dynamically, as we can resemble the poisson process during preprocessing and account for queueing
	#behavior in a manner that is explained later.
	event_times = poisson_process(lamb,num_requests)
	file_sizes = generate_files(alpha_s,int(num_files))
	file_qis = pareto_random_samples(alpha_p,num_files)
	file_pis = file_qis / numpy.sum(file_qis)
	event_list = []
	for time in event_times:
		file_id = numpy.random.choice(len(file_pis), 1, True,file_pis)
		file_size = file_sizes[file_id]
		event_list.append(Event(time, file_size, file_id))

	schemes = ["MRU", "LRU", "FIFO", "LIFO"]
	ret = []
	for cache_policy in schemes:

		#reset event loop
		for event in event_list:
			event.finish_time = None

		cache_hit_rate = 0
		if cache_policy == "MRU":
			cache = MRU_Cache(cache_capacity)
		elif cache_policy == "LRU":
			cache = LRU_Cache(cache_capacity)
		elif cache_policy == "LIFO":
			cache = OrderedQueue(cache_capacity, True)
		elif cache_policy == "LFU":
			cache = LFUCache(cache_capacity)
		else:
			cache = OrderedQueue(cache_capacity, False)

		cache_util = []
		current_time = 0
		next_event = None
		
		for i in range(0,len(event_list)):
			current_event = event_list[i]
			#print(current_event)
			#print("Event began processing at ", current_time)
			#if i == 0:
				#current_time = current_event.arrival_time
			#if i == len(event_list) -1:
				#next_event = None
			#else:
				#next_event = event_list[i+1]
			#if cache.search(current_event.file_id[0]) == -1:
				#print("File not found in cache.")
				#cache.put(current_event.file_id[0], current_event.size[0])
				#current_event.finish_time = current_time + round_trip_prop_time + file_size / R_a + file_size / R_c
			#else:
				#print("File found in cache.")
				#current_event.finish_time = current_time + current_event.size / R_c
				#cache_hit_rate += 1

			
			#if next_event is not None:
				#current_time = max(current_event.finish_time, next_event.arrival_time)
			#else:
				#current_time = current_event.finish_time
			#print("Event finished processing at ", current_time)
			
			events_while_processing = 0

			#multiple event may be satisfied in the following logic. We only want to look at events that have not been satisfied
			if current_event.finish_time == None:
				#if the current time is behind an event, update the time while we wait
				if current_time < event_list[i].arrival_time:
					current_time = event_list[i].arrival_time
					

				#event is not in cache
				if cache.search(current_event.file_id[0] == -1):

					#add the event to the cache, determine the time it will take to finish
					cache.put(current_event.file_id[0], current_event.size[0])
					processing_time = round_trip_prop_time + current_event.size[0] / R_a + current_event.size[0] / R_c
					current_event.finish_time = current_time + processing_time

					#for each event that arrived while we were processing
					while event_list[i + 1 + events_while_processing].arrival_time < current_event.finish_time:
						#if it is in cache respond quickly
						if i + 1 + events_while_processing < len(event_list):
							if cache.search(event_list[i + 1 + events_while_processing].file_id[0] != -1):
								cached_event = event_list[i + 1 + events_while_processing]
								cached_event.finish_time = cached_event.arrival_time + cached_event.size[0] / R_c
								cache_hit_rate += 1
							events_while_processing += 1

					#we have reached the end of our event
					current_time += processing_time


		ret.append((cache_policy,sum((event.finish_time - event.arrival_time) for event in event_list) / len(event_list), cache_hit_rate/len(event_list) ))
	return ret
if __name__ == "__main__":
	print(test_with_same_parameters(2,10,5,1.2,50,50,100,5))