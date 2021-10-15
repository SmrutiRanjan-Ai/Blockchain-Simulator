import global_function as g
import des
import random as r
import node
import block
import transaction
import proof
from numpy import random, round_
import selfishnode
import stubbornnode
t = g.INITIAL_TIMESTAMP


# Construct Nodes
def node_constructor(n, z):
    z_limit = int(z * n)
    for i in range(n):
        if i + 1 < z_limit:
            bandwidth = 'SLOW'
        else:
            bandwidth = 'FAST'
        n = node.Node(g.INITIAL_TIMESTAMP, g.NODE_START_ID + i + 1, bandwidth)
        g.node_list.append(n)
    g.create_peers()
    if g.selfish and not g.stubborn:
        attacker=selfishnode.SelfishNode(g.INITIAL_TIMESTAMP, 99 , 'FAST')
        g.create_attacker_peers(attacker)
        g.node_list.append(attacker)
    elif not g.selfish and g.stubborn:
        attacker=stubbornnode.StubbornNode(g.INITIAL_TIMESTAMP, 99 , 'FAST')
        g.create_attacker_peers(attacker)
        g.node_list.append(attacker)
    for n in g.node_list:
        li = list(n.peers)
        for p in li:
            rho_ij = random.uniform(g.rho_lower_limit, g.rho_upper_limit) / 1000
            n.rho[p.id] = rho_ij
        print(n, "connected to", *n.peers)


# Generate Gensis
def genesis_block(node_list):
    list_trans = []
    for n in node_list:
        txn = transaction.Txn(g.GENESIS, n.id, g.START_AMOUNT, 0)
        list_trans.append(txn)
    genesis = block.Block(0, list_trans, g.GENESIS, 0, g.VERSION, g.GENESIS)
    proof.proof_of_work(genesis)
    print("Genesis Created\t", genesis.header['block_hash'])
    for n in node_list:
        n.create_blockchain(genesis)


# Generate Txn
def random_txn_generator(node_list):
    timestamp = t
    for i in range(g.TXN_NUM):
        timestamp += random.exponential(scale=g.txn_interarrival, size=None)
        sender, receiver = r.sample(node_list, 2)
        amount = round_((r.random()) * 50, 3)
        event = node.Event(timestamp, [sender.create_trans, timestamp, sender, receiver, amount])
        des.heapq.heappush(des.q, event)
    g.final_timestamp = timestamp


node_constructor(g.NODES, g.SLOW_PROBABILITY)
genesis_block(g.node_list)

random_txn_generator(g.node_list)
des_status = True
# Customize Terminal Output in global_function.Py
# DES
while des.q:
    obj = des.heapq.heappop(des.q)
    t = obj.timestamp
    obj = obj.args
    args = obj[1:]
    obj[0](*args)

if g.selfish and g.attackers_add_end_blocks:
    selfish_node=g.node_list[-1]
    if selfish_node.private_branch:
        selfish_node.end_broadcast(t)

# visualization
for i in g.node_list:
    print(i)
    i.blockchain.visualize_tree()

# debug only
for i in g.node_list:
    chain = i.blockchain.tree.longest_chain()
    chain_list=i.blockchain.get_chain_trans_list(chain)
    if i.mempool:
        for j in i.mempool:
            if j in chain:
                print(j, True)
            else:
                print(j, False)
    else:
        print(i, "Mempool empty")


#block percentage in Main Chain

chain_blk=g.node_list[0].blockchain.tree.longest_chain()
len_chain=len(chain_blk)

for i in g.node_list:
    num=0
    for j in chain_blk:
        if i.id==j.header['creator']:
            num+=1
    print("Pecrentage of Node ",i,"=",num/len_chain,"Hash Power is ",i.hash_power,i.bandwidth)

for n in g.node_list:
    chain=n.blockchain.tree.longest_chain()
    conf_trans_list = n.blockchain.get_chain_trans_list(chain)
    if len(conf_trans_list)==len(set(conf_trans_list)):
        print(n," No double spend")
if g.selfish or g.stubborn:
    attacker=g.node_list[-1]
    main_chain=g.node_list[0].blockchain.tree.longest_chain()
    #print MPU_node_adversary
    print("Total number of blocks mined by an adversary", attacker.block_qty)
    num_main_chain=len(main_chain)
    num_attacker_blocks=0
    for i in main_chain:
        if attacker.id==i.header['creator']:
            num_attacker_blocks+=1
    print("Number of block mined by an adversary in main chain", num_attacker_blocks)
    print("MPU_node_adversary=",num_attacker_blocks/attacker.block_qty)

    #print MPU_node_overall:
    total_blocks=len(set(g.node_list[0].blockchain.tree_traverse_blkid()))
    print("Total number of blocks in main chain", num_main_chain)
    print("Total number of blocks generated across all the nodes", total_blocks)
    print("MPU_node_overall=",num_main_chain/total_blocks)