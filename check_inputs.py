#input validation
#order is: lambda, num_files, alpha_s, alpha_p, num_requests, cache_capacity, R_c, R_a
import sys
#FIXME: Number of reqs?
def check_inputs(args):
    if len(sys.argv) != 9:
        print("Program requires 8 command line arguments: lambda, number of files, alpha_s, alpha_p, num_requests, cache_capacity, R_c, R_a")
        exit()
    for i in range(1,9):
        try:
            float(sys.argv[i])
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

    num_requests = int(sys.argv[5])
    cache_capacity = float(sys.argv[6])
    R_c = float(sys.argv[7])
    R_a = float(sys.argv[8])
    return [lamb,num_files, alpha_s,alpha_p, num_requests,cache_capacity,R_c,R_a]