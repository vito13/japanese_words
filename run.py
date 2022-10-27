#!/usr/bin/python3



import os
import re
import sys
import sqlite3
import random
import json
from enum import Enum, auto, unique

dbfile = 'jp.db'
wordtable = 'jpwords'

class WORDRESULTTYPE(Enum):
    CORRECT_NEXT = auto()    # 正确next
    GIVEUP_NEXT = auto()   # 放弃next
    GIVEUP_PREV = auto()   # 放弃prev
    UNKNOWN = auto()

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

def testone(tup, stridx):
    id, kana, kanji, roma, chinese, wordtype, lesson = tup

    newroma = roma
    newchn = re.sub(r'[），（ ]', ' ', chinese)
    newchn = "{} {}".format(newchn, stridx)
    msg = "{} {} {} {} {} {}    {} {}".format(contents0, kana, contents1, newchn, contents2, newroma, kanji, contents3)
    # print(msg)    
    clear = lambda: os.system('clear')
    clear()

    result = WORDRESULTTYPE.UNKNOWN
    while True:
        response = input(msg)
        if response == 'q':
            sys.exit()
        elif response == '1':
            result = WORDRESULTTYPE.GIVEUP_PREV
            break
        elif response == '`':
            result = WORDRESULTTYPE.GIVEUP_NEXT
            break
        elif response == newroma:
            result = WORDRESULTTYPE.CORRECT_NEXT
            break
        else:
            pass
            
    return result

def run(data):
    count = len(data)
    testindex = 0
    while testindex < count: 
        stridx = '-{}-{}-'.format(testindex + 1, count)
        ret = testone(data[testindex], stridx)
        if WORDRESULTTYPE.GIVEUP_NEXT == ret:
            testindex += 1
        elif WORDRESULTTYPE.CORRECT_NEXT == ret:
            testindex += 1
        elif WORDRESULTTYPE.GIVEUP_PREV == ret:
            testindex -= 1
        else:
            pass
        
        if testindex < 0:
            testindex = 0

def getwords(sql):
    # 连接数据库
    conn = sqlite3.connect(dbfile)
    # 创建游标
    cs = conn.cursor()
    # 查询数据
    cs.execute(sql)
    words = cs.fetchall()
    # 关闭 Cursor
    cs.close()
    # 关闭连接
    conn.close()
    return words

def getparam():
    with open('run.json', 'r',encoding='utf-8') as f:
        params = json.load(f)
        return (params['sql'])
    
if __name__ == '__main__':
    run(getwords(getparam()))