import time
from pygame import mixer


mixer.init()
mixer.music.load("dajiaxue/1.wav")
mixer.music.play()
# while mixer.music.get_busy():  # wait for music to finish playing
#     time.sleep(1)

# infinite loop
while True:
      
    print("Press 'p' to pause, 'r' to resume")
    print("Press 'e' to exit the program")
    query = input("  ")
      
    if query == 'p':
  
        # Pausing the music
        mixer.music.pause()     
    elif query == 'r':
  
        # Resuming the music
        mixer.music.unpause()
    elif query == 'e':
  
        # Stop the mixer
        mixer.music.stop()
        break



def convert_mp3_to_wav(filename,savename):
    '''
    将MP3格式转成wav格式
    :param filename: x.mp3文件
    :param savename: x.wav文件
    :return: sound
    '''
    from pydub import AudioSegment
    sound = AudioSegment.from_mp3(filename)
    sound.export(savename, format="wav")
    return sound

def recognize_word(filename):
    '''
    打印wav文件的转写结果
    :param filename: wav文件
    :return: 转写结果 str
    '''
    import speech_recognition as sr
    r = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = r.record(source)  # read the entire audio file
    res = r.recognize_google(audio)  # 注意要挂梯子哦
    res1 = res.split(" ")
    result=" ".join(res1)
    print(result,type(result))
    return result

def split_to_chunks_by_slience(sound,savedir='word_wav'):
    from pydub.silence import split_on_silence
    import os
    if not os.path.exists(savedir):
        os.mkdir(savedir)
    chunks = split_on_silence(sound,
                              # must be silent for at least half a second,沉默半秒
                              min_silence_len=430,
                              # consider it silent if quieter than -16 dBFS
                              silence_thresh=-45,
                              keep_silence=400
                              )
    print('总分段：', len(chunks))

    for i, chunk in enumerate(chunks):

        chunk.export(os.path.join(savedir,"chunk{0}.wav".format(i)), format="wav")
        newname=recognize_word(os.path.join(savedir,"chunk{0}.wav".format(i)))+'.wav'
        try:
            os.rename(os.path.join(savedir,"chunk{0}.wav".format(i)),os.path.join(savedir,newname))
        except FileExistsError:
            os.remove(os.path.join(savedir,"chunk{0}.wav".format(i)))
        if i==5 :break
        # print(i)

def split_to_chunks_by_slience(sound,savedir='word_wav'):
    '''
    根据沉默片段来分割词，并且合并念两遍的
    :param sound:
    :param savedir:
    :return:
    '''
    from pydub.silence import split_on_silence
    import os
    from speech_recognition import UnknownValueError

    chunks = split_on_silence(sound,
                              # must be silent for at least half a second,沉默半秒
                              min_silence_len=230,
                              # consider it silent if quieter than -16 dBFS
                              silence_thresh=-45,
                              keep_silence=400
                              )
    print('总分段：', len(chunks))
    
    # for i, chunk in enumerate(chunks):
    #     print('now is num:',i)
    #     chunk.export(os.path.join(savedir,"chunk{0}.wav".format(i)), format="wav")
    #     try:
    #         newname=recognize_word(os.path.join(savedir,"chunk{0}.wav".format(i)))+'.wav'
    #         try:
    #             os.rename(os.path.join(savedir,"chunk{0}.wav".format(i)),os.path.join(savedir,newname))
    #         except FileExistsError:
    #             # 加载需要合并的两个mp3音频
    #             parameters = None
    #             input_word_1 = AudioSegment.from_mp3(os.path.join(savedir,newname))  # 需要修改的地方：音频1
    #             input_word_2 = AudioSegment.from_mp3(os.path.join(savedir,"chunk{0}.wav".format(i)))  # 需要修改的地方：音频2
    #             # 合并音频
    #             output_word = input_word_1 + input_word_2
    #             # 简单输入合并之后的音频
    #             os.remove(os.path.join(savedir,newname))    #先删后建
    #             os.remove(os.path.join(savedir,"chunk{0}.wav".format(i)))
    #             output_word.export(os.path.join(savedir,newname), format="wav")  # 前面是保存路径，后面是保存格式
    #     except UnknownValueError:	##识别不出来
    #         print('unkown word')


# convert_mp3_to_wav("danzi.mp3", "danzi.wav")
# recognize_word("danzi.wav")
# split_to_chunks_by_slience("danzi.wav")


def split():
    from pydub import AudioSegment
    from pydub.silence import split_on_silence

    sound = AudioSegment.from_mp3("danzi.wav")
    loudness = sound.dBFS
    print(loudness)
    
    chunks = split_on_silence(sound,
        # must be silent for at least half a second,沉默半秒
        min_silence_len=430,
    
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
    
    '''
    for x in range(0,int(len(sound)/1000)):
        print(x,sound[x*1000:(x+1)*1000].max_dBFS)
    '''
    
    for i, chunk in enumerate(chunks):
        chunk.export("wav/chunk{0}.wav".format(i), format="wav")
        print(i)
        
        
# import speech_recognition as sr
# r = sr.Recognizer()
# with sr.AudioFile("單字02.wav") as source:
#     audio = r.record(source)  # read the entire audio file
# res = r.recognize_sphinx(audio)  # 注意要挂梯子哦
# res1 = res.split(" ")
# result=" ".join(res1)
# print(result,type(result))