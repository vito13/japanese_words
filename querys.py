from hyperparameters import global_var
statstablename = global_var.get_value('stats')
wordtablename = global_var.get_value('wordtable')
wordtable = "SELECT * FROM {} ".format(wordtablename)
statstable = "SELECT kana FROM {} ".format(statstablename)
lessonre = '%w-1-08%'
def limit_offset(limit, offset = 0): return " limit {} offset {} ".format(limit, offset)
lessondata = wordtable + "where lesson like '{}'".format(lessonre)
word = lessondata + " and tone != ''"
sentence = lessondata + " and tone == ''"
new = lessondata + " and kana in (" + statstable + " where increase > decrease)"
allnew = wordtable + "where kana in (" + statstable + " where increase > decrease)"
wrong = lessondata + " and kana in (" + statstable + " where wrong > 0 order by wrong desc)"
oneday = lessondata + " and kana in (" + statstable + " where strftime('%s','now') - lasttime < 86400)"
resetnew = "update {} set decrease = increase where kana in (SELECT kana FROM {} where lesson like '{}')".format(statstablename, wordtablename, lessonre)



sqls = {
    'w': word,
    's': sentence,
    'new': new,
    'anew': allnew,
    'rnew': resetnew,
    'newlim': new + limit_offset(4, 4),
    'wrong': wrong,
    '1day': oneday
    }
