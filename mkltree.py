import math
import hashlib


class MklTree:
    def __init__(self, trans_list):
        self.trans_list = self.create_child(trans_list)
        self.hash_tree = self.add_mkl_tree(self.trans_list)

    @staticmethod
    def create_child(trans_list):
        length = len(trans_list)
        l = 2 ** (math.ceil(math.log2(length)))
        if l > length:
            li = ['dummy' for _ in range(l - length)]
            trans_list.extend(li)
        return trans_list

    @staticmethod
    def add_mkl_tree(trans_list):
        """create merkel tree from list of transactions or data"""
        ln = len(trans_list)
        level = int(math.log2(ln))
        n = 2 ** (level + 1) - 1
        mkl_list = [None for _ in range(n)]
        for i in range(ln):
            mkl_list[ln - 1 + i] = hashlib.sha256(str(trans_list[i]).encode()).hexdigest()

        while level > 0:
            for k in range(0, 2 ** level, 2):
                index = 2 ** level - 1
                parent = (index + k) // 2
                hash_str = str(mkl_list[index + k]) + str(mkl_list[index + k + 1])
                mkl_list[parent] = hashlib.sha256(hash_str.encode()).hexdigest()
            level -= 1
        return mkl_list
