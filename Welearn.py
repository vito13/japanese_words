import xlrd
from Jpword import Jpword

def load(jpdict, logger):
    data = xlrd.open_workbook('dajiaxue/dajiaxue.xlsx')
    for sheetname in data.sheet_names():
        table = data.sheet_by_name(sheetname)
        # 获取表格行数
        nrows = table.nrows
        print("表格",sheetname,"一共有",nrows,"行")

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