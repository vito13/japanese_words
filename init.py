#!/usr/bin/python3



import os
import re
import sys
import sqlite3
import romkan
import logging
import json

dbfile = 'jp.db'
wordtable = 'jpwords'
logfname = 'myProgramLog.txt'

def createdb():
    # 连接数据库
    conn = sqlite3.connect(dbfile)
    # 创建游标
    cs = conn.cursor()
    # 创建表
    sql = '''
    CREATE TABLE if not exists {0} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        kana TEXT NOT NULL,
        kanji TEXT,
        roma TEXT NOT NULL,
        chinese TEXT NOT NULL,
        wordtype TEXT,
        lesson INTEGER
        );
    '''.format(wordtable)
    logging.debug(sql)
    cs.execute(sql)
    # 关闭 Cursor
    cs.close()
    # 提交当前事务
    conn.commit()
    # 关闭连接
    conn.close()

def addword(lesson, tup):
    roma = romkan.to_roma(tup[0])
    
    # 连接数据库
    conn = sqlite3.connect(dbfile)
    # 创建游标
    cs = conn.cursor()  
    val = "'{}', '{}', '{}', '{}', '{}', {}".format(tup[0], tup[2], roma, tup[4], tup[3], int(lesson))
    sql = "INSERT INTO {} (kana, kanji, roma, chinese, wordtype, lesson) VALUES ({})".format(wordtable, val)
    logging.debug(sql)
    cs.execute(sql)
    # 关闭 Cursor
    cs.close()
    # 提交当前事务
    conn.commit()
    # 关闭连接
    conn.close()
    


def processline(lesson, line):
    ret = re.findall(r'(.*?)(（(.*?)）)*?\s〔(.*?)〕\s(.*)', line)
    
    if len(ret):
        assert 5 == len(ret[0])
        addword(lesson, ret[0])
        pass
    else:
        print(line)

def processfile(lesson, src):
    with open(src) as file_object:
        contents = file_object.read()
    for line in contents.splitlines():
        processline(lesson, line)

if __name__ == '__main__':
    os.unlink(logfname)
    logging.basicConfig(filename = logfname, level = logging.DEBUG, format = '%(asctime)s - %(levelname)s - %(message)s')
    os.unlink(dbfile)
    createdb()

    with open('book.json', 'r',encoding='utf-8') as f:
        books = json.load(f)
        for key, value in books.items(): 
            processfile(value['lesson'], value['file'])
            
