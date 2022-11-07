#!/usr/bin/python3
import os
import re
import sys
import logging
import csv
from Jpword import Jpword
from Jpdict import Jpdict

def load_newstandard(jpdict, logger):
    filename = os.path.abspath("words.csv")
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for arr in reader:
            size = len(arr)
            if (size != 7):
                assert size == 7, arr

            kana = []
            tone = []
            h = re.compile(r"((.*?)@(\d))+?")
            m = h.findall(arr[0].strip())
            
            if len(m) < 1:
                kana.append(arr[0].strip())
            else:
                for part in m:
                    x, k, t = part
                    kana.append(k)
                    tone.append(t)
            
            w = Jpword(''.join(kana))
            w.kanji = arr[1].strip()
            w.chinese = arr[3].strip()
            w.wordtype = arr[2].strip()
            w.tone = ';'.join(tone)
            lesson = arr[5].strip()
            if 'm' in lesson:
                w.lesson.append(lesson)
            else:
                w.lesson.append('n2-1-%2d' % int(lesson))
            jpdict.merge(w)


def load(jpdict, logger):
    load_newstandard(jpdict, logger)