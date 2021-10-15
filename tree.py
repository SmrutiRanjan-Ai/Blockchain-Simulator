import global_function as g


class Tree:
    def __init__(self, root_node):
        self.root=TreeNode(root_node,0)

    def add_tree_node(self, block,timestamp):
        prev_hash = block.header['prev_hash']
        stack = [self.root]
        while stack:
            parent = stack.pop()
            if parent.header['block_hash'] == prev_hash:
                code=parent.header['blkid'], "parent id found"
                node=TreeNode(block,timestamp)
                parent.adj_matrix.append(node)
                return True,code
            else:
                for child in parent.adj_matrix:
                    stack.append(child)
        code="parent not found", block.header["blkid"], block.header["prev_hash"]
        return False,code

    def check_node_hash(self, prev):
        stack = [self.root]
        while stack:
            parent = stack.pop()
            if parent.header['block_hash'] == prev:
                if parent.adj_matrix:
                    if g.mining_log_detail: print(parent.header['blkid'], " has child", parent.adj_matrix)
                    return True
                else:
                    if g.mining_log_detail: print(parent.header['blkid'], " has no child", parent.adj_matrix)
                    return False
            for child in parent.adj_matrix:
                stack.append(child)
        return False

    def longest_chain(self):
        chain = self.longest_path(self.root)
        new_chain=[]
        for i in chain:
            new_chain.append(i.block)
        new_chain.reverse()
        return new_chain

    def longest_path(self, root):
        if root is None:
            return []
        path_list = []
        if not root.adj_matrix:
            path_list.append(root)
            return path_list
        for i in root.adj_matrix:
            path_list.append(self.longest_path(i))
        max_path = []
        for i in path_list:
            if len(i) > len(max_path):
                max_path = i
            elif len(i) == len(max_path):
                if i[-1].rec_timestamp<max_path[-1].rec_timestamp:
                    max_path=i
        max_path.append(root)
        return max_path

class TreeNode:
    def __init__(self,block,timestamp):
        self.header=block.header
        self.adj_matrix=[]
        self.mkl_tree=block.mkl_tree
        self.block=block
        self.rec_timestamp=timestamp




