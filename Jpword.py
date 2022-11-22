import romkan
import re

def mergeproperty(a, b):
    if a in b: return b
    elif b in a: return a
    else: return extendproperty(a, b)

def extendproperty(a, b):
    if a == '': return b
    elif b == '': return a
    seta = set(re.split(r'[、\、\;;,，\，\；]', a))
    setb = set(re.split(r'[、\、\;;,，\，\；]', b))
    setall = seta.union(setb)
    ret = "；".join(setall)
    return ret

class Jpword:
    def __init__(self, *kwargs):
        if len(kwargs) == 1:
            self.kana = kwargs[0]
            self.kanji = ''
            self.roma = romkan.to_roma(self.kana)
            self.chinese = ''
            self.english = ''
            self.wordtype = ''
            self.tone = ''
            self.lesson = []
            self.description = ''
            self.nlevel = ''
        else:
            self.kana = kwargs[0]
            self.kanji = kwargs[1]
            self.roma = kwargs[2]
            self.chinese = kwargs[3]
            self.english = kwargs[4]
            self.wordtype = kwargs[5]
            self.tone = kwargs[6]
            self.lesson = kwargs[7]
            self.description = kwargs[8]
            self.nlevel = kwargs[9]
    
    def merge(self, newword):
        self.kanji = mergeproperty(self.kanji, newword.kanji)
        self.chinese = mergeproperty(self.chinese, newword.chinese)
        self.english = mergeproperty(self.english, newword.english)
        self.tone = mergeproperty(self.tone, newword.tone)
        self.wordtype = mergeproperty(self.wordtype, newword.wordtype)
        if (len(newword.lesson) > 0) and (newword.lesson[0] not in self.lesson):
            self.lesson.append(newword.lesson[0])
        pass

    def show(self):
        print('---')
        print('kana: ', self.kana)
        print('kanji: ', self.kanji)
        print('roma: ', self.roma)
        print('chinese: ', self.chinese)
        print('english: ', self.english)
        print('wordtype: ', self.wordtype)
        print('tone: ', self.tone)
        print('lesson: ', self.lesson)
