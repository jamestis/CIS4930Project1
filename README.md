Execution instructions:
clone this repo @ https://github.com/jamestis/CIS4930Project1.git
cd CIS4930Project1
install deps: pip3 install numpy scipy matplotlib
execute: python3 main.py # # # # # # # #
takes command line arguments in the following order: lamb,num_files, alpha_s,alpha_p, num_requests,cache_capacity,R_c,R_a
current output: print event handling and results in the terminal.

#TODO: 
# 1. Parameterize DS used for caching so we do not need multiple objects, or inherit
# 2. Add policy enumeration to event class to support differemt cache policy oroperator overloading
# 3. More in depth exploring of cache replacement policies, possible change in splay-tree data structure
# 4. Double check validity of poisson process generation and pareto dist. sampling 
# 5. When looping through events, bet sure to skip to the maxmium(next_event.time, current_time + event.service_time)
