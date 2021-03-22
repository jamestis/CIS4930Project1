#takes parameters: lambda, number of files N, F_s params, F_p params,
#consts: access link bandwidth Ra, round trip prop time btw network and serv D, institution network bandwidth Rc
#in cache response time : S_i / R_c
#not in cache = D+ Qd + Si / Ra + Si / Rc
#outputs = avg rtt

import sys

class Event:
    def __init__(self, arrival_time, size, id,):
        self.arrival_time = arrival_time
        self.size = size
        self.id = id

if len(sys.argv) != 7:
    print("Program requires 6 command line arguments")
    exit()

#require number values
#order : lambda, num files, mu_s, k_s, mu_p, k_p,
for i in range(1,7):
    try:
        float(sys.argv[i])
        print(float(sys.argv[i]))
    except ValueError:
        print("All arguments must be convertable to type float.")
        exit()

lamb = float(sys.argv[1])
num_files = int(sys.argv[2])
mu_s = float(sys.argv[3])
if not (mu_s > 1):
    print("mu_s must be greater than 1.")
    exit()
k_s = float(sys.argv[4])
mu_p = float(sys.argv[5])
if not (mu_p > 1):
    print("mu_p must be greater than 1.")
t = Event(0,0,0)
print(t.size)
exit()