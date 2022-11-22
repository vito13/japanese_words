#!/usr/bin/python3
import os, getopt
import sys
import sqlite3
import logging
import json
from hyperparameters import global_var
import Minnano
import Newstandard
import Welearn
import Custom
from Jpdict import Jpdict
from Jpword import Jpword
from datetime import timedelta, datetime

dbfile = global_var.get_value('dbfile')
wordtable = global_var.get_value('wordtable')
stats = global_var.get_value('stats')
words = {}
logger = None

def createtables():
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
        nlevel INTEGER DEFAULT 0
        );
    '''.format(wordtable)
    logger.debug(sql)
    cs.execute(sql)

    sql = '''
    CREATE TABLE if not exists {0} (
        kana TEXT PRIMARY KEY,
        increase INTEGER NOT NULL DEFAULT 0,
        decrease INTEGER NOT NULL DEFAULT 0,
        correct INTEGER NOT NULL DEFAULT 0,
        wrong INTEGER NOT NULL DEFAULT 0,
        lasttime REAL NOT NULL DEFAULT 0
        );
    '''.format(stats)
    logger.debug(sql)
    cs.execute(sql)
    
    cs.close()
    conn.commit()
    conn.close()

def getdbwords(jpdict):
    conn = sqlite3.connect(dbfile)
    cs = conn.cursor()
    cs.execute("select * from {}".format(wordtable))
    data = cs.fetchall()
    cs.close()
    conn.close()
    
    for tup in data:
        wordid, kana, kanji, roma, chinese, english, wordtype, tone, lesson, description, nlevel = tup
        lessonarr = lesson.split(',')
        jpdict.merge(Jpword(kana, kanji, roma, chinese, english, wordtype, tone, lessonarr, description, nlevel))


def resetwordtable(jpdict):
    conn = sqlite3.connect(dbfile)
    cs = conn.cursor()

    # 清表
    sql = 'delete from {}'.format(wordtable)
    logger.debug(sql)
    cs.execute(sql)
    
    # 自增归0
    sql = 'update sqlite_sequence SET seq = 0 where name = \'{}\''.format(wordtable)
    logger.debug(sql)
    cs.execute(sql)

    # 重新添加所有
    items = jpdict.getitems()
    if len(items):
        vals = []
        for kana, value in items:
            v = [
                value.kana,
                value.kanji,
                value.tone,
                value.wordtype,
                value.chinese,
                ';'.join(value.lesson),
                value.roma,
                value.english,
            ]
            vals.append(v)
        cs.executemany('''
            INSERT INTO jpwords(kana, kanji, tone, wordtype, chinese, lesson, roma, english) VALUES(?,?,?,?,?,?,?,?)
            ''', vals)
        logger.debug('Total Add {} words to db'.format(len(vals)))
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
    jpdict = Jpdict()
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], '-i-r', ['init', 'reset'])
    except getopt.GetoptError:
        print('python3 {}'.format(sys.argv[0]))
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-i','--init'):
            logger.debug("=== remove db file, create all table ===")
            if os.path.exists(dbfile):
                os.unlink(dbfile)
            createtables()
        elif opt in ('-r','--reset'):
            logger.debug("=== clear word table, reserve stats table ===")
            resetwordtable(jpdict)
            
    # load word from db
    getdbwords(jpdict)
    logger.debug("=== After reading database ===")
    jpdict.total(logger)

    
    # load word from file
    # Minnano.load(jpdict, logger)
    # Newstandard.load(jpdict, logger)
    # Custom.load(jpdict, logger)
    Welearn.load(jpdict, logger)
    logger.debug("=== After reading file ===")
    jpdict.total(logger)

    # reset table
    logger.debug("=== reset word table ===")
    resetwordtable(jpdict)
   
