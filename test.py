from jamdict import Jamdict
jam = Jamdict()

# use wildcard matching to find anything starts with 食べ and ends with る
result = jam.lookup('だいがく')

# print all word entries
for entry in result.entries:
    print(entry)
    print("---")