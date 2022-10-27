import re
str_content = "SELECT wordid, kana, kanji, roma, chinese, wordtype, lesson FROM jpwords, newwords where newwords.wordid =jpwords.id"





r1 = re.findall(r"newwords\.wordid\s*=\s*jpwords\.id", str_content)
print(r1)