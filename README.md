
#takes parameters: lambda, number of files N, alpha_s, alpha_p, FIXME: add finish event.
#consts: access link bandwidth Ra, round trip prop time btw network and serv D, institution network bandwidth Rc
#in cache response time : S_i / R_c
#not in cache = D+ Qd + Si / Ra + Si / Rc
#outputs = avg rtt


#TODO: 
# 1. Add event finished to event object
# 2. Add policy enumeration to event class to support differemt cache policy operator overloading
# 3. More in depth exploring of cache replacement policies, possible change in splay-tree data structure
# 4. Double check validity of poisson process generation and pareto dist. sampling 
# 5. When looping through events, bet sure to skip to the maxmium(next_event.time, current_time + event.service_time)