#!/usr/bin/python3



import os
import sys
import sqlite3
import logging
import json
from hyperparameters import global_var
import Minnano
import Newstandard

dbfile = global_var.get_value('dbfile')
wordtable = global_var.get_value('wordtable')
words = {}
logger = None

def createdb():
    conn = sqlite3.connect(dbfile)
    cs = conn.cursor()
    sql = '''
    CREATE TABLE if not exists {0} (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        kana TEXT NOT NULL,
        kanji TEXT,
        roma TEXT NOT NULL,
        chinese TEXT NOT NULL,
        english TEXT DEFAULT "",
        
        wordtype TEXT DEFAULT "",
        tone TEXT DEFAULT "",
        lesson TEXT DEFAULT "",
        description TEXT DEFAULT "",
        nlevel INTEGER DEFAULT 0,
        
        increase INTEGER NOT NULL DEFAULT 0,
        decrease INTEGER NOT NULL DEFAULT 0,
        correct INTEGER NOT NULL DEFAULT 0,
        wrong INTEGER NOT NULL DEFAULT 0
        );
    '''.format(wordtable)
    logger.debug(sql)
    cs.execute(sql)
    
    vals = []
    for kana, value in words.items():
        vals.append([
            kana,
            value['kanji'],
            value.get('tone', ''),
            value.get('wordtype', ''),
            value.get('chinese', ''), 
            ';'.join(value['lesson']),
            value['roma'],
            value.get('english', '')
        ])
    
    cs.executemany('''
        INSERT INTO jpwords(kana, kanji, tone, wordtype, chinese, lesson, roma, english) VALUES(?,?,?,?,?,?,?,?)
        ''', vals)
    
    logger.debug('add {} words'.format(len(words)))
    cs.close()
    conn.commit()
    conn.close()

if __name__ == '__main__':
    # init log
    logfile = sys.argv[0] + '.log'
    if os.path.exists(logfile):
        os.unlink(logfile)
    logging.basicConfig(filename = logfile, level = logging.DEBUG, format = '%(asctime)s - %(levelname)s - %(message)s')
    logger = logging
    
    # init db
    if os.path.exists(dbfile):
        os.unlink(dbfile)
    # Minnano.load(words, logger)
    Newstandard.load(words, logger)
    createdb()

