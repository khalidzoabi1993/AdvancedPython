# Create a dictionary by extracting the keys from a given dictionary
# sampleDict = {"name": "Kelly", "age": 25, "salary": 8000, "city": "New york"}
# Keys to extract
# keys = ["name", "salary"]

# Solution 1
sampleDict = {"name": "Kelly", "age": 25, "salary": 8000, "city": "New york"}

keys = ["name", "salary"]

newDict = {k: sampleDict[k] for k in keys}
print(newDict)
###############################################################################
# Solution 2: Using the update() method and loop

# new dict
res = dict()

for k in keys:
    # add current key with its va;ue from sampleDict
    res.update({k: sampleDict[k]})
print(res)
###############################################################################
