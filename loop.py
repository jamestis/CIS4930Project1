from main import main
from check_inputs import check_inputs
import numpy as np
import pickle

def run():
	num_files = 1000
	num_requests = 10000
	MRU_rtts = np.zeros((20, 10, 10, 20, 10, 10))
	LRU_rtts = np.zeros((20, 10, 10, 20, 10, 10))
	FIFO_rtts = np.zeros((20, 10, 10, 20, 10, 10))
	LIFO_rtts = np.zeros((20, 10, 10, 20, 10, 10))
	
	for lamb_iter in range(0, 20):
		for alpha_s_iter in range(0,10):
			for alpha_p_iter in range(0,10):
				for cache_capacity_iter in range(0,20):
					for R_c_iter in range(0,10):
						for R_a_iter in range(0,10):
							for i in range(0,10):
								print("Running")
								MRU_rtts[lamb_iter][alpha_s_iter][alpha_p_iter][cache_capacity_iter][R_c_iter][R_a_iter] += main(1 + .5 * lamb_iter, num_files, 1.01 + alpha_s_iter / 10, 1.01 + alpha_p_iter/10, num_requests, 20 + 20 * cache_capacity_iter, 5 + 5 * R_c_iter, 2 + 2 * R_a_iter, "MRU")
								LRU_rtts[lamb_iter][alpha_s_iter][alpha_p_iter][cache_capacity_iter][R_c_iter][R_a_iter] += main(1 + .5 * lamb_iter, num_files, 1.01 + alpha_s_iter / 10, 1.01 + alpha_p_iter/10, num_requests, 20 + 20 * cache_capacity_iter, 5 + 5 * R_c_iter, 2 + 2 * R_a_iter, "LRU")
								FIFO_rtts[lamb_iter][alpha_s_iter][alpha_p_iter][cache_capacity_iter][R_c_iter][R_a_iter] += main(1 + .5 * lamb_iter, num_files, 1.01 + alpha_s_iter / 10, 1.01 + alpha_p_iter/10, num_requests, 20 + 20 * cache_capacity_iter, 5 + 5 * R_c_iter, 2 + 2 * R_a_iter, "FIFO")
								LIFO_rtts[lamb_iter][alpha_s_iter][alpha_p_iter][cache_capacity_iter][R_c_iter][R_a_iter] += main(1 + .5 * lamb_iter, num_files, 1.01 + alpha_s_iter / 10, 1.01 + alpha_p_iter/10, num_requests, 20 + 20 * cache_capacity_iter, 5 + 5 * R_c_iter, 2 + 2 * R_a_iter, "LIFO")

	with open('MRU_rtts.npy', 'wb') as f:
		np.save(f, MRU_rtts)
	with open('LRU_rtts.npy', 'wb') as f:
		np.save(f, LRU_rtts)
	with open('FIFO_rtts.npy', 'wb') as f:
		np.save(f, FIFO_rtts)
	with open('LIFO_rtts.npy', 'wb') as f:
		np.save(f, LIFO_rtts)
	
	
if __name__ == "__main__":
	run()
