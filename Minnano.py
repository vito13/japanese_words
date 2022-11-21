#!/usr/bin/python3
import os
import re
import sys
import logging
import csv
from os import path
from Jpword import Jpword


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

def load_minnano_lev1(jpdict, logger):
    files = []
    for i in range(1,26): files.append("Minna_no_nihongo/Minna_no_nihongo_1.%02d.txt" % i)
    for i in range(26,51): files.append("Minna_no_nihongo/Minna_no_nihongo_2.%02d.txt" % i)
    data = get_words_from_files(files)
    for kana, value in data.items():
        w = Jpword(kana)
        w.kanji = value['kanji']
        w.english = value['english']
        w.lesson.append('m1-1-%02d' % int(value['chapter']))
        jpdict.merge(w)
    
def load_minnano_lev2(jpdict, logger):
    filepath = os.path.abspath("Minnano")
    file = os.listdir(filepath)
    for f in file:
        h = re.compile(r"大家的日语第二版初级(\d)_(\d\d)\.csv")
        m = h.match(f)
        booknum, lesson = m.group(1), int(m.group(2))
        logger.debug("{}, {}, {}".format(f, booknum, lesson))

        filename = path.join(filepath, f)
        vals = []
        with open(filename, newline='', encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile, delimiter=' ')
            for row in reader:
                logger.debug(row[0])
                arr = row[0].split(',')
                kana = arr[1]
                w = Jpword(kana)
                w.kanji = arr[2]
                w.chinese = arr[5]
                w.wordtype = arr[4]
                w.tone = arr[3]
                w.lesson.append('m2-1-%02d' % lesson)
                jpdict.merge(w)

def load(jpdict, logger):
    load_minnano_lev2(jpdict, logger)
    # load_minnano_lev1(jpdict, logger)
