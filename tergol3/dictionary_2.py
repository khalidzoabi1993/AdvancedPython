# Solution 1: Using the pop() method and loop
sample_dict = {"name": "Kelly", "age": 25, "salary": 8000, "city": "New york"}
# Keys to remove
keys = ["name", "salary"]

for k in keys:
    sample_dict.pop(k)
print(sample_dict)
################################################################################
# Solution 2: Dictionary Comprehension

sample_dict = {"name": "Kelly", "age": 25, "salary": 8000, "city": "New york"}
# Keys to remove
keys = ["name", "salary"]

sample_dict = {k: sample_dict[k] for k in sample_dict.keys() - keys}
print(sample_dict)
