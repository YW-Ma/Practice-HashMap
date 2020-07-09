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
        self.load_factor = 0.7
        self.bucket_array = [None for _ in range(initial_size)]

    '''
    Separate chaining:
    In case of collision, the `put()` function uses the same bucket to store 
    a linked list of key-value pairs. 
    Every bucket will have it's own separate chain of linked list nodes.
    '''  
    def put(self, key, value):
        '''
        key: "zipcode"
        value: 518052
        bucket_index: 0
        '''
        # 1. 计算bucket_index
        index = self.get_bucket_index(key)
        # 2. 如果key已在bucket存在，则更新它的value并返回
        head = self.bucket_array[index]
        while head is not None:
            if head.key == key:
                head.value = value
                return
            head = head.next
        # 3. 如果key未在bucket存在，则prepend一个节点，并节点数加一
        #    实际上，无论有无collision都是同样的操作。 只不过无collision时head是None
        new_node = LinkedListNode(key, value)
        head = self.bucket_array[index]
        new_node.next = head
        self.bucket_array[index] = new_node
        self.num_entries += 1
        # 4. check for load factor 看看是不是n/b > 0.7 该扩容了
        current_load_factor = self.num_entries / len(self.bucket_array)
        if current_load_factor > self.load_factor:
            self.num_entries = 0
            self._rehash()
        
    
    def get(self, key):
        # 查找的时候要遍历bucket中的链表。如果找到key一样的就返回。
        # 1. 计算bucket_index
        index = self.get_bucket_index(key)
        # 2. 在bucket里面找有没有对应的key
        head = self.bucket_array[index]
        while head is not None:    
            #    如果有对应的，就返回value
            if head.key == key:
                return head.value
            head = head.next
            
    
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
    
    def _rehash(self):
        '''
        扩容 + 转移
        '''
        old_capacity = len(self.bucket_array)
        new_capacity = 2 * old_capacity
        
        old_buckets = self.bucket_array
        self.bucket_array = [None for _ in range(new_capacity)]
        for head in old_buckets:
            while head is not None:
                key = head.key
                value = head.value
                self.put(key, value)  # 直接调用put就好了。不用重新写。
                head = head.next

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

# Test Rehashing

# We have reduced the size of the hashmap array to increase the load factor (> 0.7) 
# and hence trigger the rehash() function
hash_map = HashMap(3)                        

hash_map.put("one", 1)
hash_map.put("two", 2)
hash_map.put("three", 3)
hash_map.put("neo", 11)

print("size: {}".format(hash_map.size()))


print("one: {}".format(hash_map.get("one")))
print("neo: {}".format(hash_map.get("neo")))
print("three: {}".format(hash_map.get("three")))
print("size: {}".format(hash_map.size()))

hash_map                          # call to the helper function to see the hashmap