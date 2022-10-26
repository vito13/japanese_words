#!/usr/bin/python3



import os
import re
import sys
import sqlite3
import random


dbfile = 'jp.db'
wordtable = 'jpwords'
testcount = 3
c0 = "confuse0.txt"
c1 = "confuse1.txt"
c2 = "confuse2.txt"
c3 = "confuse3.txt"
contents0 = ""
contents1 = ""
contents2 = ""
contents3 = ""
with open(c0) as file_object:
    contents0 = file_object.read()
with open(c1) as file_object:
    contents1 = file_object.read()
with open(c2) as file_object:
    contents2 = file_object.read()
with open(c3) as file_object:
    contents3 = file_object.read()

def testone(tup):
    id, kana, kanji, roma, chinese, wordtype = tup
    
    while True:
        clear = lambda: os.system('clear')
        clear()
        newchn = re.sub(r'[），（ ]', ' ', chinese)
        msg = "{} {} {} {} {} {} {}".format(contents0, kana, contents1, newchn, contents2, roma, contents3)
        # print(msg)
       
        response = input(msg)
        if response == 'q':
            sys.exit()
        if response == '`':
            break
        if response == roma:
            break

def test(data, count):
    items = random.sample(data, count)
    for tup in items:
        testone(tup)

def getwords():
    # 连接数据库
    conn = sqlite3.connect(dbfile)
    # 创建游标
    cs = conn.cursor()
    # 查询数据
    cs.execute("SELECT * FROM {}".format(wordtable))

    words = cs.fetchall()
    # 关闭 Cursor
    cs.close()
    # 关闭连接
    conn.close()
    return words


if __name__ == '__main__':
    data = getwords()
    test(data, testcount)