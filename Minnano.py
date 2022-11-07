#!/usr/bin/python3
import os
import re
import sys
import romkan
import logging
from hyperparameters import global_var
import csv
from os import path


# lesson说明： m2-1-03 # 第2版, 初级, 第03课

def get_words_from_files(files):
    h = re.compile(r"(.*?)\[(.*?)\] (.*)")
    data = {}
    for fn in files:
        #print fn
        chapter = int(fn.split(".")[1])
        filename = os.path.abspath(fn)
        # logger.debug(filename)
        with open(filename, encoding ='utf-8') as file:
            # skip intro
            for i in range(4): line = file.readline()
            while line:
                line = file.readline()
                # end of line
                if line.startswith("#end"): break
                m = h.match(line)
                kanji, kana, english = m.group(1).strip(), m.group(2).strip(), m.group(3).replace('/', '').strip()
                if kana == kanji:
                    kanji = ''
                data[kana] = {"kanji": kanji, "chapter":chapter, "english":english}
    return data

def updateen(words, logger):
    files = []
    for i in range(1,26): files.append("Minna_no_nihongo/Minna_no_nihongo_1.%02d.txt" % i)
    for i in range(26,51): files.append("Minna_no_nihongo/Minna_no_nihongo_2.%02d.txt" % i)

    data = get_words_from_files(files)
    existwords = words.keys()
    
    for kana, value in data.items():
        if kana in existwords:
            words[kana]['english'] = value['english']
            words[kana]['lesson'].append('m1-1-%02d' % int(value['chapter']))
        else:
            info = {
                'roma': romkan.to_roma(kana),
                'kanji': value['kanji'],
                'english': value['english'],
                'lesson': ['m1-1-%02d' % int(value['chapter'])]
            }
            words[kana] = info

def addwords(words, logger):
    filepath = os.path.abspath("Minnano")
    file = os.listdir(filepath)
    for f in file:
        h = re.compile(r"大家的日语第二版初级(\d)_(\d\d)\.csv")
        m = h.match(f)
        booknum, lesson = m.group(1), int(m.group(2))
        logger.debug("{}, {}, {}".format(f, booknum, lesson))

        filename = path.join(filepath, f)
        vals = []
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ')
            for row in reader:
                arr = row[0].split(',')
                kana = arr[1].strip()
                info = {
                    'roma': romkan.to_roma(kana),
                    'kanji': arr[2].strip(),
                    'tone': arr[3].strip(),
                    'wordtype': arr[4].strip(),
                    'chinese': arr[5].strip(),
                    'lesson': ['m2-1-%02d' % lesson]
                }
                # 多课同词则合并
                if kana in words.keys():
                    if info['roma'] != words[kana]['roma']:
                        assert 0, "roma not same"
                    
                    if info['kanji'] != words[kana]['kanji']:
                        words[kana]['kanji'] = '{};{}'.format(words[kana]['kanji'], info['kanji'])
                    
                    if info['tone'] != words[kana]['tone']:
                        words[kana]['tone'] = '{};{}'.format(words[kana]['tone'], info['tone'])
                        
                    if info['wordtype'] != words[kana]['wordtype']:
                        words[kana]['wordtype'] = '{};{}'.format(words[kana]['wordtype'], info['wordtype'])
                    
                    if info['chinese'] != words[kana]['chinese']:
                        words[kana]['chinese'] = '{};{}'.format(words[kana]['chinese'], info['chinese'])
                    
                    if info['lesson'] not in words[kana]['lesson']:
                        words[kana]['lesson'].append(info['lesson'][0])
                
                # 无重复则添加
                else:
                    words[kana] = info

def load(words, logger):
    addwords(words, logger)
    updateen(words, logger)
