import pprint
import pickle
lastfname = 'last.bin'
with open(lastfname, 'rb') as f:
    data = pickle.load(f)
    print(data)