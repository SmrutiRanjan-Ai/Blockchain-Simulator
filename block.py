import mkltree as mk
import sys


class Block:
    """initiates Block"""

    def __init__(self, prev_hash, list_trans, blkid, timestamp, version, creator):
        self.mkl_tree = mk.MklTree(list_trans)
        self.header = {'prev_hash': prev_hash, 'mkl_root': self.mkl_tree.hash_tree[0], 'block_hash': None,
                       'nonce': None, 'timestamp': timestamp,
                       'blkid': blkid, 'creator': creator}
        self.VERSION = version
        self.adj_matrix = None

    def __str__(self):
        return "(" + str(self.header['creator']) + ' Blkid- ' + str(self.header['blkid']) + " prev "+ \
                str(self.header['prev_hash']) + " block Hash "+str(self.header['block_hash'])+")"
