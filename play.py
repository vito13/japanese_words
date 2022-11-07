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
logger = None


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

with open(c0, encoding = 'utf-8') as file_object:
    contents0 = file_object.read()
with open(c1, encoding = 'utf-8') as file_object:
    contents1 = file_object.read()
with open(c2, encoding = 'utf-8') as file_object:
    contents2 = file_object.read()
with open(c3, encoding = 'utf-8') as file_object:
    contents3 = file_object.read()

def executesql(sql):
    conn = sqlite3.connect(dbfile)
    cs = conn.cursor()
    logger.debug(sql)
    cs.execute(sql)
    cs.close()
    conn.commit()
    conn.close()
    
def buildbody(tup, stridx):
    wordid, kana, kanji, roma, chinese, english, wordtype, tone, lesson, description, nlevel, increase, decrease, correct, wrong = tup
    body = "{} {} {} {} {} {} {},   {},   {} {}".format(contents0,kana,contents1,chinese,stridx,contents2,roma,kanji,english,contents3)
    return (wordid, body, roma, kana, kanji)

def testone(tup, stridx):
    clear = lambda: os.system('clear')
    clear()
    result = WORDRESULTTYPE.UNKNOWN
    wordid, body, *ret = buildbody(tup, stridx)
    
    while True:
        response = input(body)
        if response in ['q', 'Q', 'ｑ', 'ℚ']:
            sys.exit()
        elif response in ['1', '１']:
            result = WORDRESULTTYPE.GIVEUP_PREV
            break
        elif response in ['`', '‘']:
            result = WORDRESULTTYPE.GIVEUP_NEXT
            break
        elif response in [*ret]:
            result = WORDRESULTTYPE.CORRECT_NEXT
            executesql("update {} set correct = correct + 1 where id = \"{}\"".format(wordtable, wordid))
            break
        elif response in ['9', '９']:
            result = WORDRESULTTYPE.INCREASE_NEXT
            executesql("update {} set increase = increase + 1 where id = \"{}\"".format(wordtable, wordid))
            break
        elif response in ['0', '０']:
            result = WORDRESULTTYPE.DECREASE_NEXT
            executesql("update {} set decrease = decrease + 1 where id = \"{}\" and decrease + 1 <= increase".format(wordtable, wordid))
            break
        else:
            executesql("update {} set wrong = wrong + 1 where id = \"{}\"".format(wordtable, wordid))
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

def showdata(data):
    for tup in data:
        print(tup)

def getdata(sql):
    conn = sqlite3.connect(dbfile)
    cs = conn.cursor()
    cs.execute(sql)
    data = cs.fetchall()
    logger.debug("total: {}".format(len(data)))
    cs.close()
    conn.close()
    return data

def getparam(argv):
    key = ""
    try:
        opts, args = getopt.getopt(argv,'-h-k:-v',['help', 'key=', 'version'])
    except getopt.GetoptError:
        print('python3 {}'.format(sys.argv[0]))
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h','--help'):
            print("[*] Help info")
            sys.exit()
        elif opt in ('-v','--version'):
            print("[*] Version is 0.01 ")
            sys.exit()
        elif opt in ("-k", "--key"):
            key = arg
        else:
            assert 0, 'Invalid arg'

    assert key != '', 'Invalid key'
    logger.debug("key: {}".format(key))
    showing = False
    vals = re.findall(r'show(\w+)', key)
    if len(vals) == 1:
        key = vals[0]
        showing = True

    logger.debug("showing: {}".format(showing))
    sql = ''
    with open('run.json', 'r',encoding='utf-8') as f:
        params = json.load(f)
        if key in params:
            sql = params[key]
        else:
            assert 0, 'No sql found'

    logger.debug("sql: {}".format(sql))
    return (sql, showing)

if __name__ == '__main__':
    # init log
    logfile = sys.argv[0] + '.log'
    if os.path.exists(logfile):
        os.unlink(logfile)
    logging.basicConfig(filename = logfile, level = logging.DEBUG, format = '%(asctime)s - %(levelname)s - %(message)s')
    logger = logging

    # get data
    sql, showing = getparam(sys.argv[1:])
    data = getdata(sql)
    
    # run
    if showing:
        showdata(data)
    else:
        run(data)
