#!/usr/bin/python3
import os
import re
import sys
import sqlite3
import romkan
import logging
import json
from collections import namedtuple
from enum import Enum, auto, unique
import queue
from hyperparameters import global_var

class LINETYPE(Enum):
    WORD = auto()       # 词
    SENTENCE = auto()   # 句
    LESSON = auto()     # 第x课
    WORDS = auto()      # 连续n个kana
    USELESS = auto()    # 横线
    UNKNOWN = auto()

dbfile = global_var.get_value('dbfile')
wordtable = global_var.get_value('wordtable')
log = sys.argv[0] + '.log'
dbinfo = global_var.get_value('dbinfo')

def batchinserts(sqls):
    conn = sqlite3.connect(dbfile)
    cs = conn.cursor()  

    for sql in sqls:
        logging.debug(sql)
        cs.execute(sql)

    cs.close()
    conn.commit()
    conn.close()


# 处理一行返回tuple
# kana, kanji, roma, chinese, wordtype, lesson
def processline(line):
    vals = re.findall(r'(.*?)(（(.*?)）)*?\s〔(.*?)〕\s(.*)', line)
    if len(vals) == 1 and len(vals[0]) == 5:
        tup = vals[0]
        roma = romkan.to_roma(tup[0])
        return (LINETYPE.WORD, tup[0], tup[2], roma, tup[4], tup[3], -1)

    vals = re.findall(r'(.*?)（(.*?)）\s(.*)', line)
    if len(vals) == 1 and len(vals[0]) == 3:
        tup = vals[0]
        roma = romkan.to_roma(tup[0])
        return (LINETYPE.SENTENCE, tup[0], tup[1], roma, tup[2], '', -1)

    vals = re.findall(r'第(\d+)课', line)
    if len(vals) == 1:
        return (LINETYPE.LESSON, '', '', '', '', '', vals[0])
    
    vals = re.findall(r'…+', line)
    if len(vals) == 1:
        return (LINETYPE.USELESS, '', '', '', '', '', -1)

    vals = line.split(' ')
    if len(vals) == 2:
        roma = romkan.to_roma(vals[0])
        return (LINETYPE.SENTENCE, vals[0], '', roma, vals[1], '', -1)
    
    vals = line.split('∕')
    kanas = []
    romas = []
    for v in vals:
        roma = romkan.to_roma(v)
        kanas.append(v)
        romas.append(roma)
    return (LINETYPE.WORDS, kanas, '', romas, '', '', -1)
            

def processfile(src, bookid):
    with open(src, encoding = 'utf-8') as file_object:
        contents = file_object.read()
    quote = ""
    sqls = []
    sqltemplate = "INSERT INTO {} (kana, kanji, roma, chinese, wordtype, quote) VALUES ({})"
    for line in contents.splitlines():
        linetype, kana, kanji, roma, chinese, wordtype, lesson = processline(line)
        if linetype == LINETYPE.LESSON:
            quote = "{}_{}".format(bookid, lesson)
            pass
        elif linetype == LINETYPE.WORD:
            val = "\"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\"".format(kana, kanji, roma, chinese, wordtype, quote)
            sql = sqltemplate.format(wordtable, val)
            sqls.append(sql)
            pass
        elif linetype == LINETYPE.SENTENCE:
            val = "\"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\"".format(kana, kanji, roma, chinese, LINETYPE.SENTENCE, quote)
            sql = sqltemplate.format(wordtable, val)
            sqls.append(sql)
            pass
        elif linetype == LINETYPE.WORDS:
            for k, r in zip(kana, roma):
                val = "\"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\"".format(k, '', r, '', LINETYPE.WORDS, quote)
                sql = sqltemplate.format(wordtable, val)
                sqls.append(sql)
            pass
        elif linetype == LINETYPE.USELESS:
            pass
        else:
            print(line)
            pass
    batchinserts(sqls)

if __name__ == '__main__':
    if os.path.exists(log):
        os.unlink(log)
    logging.basicConfig(filename = log, level = logging.DEBUG, format = '%(asctime)s - %(levelname)s - %(message)s')
    
    with open(dbinfo, 'r',encoding='utf-8') as f:
        info = json.load(f)
        value = info[sys.argv[0]]
        processfile(value['dict'], value['bookid'])
    
