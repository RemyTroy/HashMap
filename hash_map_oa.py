# Name:Troy Hoffman
# OSU Email: hoffmatr@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6
# Due Date: 12/7/2023
# Description:Python implementation of a hash map, utilizing quadratic probing for collision resolution, provides dynamic resizing, key-value pair insertion, retrieval, removal, and iteration functionality.

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

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
        Increment from given number to find the closest prime number
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
        Insert a key-value pair into the hash map, updating the value if the key is already present
        """
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)

        hash_value = self._hash_function(key)
        module_value = self._capacity
        index = hash_value % module_value

        # Get the value at bucket
        bucket = self._buckets[index]

        # Check if the index already has a value, if not, add the value
        if bucket is None:
            self._buckets[index] = HashEntry(key, value)
            self._size += 1

        # Check if the index has the same key, if so, replace the value
        elif self._buckets[index].key == key and self._buckets[index].is_tombstone is False:
            self._buckets[index].value = value

        # Check if the index has the same key but is a tombstone, if so, replace the value and change the tombstone to False
        elif self._buckets[index].key == key and self._buckets[index].is_tombstone is True:
            self._buckets[index].value = value
            self._buckets[index].is_tombstone = False
            self._size += 1

        else:
            # Quadratic probing
            quadratic = 1
            while bucket is not None:
                index = (hash_value + (quadratic ** 2)) % module_value
                bucket = self._buckets[index]
                quadratic += 1
                # Check if the index already has a value, if not, add the value
                if self._buckets[index] is not None and self._buckets[index].key == key:
                    # Check if the index has the same key, if so, replace the value
                    if self._buckets[index].is_tombstone is False:
                        self._buckets[index].value = value
                        return
                    # Check if the index has the same key but is a tombstone, if so, replace the value and change the tombstone to False
                    if self._buckets[index].is_tombstone is True:
                        self._buckets[index].value = value
                        self._buckets[index].is_tombstone = False
                        self._size += 1
                        return

            # Add the value to the index
            self._buckets[index] = HashEntry(key, value)
            self._size += 1


    def resize_table(self, new_capacity: int) -> None:
        """
         Resize the hash map to the specified new capacity
         """
        if new_capacity < self._size or new_capacity < 1:
            return

        # Check if the new capacity is a prime number, if not, change it to the next highest prime number
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # Create a new hash map with the new capacity
        new_hash_map = HashMap(new_capacity, self._hash_function)

        # Iterate through the current hash map and add the values to the new hash map
        for index in range(self._capacity):
            if self._buckets[index] is not None and self._buckets[index].is_tombstone is False:
                new_hash_map.put(self._buckets[index].key, self._buckets[index].value)

        # Change the current hash map to the new hash map
        self._buckets = new_hash_map._buckets
        self._capacity = new_hash_map._capacity



    def table_load(self) -> float:
        """
         Calculate and return the load factor of the hash map
         """
        # Return the load factor
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Count and return the number of empty buckets in the hash map
        """
        count = 0
        # Count empty buckets
        for index in range(self._buckets.length()):
            current_entry = self._buckets.get_at_index(index)
            if current_entry is None:
                count += 1

        return count

    def get(self, key: str) -> object:
        """
        Retrieve the value associated with the given key, or None if the key is not present
        """
        hash_value = self._hash_function(key)
        module_value = self._capacity

        # Find the index
        index = hash_value % module_value
        start_index = index
        index_value = self._buckets.get_at_index(index)

        if self._buckets[index] is not None and self._buckets[index].is_tombstone is False:
            if self._buckets[index].key == key:
                return self._buckets[index].value

            else:
                # Quadratic probing
                quadratic = 1
                while index_value is not None:
                    index = (start_index + (quadratic ** 2)) % module_value

                    # If the index has the same key and is not a tombstone, return the value
                    if index_value.key == key and index_value.is_tombstone is False:
                        return index_value.value

                    # Find the next index
                    index_value = self._buckets.get_at_index(index)
                    quadratic += 1

        else:
            return None

    def contains_key(self, key: str) -> bool:
        """
        Check if the given key is present in the hash map and return a boolean
        """
        # Check if the given key is in the hash map, otherwise it returns False.
        if self._size == 0:
            return False

        hash_value = self._hash_function(key)
        module_value = self._capacity

        index = hash_value % module_value # Get the index of the key
        start_index = index
        index_value = self._buckets.get_at_index(index) # Get the value at the index

        if self._buckets[index] is not None and self._buckets[index].is_tombstone is False:
            if self._buckets[index].key == key:
                return True

            else:
                # Quadratic probing
                quadratic = 1
                while index_value is not None:
                    index = (start_index + (quadratic ** 2)) % module_value

                    # If the index has the same key and is not a tombstone, return True
                    if index_value.key == key and index_value.is_tombstone is False:
                        return True

                    # Find the next index
                    index_value = self._buckets.get_at_index(index)
                    quadratic += 1

        return False


    def remove(self, key: str) -> None:
        """
        Remove the key-value pair associated with the given key from the hash map
        """
        if self._size == 0:
            return

        # Remove the given key and its associated value from the hash map.
        hash_value = self._hash_function(key)
        module_value = self._capacity

        index = hash_value % module_value # Get the index of the key
        quadratic = 1

        # Find the key
        while self._buckets[index] is not None:
            if self._buckets[index].key == key and self._buckets[index].is_tombstone is False:
                self._buckets[index].is_tombstone = True
                self._size -= 1
                return


            # Quadratic probing
            index = (hash_value + (quadratic ** 2)) % module_value

            quadratic += 1


    def get_keys_and_values(self) -> DynamicArray:
        """
         Return a dynamic array containing all key-value pairs in the hash map
         """
        # Return a dynamic array where each index contains a tuple of a key/value pair stored in the hash map.
        result = DynamicArray()
        for index in range(self._capacity):
            current_entry = self._buckets[index]
            # Skip empty slots
            if current_entry is not None and current_entry.is_tombstone is False:
                result.append((current_entry.key, current_entry.value))

        return result


    def clear(self) -> None:
        """
        Remove all key-value pairs from the hash map
        """
        # Create a new Dynamic Array
        self._buckets = DynamicArray()

        # Fill the Dynamic Array with None
        for index in range(self._capacity):
            self._buckets.append(None)

        # Reset the size
        self._size = 0


    def __iter__(self):
        """
        Initialize the iterator for the hash map and return itself
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Return the next non-empty and non-tombstone HashEntry in the hash map
        """
        while self._index < self._capacity:
            current_entry = self._buckets[self._index]
            # Skip empty slots
            if current_entry is not None and not current_entry.is_tombstone:
                self._index += 1
                return current_entry
            else:
                self._index += 1

        raise StopIteration

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
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

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
    m = HashMap(11, hash_function_1)
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

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
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

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
