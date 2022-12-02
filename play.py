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
from jamdict import Jamdict
import pickle
from datetime import timedelta, datetime
import querys
from pygame import mixer
from wordaudio import wordaudio

dbfile = global_var.get_value('dbfile')
wordtable = global_var.get_value('wordtable')
stats = global_var.get_value('stats')
logger = None
jam = Jamdict()
lastfname = 'last.bin'
mixer.init()
mute = False

class WORDRESULTTYPE(Enum):
    CORRECT_NEXT = auto()       # 正确next
    GIVEUP_NEXT = auto()        # 放弃next
    GIVEUP_PREV = auto()        # 放弃prev
    
    INCREASE_NEXT = auto()        # 加入后next
    DECREASE_NEXT = auto()        # 去除后next
    
    UNKNOWN = auto()


contents0 = ""
with open("confuse.txt", encoding = 'utf-8') as file_object:
    contents0 = file_object.read()

def lookupdictionary(text):
    # print("-------look up: ", text)
    result = jam.lookup(text)
    for entry in result.entries:
        print(entry)

def updatelasttime(kana):
    return "update {} set lasttime = {} where kana = \"{}\"".format(stats, datetime.today().timestamp(), kana)

def executesql(sqls):
    conn = sqlite3.connect(dbfile)
    cs = conn.cursor()
    for sql in sqls:
        logger.debug(sql)
        cs.execute(sql)
    cs.close()
    conn.commit()
    conn.close()
    
def buildbody(tup, stridx):
    wordid, kana, kanji, roma, chinese, english, wordtype, tone, lesson, description, nlevel = tup
    body = contents0.format(kana, tone, stridx, chinese ,roma, kanji, english)
    body = "({}) {}, {} [{}] {} :".format(stridx, roma, kana, kanji, chinese)
    # body = "{}, {} :".format(stridx, chinese)
    return (wordid, body, roma, kana, kanji)

def stopaudio():
    if mute == True: return
    if mixer.music.get_busy():
        mixer.music.stop()

def playaudio(kana):
    if mute == True: return
    stopaudio()
    audiofile = wordaudio.get(kana, '')
    if len(audiofile):
        mixer.music.load(audiofile)
        mixer.music.play()

def testone(tup, stridx, wrongwords):
    # clear = lambda: os.system('clear')
    # clear()
    result = WORDRESULTTYPE.UNKNOWN
    wordid, body, *ret = buildbody(tup, stridx)
    kana = ret[1]
    kanji = ret[2]
    wronged = False
    
    # 确保stats内有词
    executesql([
        "insert into {}(kana) select '{}' where not exists(select * from {} where kana='{}')".format(stats, kana, stats, kana)
        ])

    # 答案里会自动去掉"[]~'"的检测
    answer = [re.sub('\[|\]|~|～|\'|、|…','', word) for word in ret]
    
    playaudio(kana)
    while True:
        response = input(body)
        if response == '':
            continue
        if response in ['q', 'Q', 'ｑ', 'ℚ']:
            sys.exit()
        elif response in ['1', '１']:
            result = WORDRESULTTYPE.GIVEUP_PREV
            break
        elif response in ['`', '‘']:
            result = WORDRESULTTYPE.GIVEUP_NEXT
            break
        elif response in answer:
            result = WORDRESULTTYPE.CORRECT_NEXT
            executesql([
                "update {} set correct = correct + 1 where kana = \"{}\"".format(stats, kana),
                updatelasttime(kana)
                ])
            break
        elif response in ['9', '９']:
            result = WORDRESULTTYPE.INCREASE_NEXT
            executesql([
                "update {} set increase = increase + 1 where kana = \"{}\"".format(stats, kana),
                updatelasttime(kana)
                ])
            break
        elif response in ['0', '０']:
            result = WORDRESULTTYPE.DECREASE_NEXT
            executesql(["update {} set decrease = decrease + 1 where kana = \"{}\" and decrease + 1 <= increase".format(stats, kana)])
            break
        elif response in ['4', '４']:
            playaudio(kana)
            pass
        elif response in ['6', '６']:
            lookupdictionary(kana)
            input("-------please enter any key...")
            pass
        elif response in ['5', '５']:
            print("kana:{}".format(kana))
            if len(kanji):
                print("kanji:{}".format(kanji))
            input("-------please try again...")
            pass
        else:
            executesql([
                "update {} set wrong = wrong + 1 where kana = \"{}\"".format(stats, kana),
                updatelasttime(kana)
                ])
            wronged = True
            pass
    
    if wronged == True:
        wrongwords.append(tup)
    return result

def run(data):
    count = len(data)
    testindex = 0
    wrongwords = []
    while testindex < count: 
        stridx = '{}，{}'.format(testindex + 1, count)
        ret = testone(data[testindex], stridx, wrongwords)
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
    
    return wrongwords

def showdata(data):
    for tup in data:
        wordid, kana, kanji, roma, chinese, english, wordtype, tone, lesson, description, nlevel = tup
        print("{}:\t{} [{}]".format(chinese, kana, kanji))
    print(len(data))

def getdata(value):
    data = []
    if os.path.isfile(value):
        with open(value, 'rb') as f:
            data = pickle.load(f)
            logger.debug("load data from: {}".format(value))
            # Refresh data
            
    else:
        conn = sqlite3.connect(dbfile)
        cs = conn.cursor()
        cs.execute(value)
        if re.match(r'select', value, re.I) != None:
            data = cs.fetchall()
        else:
            conn.commit()
        cs.close()
        conn.close()
        logger.debug("total: {}".format(len(data)))
    return data

def getparam(argv):
    key = ""
    randomword = False
    muteaudio = False
    opts, args = getopt.getopt(argv,'-h-k:-v-r-m',['help', 'key=', 'version', 'random', 'mute'])
    for opt, arg in opts:
        if opt in ('-h','--help'):
            print("[*] Help info")
            sys.exit()
        if opt in ('-v','--version'):
            print("[*] Version is 0.01 ")
            sys.exit()
        if opt in ('-m', '--mute'):
            muteaudio = True
        if opt in ('-r', '--random'):
            randomword = True
        if opt in ("-k", "--key"):
            key = arg

    assert key != '', 'Invalid key'
    logger.debug("key: {}, random: {}".format(key, randomword))
    showing = False
    vals = re.findall(r'(.*?)show$', key)
    if len(vals) == 1:
        key = vals[0]
        showing = True

    logger.debug("showing: {}".format(showing))
    value = ''
    if key in querys.sqls.keys():
        value =  querys.sqls[key]
    elif key in lastfname:
        value = lastfname
    else:
        assert 0, 'No value found'

    logger.debug("value: {}".format(value))
    return (value, showing, randomword, muteaudio)

if __name__ == '__main__':
    # init log
    logfile = sys.argv[0] + '.log'
    if os.path.exists(logfile):
        os.unlink(logfile)
    logging.basicConfig(filename = logfile, level = logging.DEBUG, format = '%(asctime)s - %(levelname)s - %(message)s')
    logger = logging

    # get data
    value, showing, randomword, mute = getparam(sys.argv[1:])
    data = getdata(value)
    if randomword:
        random.shuffle(data)

    # run
    if showing:
        showdata(data)
    else:
        while(len(data)):
            data = run(data)
            datasize = len(data)
            if (datasize > 0):
                response = input("-------training again {} wrong words?(yes/no)".format(datasize))
                if 'y' in response or 'ｙ' in response:
                    with open(lastfname, 'wb') as f:
                        pickle.dump(data, f)
                    random.shuffle(data)
                    continue
            break
    
    stopaudio()
    print('-------bye')
