#takes parameters: lambda, number of files N, F_s params, F_p params,
#consts: access link bandwidth Ra, round trip prop time btw network and serv D, institution network bandwidth Rc
#in cache response time : S_i / R_c
#not in cache = D+ Qd + Si / Ra + Si / Rc
#outputs = avg rtt

import sys
import os
import numpy
import pareto_random_samples
import Event


#input validation
#order is: lambda, num_files, mu_s, k_s, mu_p, k_p
def check_inputs(args):
    if len(sys.argv) != 5:
        print("Program requires 4 command line arguments: lambda, number of files, alpha_s, alpha_p")
        exit()
    for i in range(1,5):
        try:
            float(sys.argv[i])
            print(float(sys.argv[i]))
        except ValueError:
            print("All arguments must be convertable to type float or int.")
            exit()

    lamb = float(sys.argv[1])
    num_files = int(sys.argv[2])
    alpha_s = float(sys.argv[3])
    if alpha_s <= 1:
        print("Alpha_s must be greater than 1.")
        exit()
    alpha_p = float(sys.argv[4])
    if alpha_p <=1 :
        print("Alpha_p must be greater than 1.")
        exit()
    return [lamb,num_files, alpha_s,alpha_p]

check_inputs(sys.argv)
exit()