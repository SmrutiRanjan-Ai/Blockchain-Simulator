import sys
import des
import global_function as g
from blockchain import Blockchain
from transaction import Txn
from numpy import random
from objsize import get_deep_size

lag = 0.00001


class Message:
    def __init__(self, message_type, content):
        self.type = message_type
        self.content = content
        self.id = random.randint(1, 1000000)
        if self.type == 'blk':
            # Calculate SIze of Message
            self.size = get_deep_size(self.content)
        else:
            self.size = sys.getsizeof(self) * 8

    def __str__(self):
        return str(self.content)


class Node:
    def __init__(self, creation_time, node_id, bandwidth):
        self.id = node_id
        self.creation_time = creation_time
        self.bandwidth = bandwidth
        self.rho = {}
        self.peers = set()
        self.mempool = set()
        self.completed = set()
        self.message_sent_list = {}
        self.busy = False
        self.blockchain = None
        self.hash_power = g.random.choice(['high', 'low'])
        if self.hash_power == 'high':
            self.hash_mean = g.hashing_power_high_mean
        else:
            self.hash_mean = g.hashing_power_low_mean
        self.pending_block = None
        self.mempool_limit = min(g.TXN_NUM / 10, 1000)
        print(self.id, " created at t=\t", self.creation_time)
        self.chain = None
        self.received_blk = set()
        self.type = 'honest'

    def __str__(self):
        return str(self.id)

    def create_blockchain(self, genesis):
        '''Initialize Blockchain'''
        self.blockchain = Blockchain(genesis)
        self.chain = self.blockchain.tree.longest_chain()

    def create_trans(self, timestamp, sender, receiver, amount, commission=0):
        '''Create Transaction and add to mempool and BroadCast Them'''
        txn = Txn(sender, receiver, amount, commission)
        self.mempool.add(txn)
        self.broadcast_txn(timestamp + lag, txn)
        if g.create_trans_log:
            print(timestamp, txn, "Created")
        event = Event(timestamp, [self.check_mempool, timestamp + lag])
        des.heapq.heappush(des.q, event)

    def verify_txn(self, conf_trans_list, txn):
        ''' Verify Transaction'''
        if self.blockchain.verify_trans_balance(conf_trans_list, txn.amount, txn.sender):
            return True
        else:
            if g.create_trans_log:
                print(txn, "Rejected")
            return False

    def check_mempool(self, timestamp):
        ''' Check mempool to add into block and trigger mining of block'''
        if not self.busy:
            if g.mempool_log:
                print(self.id, "mempool is ", *self.mempool)
            if timestamp > 0.98 * g.final_timestamp:
                self.mempool_limit = g.TXN_NUM / 100
            if timestamp > 0.99 * g.final_timestamp:
                self.mempool_limit = 0
            if len(self.mempool) > self.mempool_limit:
                self.chain = self.blockchain.tree.longest_chain()
                self.create_block(timestamp, self.chain)

    def broadcast_txn(self, timestamp, txn):
        message = Message('txn', txn)
        self.broadcast_message(timestamp, message, self)

    def broadcast_blk(self, timestamp, blk):
        message = Message('blk', blk)
        self.broadcast_message(timestamp, message, self)

    def broadcast_message(self, timestamp, message, sender=None):
        '''This function create a event that sends txn to its peers'''
        m_id = message.id
        li = list(self.peers)
        random.shuffle(li)
        if m_id not in self.message_sent_list:
            self.message_sent_list[m_id] = []
            if g.message_log:
                print(timestamp, self, "Sends Message(", m_id, message, ") to ", end="")
            m = message.size
            for j in li:
                peer_id = j.id
                if peer_id != sender.id:
                    if peer_id not in self.message_sent_list[m_id]:
                        peer_bandwidth = j.bandwidth
                        rho_ij = self.rho[peer_id]
                        latency = self.get_latency(self.bandwidth, peer_bandwidth, rho_ij, m)
                        t = timestamp + latency
                        if g.message_log: print(j.id, end=" ")
                        self.message_sent_list[m_id].append(peer_id)
                        if g.message_log and message.type == "blk":
                            print(timestamp, self, "Sends Message(", m_id, message, ") to ", j)
                        event = Event(t, [j.receive_message, t, message, self])
                        des.heapq.heappush(des.q, event)

            if g.message_log: print()

    @staticmethod
    def get_latency(i_bandwidth, j_bandwidth, rho_ij, m):
        '''Calculate Latency'''
        if i_bandwidth == 'FAST' and j_bandwidth == 'FAST':
            c = g.C_FAST
        else:
            c = g.C_SLOW
        d = random.exponential(scale=g.D_CONSTANT / c, size=None)
        l = rho_ij + m / c + d
        return l

    def receive_message(self, timestamp, message, sender):
        '''Receive Message'''
        if message.type == 'txn':
            if message.content not in self.mempool:
                self.mempool.add(message.content)
            self.broadcast_message(timestamp, message, sender)
            if g.message_log: print(timestamp, self, " Received Transaction", message.content, "from ", sender.id)
        if message.type == 'blk':
            if message.content not in self.received_blk:
                if g.message_blk_log: print(timestamp, self, " Received Block", message.content, "from ", sender.id)
                self.received_blk.add(message.content)
                self.receive_blk(timestamp, message.content, sender)
                event = Event(timestamp + lag, [self.broadcast_message, timestamp + lag, message, sender])
                des.heapq.heappush(des.q, event)

    def receive_blk(self, timestamp, block, sender):
        '''Receive Block'''
        if sender.type == 'selfish':
            print(timestamp, self, "honest recieved selifsh block", block)
        status, code = self.blockchain.add_block_to_chain(block, timestamp)
        if g.mining_log:
            print(timestamp, self, block.header['blkid'], status, code)

        if status:
            self.check_completed_trans()
            self.stop_mining(timestamp, block)
        else:
            print(code)

    def stop_mining(self, timestamp, block):
        '''Stop Mining If a corresponding valid block is received'''
        if self.pending_block is not None:
            prev_hash = self.pending_block.header['prev_hash']
            if block.header['prev_hash'] == prev_hash:
                if self.pending_block.header['timestamp'] - timestamp > g.NODES_MINING_TIME_DIFF:
                    self.pending_block = None
                    self.busy = False
                    event = Event(timestamp + lag, [self.check_mempool, timestamp + lag])
                    des.heapq.heappush(des.q, event)

    def check_completed_trans(self, chain=None):
        ''' Remove Trans after adding block to chain'''
        if chain is None:
            chain = self.blockchain.tree.longest_chain()
        valid_trans_list = self.blockchain.get_chain_trans_list(chain)
        li = list(self.mempool)
        for i in valid_trans_list:
            if i in li:
                self.mempool.discard(i)

    def check_double_spending(self):
        valid_trans_id = self.blockchain.get_longest_chain_trans_list()
        if len(valid_trans_id) != len(set(valid_trans_id)):
            print(valid_trans_id)
            print(set(valid_trans_id))
            print("Double Spend Attack")
            raise NameError('Block Integrity Violated')

    def create_block(self, timestamp, chain=None):
        """Selection of transaction and Mining of block happens here"""
        if chain is None:
            chain = self.blockchain.tree.longest_chain()
        new_blkid = g.blkid_gen()
        mem_pool_list = list(self.mempool)
        conf_trans_list = self.blockchain.get_chain_trans_list(chain)
        last_block = self.blockchain.last_block(chain)
        txn_list = [i for i in mem_pool_list if i not in conf_trans_list]
        txn_list = [i for i in txn_list if self.verify_txn(conf_trans_list, i)]
        prev_hash = last_block.header['block_hash']
        new_timestamp = random.exponential(scale=self.hash_mean, size=1)[0] + timestamp
        if txn_list:
            if g.mining_log_detail:
                print(timestamp, "\tmining of ", new_blkid, " started by\t", self.id, "\t")

            status, new_block = self.blockchain.create_block(blkid=new_blkid, list_trans=txn_list[0:100], \
                                                             timestamp=new_timestamp, version=g.VERSION,
                                                             creator=self.id, prev_hash=prev_hash)
            if status:
                self.busy = True
                self.pending_block = new_block
                event = Event(new_timestamp, [self.add_block, new_timestamp, new_block.header['blkid']])
                des.heapq.heappush(des.q, event)

    def add_block(self, timestamp, blkid):
        ''' Add a block after mining'''
        block = self.pending_block
        if block is not None:
            if block.header['blkid'] == blkid:
                status, code = self.blockchain.add_block_to_chain(block, timestamp)
                if status:
                    print(timestamp, self, "mined", block)
                chain = self.blockchain.tree.longest_chain()
                self.check_completed_trans(chain)
                timestamp += lag
                message = Message('blk', block)
                self.broadcast_message(timestamp, message, self)
        self.pending_block = None
        self.busy = False
        event = Event(timestamp + lag, [self.check_mempool, timestamp + lag])
        des.heapq.heappush(des.q, event)


class Event:
    def __init__(self, timestamp, args):
        self.timestamp = timestamp
        self.args = args

    def __str__(self):
        print(self.timestamp, *self.args)
        return str()

    def __le__(self, other):
        if self.timestamp <= other.timestamp:
            return True
        else:
            return False

    def __lt__(self, other):
        if self.timestamp < other.timestamp:
            return True
        else:
            return False

    def __ge__(self, other):
        if self.timestamp >= other.timestamp:
            return True
        else:
            return False

    def __gt__(self, other):
        if self.timestamp > other.timestamp:
            return True
        else:
            return False
