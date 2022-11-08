import csv
import re
import os
from Jpword import Jpword

def load(jpdict, logger):
    filepath = os.path.abspath("custom")
    file = os.listdir(filepath)
    for f in file:
        real_url = os.path.join(filepath , f)
        h = re.compile(r"(.*)\.csv")
        m = h.match(f)
        wordtype = m.group(1)
        
        with open(real_url, newline='', encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                w = Jpword(row[0])
                w.chinese = row[1]
                w.wordtype = wordtype
                jpdict.merge(w)