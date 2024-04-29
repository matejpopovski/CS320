class Node():
    def __init__(self, key):
        self.key = key
        self.values = []
        self.left = None
        self.right = None
        
    def __len__(self):
        size = len(self.values)
        if self.left != None:
            size += len(self.left)
        if self.right != None:
            size += len(self.right)
        return size
    
    def lookup(self, target):
        if self.key == target:
            return self.values
        if target < self.key and self.left != None:
            return Node.lookup(self.left, target)
        if target > self.key and self.right != None:
            return Node.lookup(self.right, target)
        else:
            return []
        
class BST():
    def __init__(self):
        self.root = None

    def add(self, key, val):
        if self.root == None:
            self.root = Node(key)

        curr = self.root
        while True:
            if key < curr.key:
                # go left
                if curr.left == None:
                    curr.left = Node(key)
                curr = curr.left
            elif key > curr.key:
                 # go right
                if curr.right == None:
                    curr.right = Node(key)
                curr = curr.right
                
            else:
                # found it!
                assert curr.key == key
                break

        curr.values.append(val)
        
    def __dump(self, node):
        if node == None:
            return
        self.__dump(node.left)            # 1
        print(node.key, ":", node.values)  # 2
        self.__dump(node.right)             # 3

    def dump(self):
        self.__dump(self.root)
        
    def __getitem__(self, item):
        return self.root.lookup(item)

    def get_height(self, node):
        if node is None or (node.left is None and node.right is None):
          return 1
        return 1 + max(self.get_height(node.left), self.get_height(node.right))

    def num_nonleaf_nodes(self, node=None):
        if node is None:
            return 0
        if node is None or (node.left is None and node.right is None):
            return 0
        count = 0
        if node.left is not None or node.right is not None:
            count += 1
        count += self.num_nonleaf_nodes(node.left)
        count += self.num_nonleaf_nodes(node.right)
        return count

    def node_counter(self, node=None):
      if node is None:
          return 0
      return self.node_counter(node.left) + self.node_counter(node.right) + 1

    def top_n_keys(self, n, node=None):
        # A recursive method that can return the top N keys for any subtree
        if node is None:
            node = self.root
        result = []
        self.__top_n_keys_helper(node, n, result)
        return result

    def __top_n_keys_helper(self, node, n, result):
        # Helper method for the reverse in-order traversal
        if node is None or len(result) >= n:
            return
        self.__top_n_keys_helper(node.right, n, result)
        if len(result) < n:
            result.append(node.key)
        self.__top_n_keys_helper(node.left, n, result)
    
    