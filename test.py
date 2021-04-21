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
import matplotlib.pyplot as plt
def test(lamb, num_files, alpha_s, alpha_p, num_requests, cache_capacity, R_c, R_a):
	round_trip_prop_time = .4 #s
	lfu_rtt = 0
	mru_rtt = 0
	lru_rtt = 0
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


	policies = ["MRU", "LRU", "LFU"]
	ret = []
	for policy in policies:
		#reset event loop
		print(policy)
		for event in event_list:
			event.finish_time = None
		cache = None
		cache_hit_rate = 0
		current_time = 0
		ret = []
		if policy == "MRU":
			cache = MRU_Cache(cache_capacity)
		elif policy == "LRU":
			cache = LRU_Cache(cache_capacity)
		elif policy == "FIFO":
			cache = OrderedQueue(cache_capacity, FIFO = True)
		elif policy == "LFU":
			cache = LFUCache(cache_capacity)
		else:
			cache = OrderedQueue(cache_capacity, FIFO = False)
		#main event loop
		for i in range(0,len(event_list)):
			current_event = event_list[i]
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
					
					
					events_while_processing = 1
					while i + events_while_processing < len(event_list):
						#if it is in cache respond quickly
						if event_list[i + events_while_processing].arrival_time <= current_event.finish_time:
							future_event = event_list[i + events_while_processing]
							if cache.search(future_event.file_id[0]) != -1:
								if future_event.finish_time is None:
									cache_hit_rate+= 1
									future_event.finish_time = future_event.arrival_time + future_event.size[0] / R_c								
						events_while_processing += 1
					current_time += processing_time
		rtt = sum((event.finish_time - event.arrival_time) for event in event_list) / len(event_list)
		if policy == "LFU":
			lfu_rtt = rtt
		elif policy == "MRU":
			mru_rtt = rtt
		else:
			lru_rtt = rtt
		print(rtt)
	
	return (lfu_rtt, mru_rtt, lru_rtt)
if __name__ == "__main__":
	res = input("Type Example or Interactive: ")
	if res == "Example":
		print(test(2, 200, 1.5, 1.5, 5000, 100, 1000, 20))
	
	elif res == "Big Test":
		print("Begin lambda test")
		lfu_vals = []
		mru_vals = []
		lru_vals = []
		#ten data points
		for i in range(1,10):
			#five test of each
			print("iteration: ",i)
			lfu_temp = 0
			mru_temp = 0
			lru_temp = 0
			for j in range(0,5):
				res = test(i, 200, 1.5, 1.5, 2000, 100, 1000, 20)
				lfu_temp += res[0]
				mru_temp += res[1]
				lru_temp += res[2]
				print(lfu_temp)
				print(mru_temp)
				print(lru_temp)
			lfu_temp = lfu_temp/5
			mru_temp = mru_temp/5
			lru_temp = lru_temp/5
			lfu_vals.append(lfu_temp)
			mru_vals.append(mru_temp)
			lru_vals.append(lru_temp)

		x = [1,2,3,4,5,6,7,8,9]
		plt.title("Lambda vs MTT")
		plt.xlabel("Lambda value")
		plt.ylabel("MTT(s)")
		plt.plot(x, lru_vals, label="LRU")
		plt.plot(x,lfu_vals, label="LFU")
		plt.plot(x,mru_vals, label="MRU")
		plt.legend()
		plt.show()

	else:
		try:
			lamb = float(input("Enter the value for lambda: "))
			num_files = int(input("Enter the number of possible files: "))
			alpha_s = float(input("Enter the value for alpha_s > 1: "))
			alpha_p = float(input("Enter the value for alpha_p > 1: "))
			num_requests = int(input("Enter the number of requests to the server: "))
			cache_capacity = int(input("Enter the capacity of the the cache in MB(must be an integer): "))
			R_c = float(input("Enter the cache speed in MB/s: "))
			R_a = float(input("Enter the network speed in MB/s: "))
			test(lamb, num_files, alpha_s, alpha_p, num_requests, cache_capacity, alpha_p, alpha_s)
		except:
			print("Invalid parameters")
	