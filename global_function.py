import random

node_list = []
ID = 0  # start transaction id index
blk_list = set()  # set of all blkids
id_list = []
COMMISSION_LIMIT = 0
NODE_START_ID = 100
# Number of Nodes
NODES = 20
NODES_MINING_TIME_DIFF = 0
INITIAL_TIMESTAMP = 0
VERSION = '1.0'
GENESIS = 0
START_AMOUNT = 50
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

'''Terminal Customization'''
message_log = False
message_blk_log = False
create_trans_log = False
trans_log = False
mining_log = False
mining_log_detail = False
mempool_log = False
final_timestamp=None


def get_trans_id():
    """generate unique sequential transids"""
    if not id_list:
        id_list.append(ID)
    else:
        id_list.append(id_list[-1] + 1)
    return id_list[-1]


def create_peers():
    '''Create Peers'''
    for n in node_list:
        peers_num = random.randint(3, NODES - 1)
        for i in range(peers_num):
            while True:
                p = random.choice(node_list)
                if p != n:
                    n.peers.add(p)
                    p.peers.add(n)
                    break


def create_attacker_peers(attacker):
    '''Create Peers for attackers'''
    peers_num = int(zeta * NODES)
    for i in range(peers_num):
        p = random.choice(node_list)
        attacker.peers.add(p)
        p.peers.add(attacker)


def blkid_gen():
    """generate unique blk id"""
    while True:
        n = int((random.uniform(1, 10) * 100000000000))
        if n in blk_list:
            continue
        blk_list.add(n)
        return n
