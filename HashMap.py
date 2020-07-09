class LinkedListNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

class HashMap:
    '''
    目标：
    用数组和hash函数设计一个各项操作的时间复杂度为O(1)的hashMap
    
    1. 计算hash和bucket_index
    2. 设计不用rehash的put
    3. 设计get
    4. 设计rehash 和 利用rehash的put(引入load_factor概念)
    5. 设计一个删除函数
    '''
    def __init__(self, initial_size = 10):
        self.num_entries = 0 #当前具有的条目数，注意load factor 为0.7
        self.p = 31
        self.bucket_array = [None for _ in range(initial_size)]

    def put(self, key, value):
        pass
        
    
    def get(self, key):
        pass
            
    
    def get_bucket_index(self, key):
        return self.get_hash_code(key)
    
    def get_hash_code(self, key):
        """
        # 由于modular mutiplication性质 
        # 循环中的这两次 % num_buckets 不影响最后的结果，只是保证不会数值巨大罢了。
        """
        key = str(key)
        num_buckets = len(self.bucket_array)
        
        current_coef = 1
        hash_code = 0
        
        for char in key:
            hash_code += ord(char) * current_coef
            hash_code = hash_code % num_buckets
            current_coef *= self.p
            current_coef = current_coef % num_buckets
        
        return hash_code % num_buckets
    
    def size(self):
        return self.num_entries
    
    # Helper function to see the hashmap
    def __repr__(self):
        output = "\nLet's view the hash map:"

        node = self.bucket_array
        for bucket_index, node in enumerate(self.bucket_array):
            if node is None:
                output += '\n[{}] '.format(bucket_index)
            else:
                output += '\n[{}]'.format(bucket_index)
                while node is not None:
                    output += ' ({} , {}) '.format(node.key, node.value)
                    if node.next is not None:
                        output += ' --> '
                    node = node.next
                    
        return output

# Test delete operation
hash_map = HashMap(10)
print(hash_map.get_bucket_index("abcd"))