#!/usr/bin/python3
import os, getopt, time
from threading import Thread, Event
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
bodynum = 0

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
    text = re.sub('～','', text)
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
    if bodynum == '2':
        if len(kanji) > 0:
            body = "({}) {}, {} 【{}】, {}:".format(stridx, roma, kana, kanji, chinese)
        else:
            body = "({}) {}, {}, {}:".format(stridx, roma, kana, chinese)
    elif bodynum == '1':
        body = "{}, {}:".format(stridx, chinese)
    else:
        body = contents0.format(kana, tone, stridx, chinese ,roma, kanji, english)
    return (wordid, body, roma, kana, kanji)

def stopaudio(onmute):
    if onmute == True: return
    if mixer.music.get_busy():
        mixer.music.stop()

def playaudio(key, onmute):
    if onmute == True: return
    stopaudio(onmute)
    if os.path.isfile(key):
        audiofile = key
    else:
        audiofile = wordaudio.get(key, '')
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
    answer = [re.sub('\[|\]|~|～|\？|\?|\'|、|…','', word) for word in ret]
    
    playaudio(kana, mute)
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
            playaudio(kana, False)
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
            playaudio(kana, False)
            pass
        elif response in ['6', '６']:
            lookupdictionary(kana)
            input("-------please enter any key...")
            pass
        elif response in ['5', '５']:
            if len(kanji):
                print("{}【{}】".format(kana, kanji))
            else:
                print("{}".format(kana))
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
            # playaudio('right.mp3', False)
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


def waitkey(event):
    k = input("enter anykey for exit")
    event.set()
    
def showdata(data):
    if len(data) == 0: return
    inx = 0
    kanas = []
    for tup in data:
        inx += 1
        wordid, kana, kanji, roma, chinese, english, wordtype, tone, lesson, description, nlevel = tup
        kanas.append(kana)
        if len(kanji) > 0:
            print("{} {}: {} [{}]".format(inx, chinese, kana, kanji))
        else:
            print("{} {}: {}".format(inx, chinese, kana))

    if mute == True: return
    event = Event()
    t1 = Thread(target = waitkey, args = (event, ))
    t1.start()
    for kana in kanas:
        if event.isSet(): return
        playaudio(kana, mute)
        while mixer.music.get_busy():
            time.sleep(1)

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
    bodynum = 0
    randomword = False
    muteaudio = False
    lessonre = ''
    opts, args = getopt.getopt(argv,'-h-k:-v-r-m-b:-l:',['help', 'key=', 'version', 'random', 'mute', 'body=', 'lesson='])
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
        if opt in ("-b", "--body"):
            bodynum = arg
        if opt in ("-l", "--lesson"):
            lessonre = querys.getlessonre(arg)

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
        value =  querys.sqls[key].format(lessonre)
    elif key in lastfname:
        value = lastfname
    else:
        assert 0, 'No value found'

    logger.debug("value: {}".format(value))
    return (value, showing, randomword, muteaudio, bodynum)

if __name__ == '__main__':
    # init log
    logfile = sys.argv[0] + '.log'
    if os.path.exists(logfile):
        os.unlink(logfile)
    logging.basicConfig(filename = logfile, level = logging.DEBUG, format = '%(asctime)s - %(levelname)s - %(message)s')
    logger = logging

    # get data
    value, showing, randomword, mute, bodynum = getparam(sys.argv[1:])
    data = getdata(value)
    if len(data) == 0:
        print('-------no data, please check your sql')
        print("-------{}".format(value))
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
    
    stopaudio(mute)
    print('-------bye')
