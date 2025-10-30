"""
operations on lists:
    - creating a list
    - finding the length of a list
    - sorting a list
    - removing elements from a list
    - checking if a specific item exists in a list
    - creating a new list by slicing elements 
"""

# create a simple list
simple_list = [1, 2, 3, 4, 5]
print(f"simple_list: {simple_list}")

# Finding the length of a list
print(f"len(simple_list): {len(simple_list)}")

# Sorting a list in ascending order (in-place)
simple_list.sort()
print(f"simple_list.sort(): {simple_list}")

# Sorting a list in descending order (in-place)
simple_list.sort(reverse=True)
print(f"simple_list.sort(reverse=True): {simple_list}")

# Removing elements from a list
simple_list.remove(3)
print(f"simple_list.remove(3): {simple_list}")

# Checking if a specific item exists in a list
print(f"4 in simple_list: {4 in simple_list}")
print(f"3 in simple_list: {3 in simple_list}")

# Creating a new list by slicing elements
new_list = simple_list[1:3]
print(f"new_list = simple_list[1:3]: {new_list}")
