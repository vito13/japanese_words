import xlrd, os, shutil
from Jpword import Jpword
import audiotool
from pathlib import Path

def load(jpdict, logger, audiomap):
    os.chdir('dajiaxue')
    fname = 'dajiaxue.xlsx'
    data = xlrd.open_workbook(fname)
    logger.debug("load file {}".format(fname))
    for sheetname in data.sheet_names():
        table = data.sheet_by_name(sheetname)
        # 获取表格行数
        nrows = table.nrows
        logger.debug("lesson {}, words: {}".format(sheetname, nrows))
        kanaarr = []
        for r in range(0, nrows):
            tone, kana, kanji, chinese = table.row_values(r)
            if type(tone) == float:
                tone = str(int(tone))
            # logger.debug(row[0])
            kanaarr.append(kana)
            w = Jpword(kana)
            w.kanji = kanji
            w.chinese = chinese
            w.tone = tone
            w.lesson.append('w-1-%02d' % int(sheetname))
            jpdict.merge(w)
        handleaudio(sheetname, kanaarr)
        audiotool.writeaudioinfo(".", audiomap)
    os.chdir('..')
    
def handleaudio(sheetname, kanaarr):
    mp3 = "{}.mp3".format(sheetname)
    wav = "{}.wav".format(sheetname)
    if os.path.isfile(mp3):
        subdir = "{}".format(sheetname)
        if os.path.exists(subdir):
            if len(os.listdir(subdir)) == len(kanaarr):
                print("{} no changes".format(subdir))
                return
            shutil.rmtree(subdir)
        os.mkdir(subdir)
        audiotool.convert_mp3_to_wav(mp3, wav)
        audiotool.split_to_chunks_by_slience(wav, subdir, kanaarr)
        os.unlink(wav)
    else:
        assert(0)
