#!/usr/bin/python3
import os
import re
import sys
import sqlite3
import romkan
import logging
import json
from hyperparameters import global_var
import csv
from os import path 


dbfile = global_var.get_value('dbfile')
wordtable = global_var.get_value('wordtable')
log = sys.argv[0] + '.log'
dbinfo = global_var.get_value('dbinfo')



def get_words_from_files(files):
    h = re.compile(r"(.*?)\[(.*?)\] (.*)")
    words = {}
    for fn in files:
        #print fn
        chapter = int(fn.split(".")[1])
        filename = os.path.abspath(fn)
        logging.debug(filename)
        with open(filename, encoding ='utf-8') as file:
            # skip intro
            for i in range(4): line = file.readline()
            while line:
                line = file.readline()
                # end of line
                if line.startswith("#end"): break
                m = h.match(line)
                word, kana, meaning = m.group(1), m.group(2), m.group(3)
                words[kana] = {"chapter":chapter, "meaning":meaning}
                logging.debug("kana: {}, meaning: {}".format(kana, meaning))
    return words

def updateen(cs):
    files = []
    for i in range(1,26): files.append("Minna_no_nihongo/Minna_no_nihongo_1.%02d.txt" % i)
    for i in range(26,51): files.append("Minna_no_nihongo/Minna_no_nihongo_2.%02d.txt" % i)

    vals = []
    data = get_words_from_files(files)
    for key, value in data.items():
        kana = key
        lesson = value['chapter']
        english = value['meaning'].replace('/', '')
        vals.append([english, kana])

    cs.executemany('''
        UPDATE jpwords set english = ? WHERE kana = ?
    ''', vals)

def addwords(cs):
    filepath = os.path.abspath("Minnano")
    file = os.listdir(filepath)
    for f in file:
        h = re.compile(r"大家的日语第二版初级(\d)_(\d\d)\.csv")
        m = h.match(f)
        booknum, lesson = m.group(1), int(m.group(2))
        logging.debug("{}, {}, {}".format(f, booknum, lesson))

        filename = path.join(filepath, f)
        vals = []
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ')
            for row in reader:
                arr = row[0].split(',')
                # if len(arr) < 5:
                #     print(row[0])
                
                kana = arr[1]
                kanji = arr[2]
                tone = arr[3]
                wordtype = arr[4]
                chinese = arr[5]

                booklesson = 'm-{}-{}'.format(1, lesson)
                roma = romkan.to_roma(kana)
                
                data = [kana, kanji, tone, wordtype, chinese, booklesson, roma]
                vals.append(data)
                logging.debug(data)
            
            cs.executemany('''
                INSERT INTO jpwords(kana, kanji, tone, wordtype, chinese, booklesson, roma) VALUES(?,?,?,?,?,?,?)
            ''', vals)


if __name__ == '__main__':
    if os.path.exists(log):
        os.unlink(log)
    logging.basicConfig(filename = log, level = logging.DEBUG, format = '%(asctime)s - %(levelname)s - %(message)s')
    
    conn = sqlite3.connect(dbfile)
    cs = conn.cursor()
    addwords(cs)
    updateen(cs)
    cs.close()
    conn.commit()
    conn.close()
