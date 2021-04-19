from main import main
from check_inputs import check_inputs
import numpy as np

def run():
	num_files = 1000
	num_requests = 10000
	R_c_init = 10
	R_a_init = 5
	cache_cap = 100
	MRU_rtts =np.zeros((20, 20, 20, 10))
	#50 values of each parameters, 125000 calls each
	lamb = 1.1
	for lamb_iter in range(1, 20):
		R_c_init = 10
		R_a_init = 5
		for alpha_s in range(1,20):
			for alpha_p in range(1, 20):
				for R_c_iter in range(1,10):
					print("")
					print("lamb = {}".format(lamb))
					print("alpha_s = {}".format(1 + alpha_s/ 10))
					print("alpha_p = {}".format(1 + alpha_p /10))
					print("R_c = {}".format(R_c_init + 5 * R_c_iter))
					print("R_a = {}".format(R_a_init + 2 * R_c_iter))
					MRU_rtts[lamb_iter][alpha_s][alpha_p][R_c_iter] = main(lamb, num_files, 1 + alpha_s/10, 1 + alpha_p /10, num_requests, 100, R_c_init + 5 * R_c_iter, R_a_init + 2 * R_c_iter, "LRU")
		lamb += .3
	return MRU_rtts
if __name__ == "__main__":
	run()
