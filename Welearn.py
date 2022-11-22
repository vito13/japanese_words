import xlrd
from Jpword import Jpword

def load(jpdict, logger):
    fname = 'dajiaxue/dajiaxue.xlsx'
    data = xlrd.open_workbook(fname)
    logger.debug("load file {}".format(fname))
    for sheetname in data.sheet_names():
        table = data.sheet_by_name(sheetname)
        # 获取表格行数
        nrows = table.nrows
        logger.debug("lesson {}, words: {}".format(sheetname, nrows))

        for r in range(1, nrows):
            tone, kana, kanji, chinese = table.row_values(r)
            if type(tone) == float:
                tone = str(int(tone))
            # logger.debug(row[0])
            w = Jpword(kana)
            w.kanji = kanji
            w.chinese = chinese
            w.tone = tone
            w.lesson.append('w-1-%02d' % int(sheetname))
            jpdict.merge(w)