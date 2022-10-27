#!/usr/bin/python3



import os
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
newwordtable = global_var.get_value('newwordtable')
runlog = global_var.get_value('runlog')


class RUNMODETYPE(Enum):
    RMT_JP = auto()
    RMT_NEW = auto()
    UNKNOWN = auto()
    
runmode = RUNMODETYPE.RMT_JP

class WORDRESULTTYPE(Enum):
    CORRECT_NEXT = auto()       # 正确next
    GIVEUP_NEXT = auto()        # 放弃next
    GIVEUP_PREV = auto()        # 放弃prev
    
    ADDNEW_NEXT = auto()        # 加入后next
    REMOVE_NEXT = auto()        # 去除后next
    
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



def addnewwords(idarr):
    conn = sqlite3.connect(dbfile)
    cs = conn.cursor()
    for wordid in idarr:
        val = "{}, \"{}\"".format(wordid, 'test')
        sql = "INSERT INTO {} (wordid, wordgroup) VALUES ({})".format(newwordtable, val)
        logging.debug(sql)
        cs.execute(sql)
    cs.close()
    conn.commit()
    conn.close()


def removenewwords(idarr):
    conn = sqlite3.connect(dbfile)
    cs = conn.cursor()
    for wordid in idarr:
        val = wordid
        sql = "DELETE FROM {} WHERE wordid = \"{}\"".format(newwordtable, val)
        logging.debug(sql)
        cs.execute(sql)
    cs.close()
    conn.commit()
    conn.close()


def testone(tup, stridx):
    wordid, kana, kanji, roma, chinese, wordtype, lesson = tup

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
            break
        elif response == '9':
            if runmode == RUNMODETYPE.RMT_JP:
                result = WORDRESULTTYPE.ADDNEW_NEXT
                addnewwords([wordid])
            elif runmode == RUNMODETYPE.RMT_NEW:
                result = WORDRESULTTYPE.REMOVE_NEXT
                removenewwords([wordid])
            else:
                assert 0, 'error mode'
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
        elif WORDRESULTTYPE.ADDNEW_NEXT == ret:
            testindex += 1
        elif WORDRESULTTYPE.REMOVE_NEXT == ret:
            testindex += 1
        else:
            pass
        
        if testindex < 0:
            testindex = 0

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

def getparam():
    global runmode
    with open('run.json', 'r',encoding='utf-8') as f:
        params = json.load(f)
        sql = params['sql']
        r1 = re.findall(r"newwords\.wordid\s*=\s*jpwords\.id", sql)     
        if r1:
            runmode = RUNMODETYPE.RMT_NEW
        logging.debug(runmode)
        return (sql)
    
if __name__ == '__main__':
    if os.path.exists(runlog):
        os.unlink(runlog)
    logging.basicConfig(filename = runlog, level = logging.DEBUG, format = '%(asctime)s - %(levelname)s - %(message)s')   
    run(getwords(getparam()))