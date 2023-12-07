HashMap Implementation in Python
This project implements a hash map in Python, utilizing quadratic probing for collision resolution. The hash map provides dynamic resizing, key-value pair insertion, retrieval, removal, and iteration functionality.


The hash map is implemented in the HashMap class, which supports the following operations:

Insertion of key-value pairs
Retrieval of values using keys
Removal of key-value pairs
Dynamic resizing for efficient memory management
Iteration over non-empty and non-tombstone entries
Features
Quadratic Probing: The hash map uses quadratic probing to resolve collisions.
Dynamic Resizing: The hash map automatically resizes when the load factor exceeds a certain threshold.
Hash Functions: The implementation supports custom hash functions.
Efficient Iteration: The __iter__() and __next__() methods allow for efficient iteration over non-empty and non-tombstone entries.
Getting Started
Prerequisites
Python 3.x


Installation
Clone the repository to your local machine:

bash
Copy code
git clone https://github.com/your-username/hashmap-python.git
Usage
python
Copy code
from hashmap import HashMap, hash_function_1, hash_function_2

# Create a hash map with a specified capacity and hash function
my_map = HashMap(50, hash_function_1)

# Insert key-value pairs
my_map.put('key1', 'value1')
my_map.put('key2', 'value2')

# Retrieve values
value = my_map.get('key1')

# Remove a key-value pair
my_map.remove('key2')

# Iterate over non-empty and non-tombstone entries
for item in my_map:
    print('Key:', item.key, 'Value:', item.value)
Examples
Example 1: Insertion and Retrieval
python
Copy code
from hashmap import HashMap, hash_function_1

# Create a hash map
my_map = HashMap(50, hash_function_1)

# Insert key-value pairs
my_map.put('key1', 'value1')
my_map.put('key2', 'value2')

# Retrieve values
value1 = my_map.get('key1')
value2 = my_map.get('key2')

print('Value for key1:', value1)
print('Value for key2:', value2)
Example 2: Dynamic Resizing
python
Copy code
from hashmap import HashMap, hash_function_2

# Create a hash map
my_map = HashMap(50, hash_function_2)

# Insert key-value pairs until resizing occurs
for i in range(100):
    my_map.put(f'key{i}', f'value{i}')

print('Current capacity:', my_map.get_capacity())
