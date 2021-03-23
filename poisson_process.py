#credit to https://gist.githubusercontent.com/sachinsdate/d48abefe2f75541c7d98f51599c927b0/raw/885d39ca60e80f7da5963b2a8c7bc08d41d407a1/poisson_sim.py
import random
import math
def poisson_process(lamb, num_arrivals):
	res = []
	arrival_time = 0
	for i in range(num_arrivals):
		p = random.random()
		_inter_arrival_time = -math.log(1.0-p)/lamb
		arrival_time = arrival_time + _inter_arrival_time
		res.append(arrival_time)
	return res

