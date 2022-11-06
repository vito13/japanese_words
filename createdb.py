#!/usr/bin/python3



import os
import sys
import sqlite3
import logging
import json
from hyperparameters import global_var
import subprocess

dbfile = global_var.get_value('dbfile')
wordtable = global_var.get_value('wordtable')
log = sys.argv[0] + '.log'
dbinfo = global_var.get_value('dbinfo')

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
        booklesson TEXT DEFAULT "",
        description TEXT DEFAULT "",
        nlevel INTEGER DEFAULT 0,
        
        increase INTEGER NOT NULL DEFAULT 0,
        decrease INTEGER NOT NULL DEFAULT 0,
        correct INTEGER NOT NULL DEFAULT 0,
        wrong INTEGER NOT NULL DEFAULT 0
        );
    '''.format(wordtable)
    logging.debug(sql)
    cs.execute(sql)
    cs.close()
    conn.commit()
    conn.close()

if __name__ == '__main__':
    if os.path.exists(log):
        os.unlink(log)
    logging.basicConfig(filename = log, level = logging.DEBUG, format = '%(asctime)s - %(levelname)s - %(message)s')
    
    if os.path.exists(dbfile):
        os.unlink(dbfile)
    createdb()

    with open(dbinfo, 'r',encoding='utf-8') as f:
        info = json.load(f)
        for key, value in info.items():
            cmd = 'python3 {}'.format(key)
            ret = subprocess.getoutput(cmd)
            print(ret)
