import random
MISSING = [55, 92, 241, 395, 457, 458, 469, 519, 532, 603, 798, 936, 1098, 1266, 1311, 1325, 1399, 1481, 1483, 1556, 1733, 1765, 1785, 1970, 1982]
#foods_with_images.csv  old_data  programs  stores.csv  transactions.csv  users.csv
#list all purchase_id where food_id is not in food_type

food_types="foods_with_images.csv"
food_instances="transactions.csv"

food_ids={}
with open(food_types, "r") as f1:
        for line in f1:
            fields = line.split(",")
            food_id = fields[0]
            food_ids[food_id] = ""

with open(food_instances, "r") as f2:
        for line in f2:
            fields = line.split(",")
            food_id = fields[1]
            purchase_id = fields[0]
            if food_id not in food_ids:
                replacement = random.randint(1, 2593)
                while replacement in MISSING:
                    replacement = random.randint(1, 2593)
                print(purchase_id, "\tMISSING:", food_id, "\t\tREPLACEMENT: ", replacement)
