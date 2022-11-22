from hyperparameters import global_var
statstablename = global_var.get_value('stats')
wordtablename = global_var.get_value('wordtable')
wordtable = "SELECT * FROM {} ".format(wordtablename)
statstable = "SELECT kana FROM {} ".format(statstablename)
lessonre = '%w-1-03%'
random = " ORDER BY RANDOM() "
limit_offset = " limit {} offset {} ".format(10, 10)
random_limit_offset = random + limit_offset
lessondata = wordtable + "where lesson like '{}'".format(lessonre)
word = lessondata + " and tone != ''"
sentence = lessondata + " and tone == ''"
new = lessondata + " and kana in (" + statstable + " where increase > decrease)"
wrong = lessondata + " and kana in (" + statstable + " where wrong > 0 order by wrong desc)"
oneday = lessondata + " and kana in (" + statstable + " where strftime('%s','now') - lasttime < 86400)" + random_limit_offset

sqls = {
    'w': word,
    's': sentence,
    'new': new,
    'wrong': wrong,
    '1day': oneday
    }
