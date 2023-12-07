# HashMap Implementation in Python

This project implements a hash map in Python, utilizing quadratic probing for collision resolution. The hash map provides dynamic resizing, key-value pair insertion, retrieval, removal, and iteration functionality.

## Table of Contents

- [Description](#description)
- [Features](#features)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## Description

The hash map is implemented in the `HashMap` class, which supports the following operations:

- Insertion of key-value pairs
- Retrieval of values using keys
- Removal of key-value pairs
- Dynamic resizing for efficient memory management
- Iteration over non-empty and non-tombstone entries

## Features

- **Quadratic Probing:** The hash map uses quadratic probing to resolve collisions.
- **Dynamic Resizing:** The hash map automatically resizes when the load factor exceeds a certain threshold.
- **Hash Functions:** The implementation supports custom hash functions.
- **Efficient Iteration:** The `__iter__()` and `__next__()` methods allow for efficient iteration over non-empty and non-tombstone entries.

## Getting Started

### Prerequisites

- Python 3.x

### Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/your-username/hashmap-python.git

https://remytroy.github.io/HashMap/
