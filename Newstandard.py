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
   

  
   
    
   
  
    vals = line.split('∕')
    kanas = []
    romas = []
    for v in vals:
        roma = romkan.to_roma(v)
        kanas.append(v)
        romas.append(roma)
    return (LINETYPE.WORDS, kanas, '', romas, '', '', -1)
            

def processfile(words, src):
    with open(src, encoding = 'utf-8') as file_object:
        contents = file_object.read()
    
    kana = ''
    roma = ''
    kanji = ''
    wordtype = ''
    chinese = ''
    lesson = ''
    
    elsecount = 0
    addnew = 0
    updateword = 0
    
    for line in contents.splitlines():
        vals = re.findall(r'第(\d+)课', line)
        if len(vals) == 1:
            lesson = 'n2-1-%02d' % int(vals[0])
            continue
        vals = re.findall(r'-+', line)
        if len(vals) == 1:
            continue
        
        ok = False
        if not ok:
            vals = re.findall(r'(.*?)(（(.*?)）)*?\s〔(.*?)〕\s(.*)', line)
            if len(vals) == 1 and len(vals[0]) == 5:
                tup = vals[0]
                kana = tup[0].strip()
                roma = romkan.to_roma(kana)
                kanji = tup[2].strip()
                wordtype = tup[3].strip()
                chinese = tup[4].strip()
                ok = True
        
        if not ok:
            vals = line.split(' ')
            if len(vals) == 3:
                
                assert 0, vals
                # tup = vals[0]
                # kana = tup[0].strip()
                # roma = romkan.to_roma(kana)
                # wordtype = tup[1].strip()
                # chinese = tup[2].strip()
                # ok = True
            elif len(vals) == 2:
                # print(vals)
                # tup = vals[0]
                # kana = tup[0].strip()
                # arr = re.findall(r'(.*?)(（(.*?)）)', kana)
                # if len(arr) == 1 and len(arr[0]) == 3:
                #     print(arr)
                
               
                # kanji
                # roma = romkan.to_roma(kana)
                # chinese = tup[1].strip()
                # ok = True
                pass
            else:
                print(vals)
                pass
                
        if not ok:
            elsecount += 1
            continue

        info = {
            'roma': roma,
            'kanji': kanji,
            'wordtype': wordtype,
            'chinese': chinese,
            'lesson': [lesson]
        }
        
        # 多课同词则合并
        if kana in words.keys():
            # print(info)
            # print(words[kana])
            keys = words[kana].keys()
                
            if info['roma'] != words[kana]['roma']:
                assert 0, "roma not same"
            
            if info['kanji'] != words[kana]['kanji']:
                words[kana]['kanji'] = '{};{}'.format(words[kana]['kanji'], info['kanji'])
            
            # 没有则创建，有则比较
            if 'wordtype' not in keys:
                words[kana]['wordtype'] = info['wordtype']
            else:
                if info['wordtype'] != words[kana]['wordtype']:
                    words[kana]['wordtype'] = '{};{}'.format(words[kana]['wordtype'], info['wordtype'])
            
            if 'chinese' not in keys:
                words[kana]['chinese'] = info['chinese']
            else:
                if info['chinese'] != words[kana]['chinese']:
                    words[kana]['chinese'] = '{};{}'.format(words[kana]['chinese'], info['chinese'])
            
            if info['lesson'] not in words[kana]['lesson']:
                words[kana]['lesson'].append(info['lesson'][0])

            updateword += 1
        # 无重复则添加
        else:
            words[kana] = info
            addnew += 1

        # vals = re.findall(r'(.*?)（(.*?)）\s(.*)', line)
        # if len(vals) == 1 and len(vals[0]) == 3:
        #     tup = vals[0]
        #     roma = romkan.to_roma(tup[0])
        #     return (LINETYPE.SENTENCE, tup[0], tup[1], roma, tup[2], '', -1)

        
        
        
        # linetype, kana, kanji, roma, chinese, wordtype, lesson = processline(line)
        # if linetype == LINETYPE.LESSON:
        #     bookid = 'aaa'
        #     quote = "{}_{}".format(bookid, lesson)
        #     pass
        # elif linetype == LINETYPE.WORD:
        #     val = "\"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\"".format(kana, kanji, roma, chinese, wordtype, lesson)
        #     sql = sqltemplate.format(wordtable, val)
        #     sqls.append(sql)
        #     pass
        # elif linetype == LINETYPE.SENTENCE:
        #     val = "\"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\"".format(kana, kanji, roma, chinese, LINETYPE.SENTENCE, lesson)
        #     sql = sqltemplate.format(wordtable, val)
        #     sqls.append(sql)
        #     pass
        # elif linetype == LINETYPE.WORDS:
        #     for k, r in zip(kana, roma):
        #         val = "\"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\"".format(k, '', r, '', LINETYPE.WORDS, lesson)
        #         sql = sqltemplate.format(wordtable, val)
        #         sqls.append(sql)
        #     pass
        # elif linetype == LINETYPE.USELESS:
        #     pass
        # else:
        #     print(line)
        #     pass
        
    
    
    
    
    # sqls = []
    # sqltemplate = "INSERT INTO {} (kana, kanji, roma, chinese, wordtype, lesson) VALUES ({})"
    
    # /batchinserts(sqls)
    # print(sqls)
    print('add:{}, update:{}, else:{}'.format(addnew, updateword, elsecount))

def load(words, logger):
    # print(len(words))
    processfile(words, os.path.abspath("Newstandard.txt"))