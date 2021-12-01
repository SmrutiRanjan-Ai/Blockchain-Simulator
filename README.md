
Smruti Ranjan Behera 
Saurish D
Hrithik

Run main.py
Adjust parameters in Global Function
To run Selfish Mining make global_function.py selfish=True
To run Stubborn Mining make global_function.py Stubborn=True
Note: Both Must be Not be true at the same time

global_function.py Parameters:
Number of Nodes
NODES 

Number of Transaction
TXN_NUM = 1000

# Network Parameters

C_FAST = 100000000  # 100mbps = 100 * 10^6 bits 

C_SLOW = 5000000  # 5mbps = 5 * 10^6 bits

D_CONSTANT = 96000  # 96 Kilobits Queueing Delay in bits

SLOW_PROBABILITY = 0.5  # Z

txn_interarrival = 10  # Exponential distribution mean time T_tx

rho_upper_limit = 500  # in milliSeconds

rho_lower_limit = 10  # in milliSeconds

hashing_power_high_mean = 400  # Tk - lower is faster/better

hashing_power_low_mean = 800  # Tk - higher is slower/better

# Attacker Mining Parameters
selfish = False  # True if want to do only Selfish Mining

stubborn = True  # True if want to do only Stubborn Mining

attackers_add_end_blocks = True  # Add private blocks to blockchain at the end of simulation

adversary_mining_power = 50  # lower is higher

zeta = 0.5  # ζ = 25%, 50%, 75%

#Customize Terminal Output Here:

message_log = False

message_blk_log = False

create_trans_log = False

trans_log = False

mining_log = False

mining_log_detail = False

mempool_log = False


