#sorts a 2 level dictionary by key of both levels

import json

# Read the input file
with open("unsorted_dict.txt", "r") as f:
    my_dict = json.load(f)

# Sort both levels of the dictionary by keys
sorted_dict = {}
for outer_key in sorted(my_dict.keys()):
    outer_dict = my_dict[outer_key]
    sorted_inner_dict = {}
    for inner_key in sorted(outer_dict.keys()):
        sorted_inner_dict[inner_key] = outer_dict[inner_key]
    sorted_dict[outer_key] = sorted_inner_dict

# Write the sorted dictionary to a JSON file
with open("sorted_dict.json", "w") as f:
    json.dump(sorted_dict, f, indent=4)
