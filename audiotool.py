import os, re
from pathlib import Path
from pydub import AudioSegment
from pydub.silence import split_on_silence

def convert_mp3_to_wav(filename,savename):
    '''
    将MP3格式转成wav格式
    :param filename: x.mp3文件
    :param savename: x.wav文件
    :return: sound
    '''
    sound = AudioSegment.from_mp3(filename)
    sound.export(savename, format="wav")
    return sound


def split_to_chunks_by_slience(fname, subdir, kanaarr):
    sound = AudioSegment.from_wav(fname)
    # loudness = sound.dBFS
    # print(loudness)
    
    chunks = split_on_silence(sound,
        # must be silent for at least half a second,沉默半秒
        min_silence_len=1000,
    
        # consider it silent if quieter than -16 dBFS
        silence_thresh=-45,
        keep_silence=400
    
    )
    print('总分段：', len(chunks))

    # 放弃长度小于2秒的录音片段
    # for i in list(range(len(chunks)))[::-1]:
    #     if len(chunks[i]) <= 2000 or len(chunks[i]) >= 10000:
    #         chunks.pop(i)
    # print('取有效分段(大于2s小于10s)：', len(chunks))
    
    # '''
    # for x in range(0,int(len(sound)/1000)):
    #     print(x,sound[x*1000:(x+1)*1000].max_dBFS)
    # '''
    
    if len(kanaarr) == len(chunks):
        for i, chunk in enumerate(chunks):
            chunk.export("{}/{}.wav".format(subdir, kanaarr[i]), format="wav")
            # print(i)
    else:
        for i, chunk in enumerate(chunks):
            if (i < len(kanaarr)):
                chunk.export("{}/{}_{}.wav".format(subdir, i, kanaarr[i]), format="wav")
            else:
                chunk.export("{}/{}_{}.wav".format(subdir, i, "???"), format="wav")
            # print(i)

def writeaudioinfo(rootdir, audiomap):
    for i in findAllFile(rootdir):
        nowPath = Path(i).resolve()
        audiomap[nowPath.stem] = "%s" % nowPath

def findAllFile(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            if re.match(r'.*\.wav', f):
                fullname = os.path.join(root, f)
                yield os.path.abspath(fullname)