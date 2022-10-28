#!/usr/bin/python3



import os, getopt
import re
import sys
import sqlite3
import random
import json
from enum import Enum, auto, unique
import logging
from hyperparameters import global_var

dbfile = global_var.get_value('dbfile')
wordtable = global_var.get_value('wordtable')
runlog = global_var.get_value('runlog')

class WORDRESULTTYPE(Enum):
    CORRECT_NEXT = auto()       # 正确next
    GIVEUP_NEXT = auto()        # 放弃next
    GIVEUP_PREV = auto()        # 放弃prev
    
    INCREASE_NEXT = auto()        # 加入后next
    DECREASE_NEXT = auto()        # 去除后next
    
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



def doincrease(wid):
    conn = sqlite3.connect(dbfile)
    cs = conn.cursor()
    sql = "update {} set increase = increase + 1 where id = \"{}\"".format(wordtable, wid)
    logging.debug(sql)
    cs.execute(sql)
    cs.close()
    conn.commit()
    conn.close()


def dodecrease(wid):
    conn = sqlite3.connect(dbfile)
    cs = conn.cursor()
    sql = "update {} set decrease = decrease + 1 where id = \"{}\" and decrease + 1 <= increase".format(wordtable, wid)
    logging.debug(sql)
    cs.execute(sql)
    cs.close()
    conn.commit()
    conn.close()

def dowrong(wid):
    conn = sqlite3.connect(dbfile)
    cs = conn.cursor()
    sql = "update {} set wrong = wrong + 1 where id = \"{}\"".format(wordtable, wid)
    logging.debug(sql)
    cs.execute(sql)
    cs.close()
    conn.commit()
    conn.close()
    
def docorrect(wid):
    conn = sqlite3.connect(dbfile)
    cs = conn.cursor()
    sql = "update {} set correct = correct + 1 where id = \"{}\"".format(wordtable, wid)
    logging.debug(sql)
    cs.execute(sql)
    cs.close()
    conn.commit()
    conn.close()

def testone(tup, stridx):
    wordid, kana, kanji, roma, chinese, wordtype, lesson, increase, decrease, correct, wrong = tup

    newroma = roma
    newchn = re.sub(r'[），（ ]', ' ', chinese)
    newchn = "{} {}".format(newchn, stridx)
    msg = "{} {} {} {} {} {}    {} {}".format(contents0, kana, contents1, newchn, contents2, newroma, kanji, contents3)
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
            docorrect(wordid)
            break
        elif response == '9':
            result = WORDRESULTTYPE.INCREASE_NEXT
            doincrease(wordid)
            break
        elif response == '0':
            result = WORDRESULTTYPE.DECREASE_NEXT
            dodecrease(wordid)
            break
        else:
            dowrong(wordid)
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
        elif WORDRESULTTYPE.INCREASE_NEXT == ret:
            testindex += 1
        elif WORDRESULTTYPE.DECREASE_NEXT == ret:
            testindex += 1
        else:
            pass
        
        if testindex < 0:
            testindex = 0

def show(data, key):
    for tup in data:
        wordid, kana, kanji, roma, chinese, wordtype, lesson, increase, decrease, correct, wrong = tup
        if 'correct' == key:
            print("{}\tL{} {}".format(correct, lesson, chinese))
        elif 'wrong' == key:
            print("{}\tL{} {}".format(wrong, lesson, chinese))
        else:
            pass
            
def getwords(sql):
    conn = sqlite3.connect(dbfile)
    cs = conn.cursor()
    cs.execute(sql)
    logging.debug(sql)
    words = cs.fetchall()
    for word in words:
        logging.debug(word)
    cs.close()
    conn.close()
    return words

def getparam(key):
    with open('run.json', 'r',encoding='utf-8') as f:
        params = json.load(f)
        sql = ''
        if key in params:
            sql = params[key]
        else:
            assert 0, 'Invalid parameter'
        
        return sql

def main(argv):
    sqlkey = ""
    try:
        opts, args = getopt.getopt(argv,"hw:",["sql="])
    except getopt.GetoptError:
        print ('run.py -w <sql>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('run.py -w <key>')
            sys.exit()
        elif opt in ("-w", "--key in run.json"):
            sqlkey = arg
    
    if not sqlkey:
        sqlkey = 'random'
    logging.debug(sqlkey)
    v = getparam(sqlkey)
    if v:
        date = getwords(v)
        vals = re.findall(r'show_(\w+)', sqlkey)
        if len(vals) == 1:
            show(date, vals[0])
        else:
            run(date)
    else:
        assert 0, 'Invalid parameter'


if __name__ == '__main__':
    if os.path.exists(runlog):
        os.unlink(runlog)
    logging.basicConfig(filename = runlog, level = logging.DEBUG, format = '%(asctime)s - %(levelname)s - %(message)s')
    main(sys.argv[1:])