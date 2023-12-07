# Name:Troy Hoffman
# OSU Email: hoffmatr@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6
# Due Date: 12/7/2023
# Description:Python script implements a hash map with separate chaining for collision resolution, including methods for inserting, resizing, retrieving, checking existence, removing, and finding the mode
#and frequency of elements in a dynamic array

from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Insert a Key value pair into hashmap
        """
        # Check if the table needs to be resized
        if self.table_load() >= 1:
            self.resize_table(self._capacity * 2)

        hash_value = self._hash_function(key)
        module_value = self._capacity
        index_value = hash_value % module_value

        # Track the bucket value
        bucket = self._buckets[index_value]

        # Check if the key is already present
        node_value = self.contains_key(key)

        # if key is present, update the value
        if node_value is True:

            # Iterate through the hash map
            for index in range(self._capacity):
                current_bucket = self._buckets.get_at_index(index_value)

                # Iterate through the linked list and update the value
                for node in current_bucket:
                    if node.key == key:
                        node.value = value

        # If the key is not present, insert the key-value pair
        else:
            bucket.insert(key, value)
            self._size += 1


    def resize_table(self, new_capacity: int) -> None:
        """
        Resize the Hash map to the specified new capacity
        """
        # Check if the new capacity is less than 1
        if new_capacity < 1:
            return

        # Check if the new capacity is a prime number
        if self._is_prime(new_capacity) is False:
            new_capacity = self._next_prime(new_capacity)

        # Check if the new capacity is greater than the current capacity
        while (self._size/new_capacity) > 1:
            new_capacity = new_capacity * 2
            new_capacity = self._next_prime(new_capacity)

        # Reset the size
        self._size = 0

        # Create a new DynamicArray
        storage_da = DynamicArray()

        # Iterate through the new DynamicArray and append a LinkedList
        for index in range(new_capacity):
            storage_da.append(LinkedList())

        # Iterate through the old DynamicArray
        for bucket in range(self._capacity):
            # Remove the old bucket
            current_bucket = self._buckets.pop()

            # Iterate through the old bucket
            for node in current_bucket:
                key = node.key
                value = node.value

                # Find the new index of the bucket
                new_key = self._hash_function(key) % new_capacity
                bucket = storage_da[new_key]

                # Insert the key-value pair into the new bucket
                bucket.insert(key, value)
                self._size += 1

        # Update the capacity and buckets
        self._buckets = storage_da
        self._capacity = new_capacity

    def table_load(self) -> float:
        """
        Calculate and return the load factor of the hash map.
        """
        # Calculate the load factor
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Count and return the number of empty buckets in hash map
        """
        count = 0
        # Count the number of empty buckets
        for i in range(self._buckets.length()):
            current_bucket = self._buckets.get_at_index(i)
            if current_bucket.length() == 0:
                count += 1
        return count

    def get(self, key: str):
        """
        Retrieve the value associated with key or none
        """
        # Find the index of the bucket
        index = self._hash_function(key) % self._capacity
        bucket = self._buckets[index]

        # Check if the key exists in the bucket
        node = bucket.contains(key)

        # If the key exists, return the value
        if node:
            return node.value
        else:
            return None

    def contains_key(self, key: str) -> bool:
        """
        Check if the given key is present in the hash map
        """
        # Find the index of the bucket
        index = self._hash_function(key) % self._capacity
        bucket = self._buckets[index]

        # Check if the key exists in the bucket
        node = bucket.contains(key)

        # If the key exists, return True
        if node:
            return True
        else:
            return False

    def remove(self, key: str) -> None:
        """
        Remove the key-value pair associated with the given key from the hash map.
        """
        # Find the index of the bucket
        index = self._hash_function(key) % self._capacity
        bucket = self._buckets[index]

        # Remove the key-value pair from the bucket
        if bucket.remove(key):
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
         Return a dynamic array containing all key-value pairs in the hash map.
         """
        # Create a dynamic array
        da = DynamicArray()

        # Iterate through the hash map
        for i in range(self._buckets.length()):
            if self._buckets[i] is not None:
                for node in self._buckets[i]:
                    # Append the key-value pair to the dynamic array
                    da.append((node.key, node.value))

        return da

    def clear(self) -> None:
        """
        Remove all key-value pairs from the hash map
        """
        # Iterate through the hash map
        for i in range(self._buckets.length()):
            if self._buckets[i] is not None:
                for node in self._buckets[i]:
                    # Remove the key-value pair from the hash map
                    self.remove(node.key)


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
     Find the mode and frequency of elements in the given dynamic array
     """
    # Create a hash map
    hm = HashMap()

    # Iterate through the dynamic array
    for i in range(da.length()):
        # Add the key-value pair to the hash map
        hm.put(da[i], 0)

    # Iterate through the dynamic array
    for i in range(da.length()):
        # Update the value of the key-value pair
        hm.put(da[i], hm.get(da[i]) + 1)

    # Initialize the mode and frequency
    mode = DynamicArray()
    frequency = 0

    # Iterate through the hash map
    for i in range(hm._buckets.length()):
        if hm._buckets[i] is not None:
            for node in hm._buckets[i]:
                # Check if the frequency is greater than the current frequency
                if node.value > frequency:
                    # Update the mode and frequency
                    mode = DynamicArray()
                    mode.append(node.key)
                    frequency = node.value

                # Check if the frequency is equal to the current frequency
                elif node.value == frequency:
                    # Update the mode
                    mode.append(node.key)

    return mode, frequency


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
