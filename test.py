import re
s = '他她、那个人(「あのかた」是「あのひと」的礼貌说法),他、她、那个人,你、 您a '
seta = set(re.split(r'[、;，,]', s))
s2 = '他她、那个人(「あのかた」是「あのひと」的礼貌说法),他、她、那个人,你、 您b '
setb = set(re.split(r'[、;，,]', s2))
setall = seta.union(setb)
print(setall)