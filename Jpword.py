import romkan

def extendproperty(a, b):
    if a == '': return b
    if b == '': return a
    return '{};{}'.format(a, b)

class Jpword:
    def __init__(self, kana):
        self.kana = kana
        self.kanji = ''
        self.roma = romkan.to_roma(kana)
        self.chinese = ''
        self.english = ''
        self.wordtype = ''
        self.tone = ''
        self.lesson = []
        self.description = ''
        self.nlevel = ''
    
    def merge(self, newword):
        if self.kanji != newword.kanji:
            self.kanji = extendproperty(self.kanji, newword.kanji)
        if self.chinese != newword.chinese:
            self.chinese = extendproperty(self.chinese, newword.chinese)
        if self.english != newword.english:
            self.english = extendproperty(self.english, newword.english)
        if self.tone != newword.tone:
            self.tone = extendproperty(self.tone, newword.tone)
        if self.wordtype != newword.wordtype:
            self.wordtype = extendproperty(self.wordtype, newword.wordtype)
        if newword.lesson[0] not in self.lesson:
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
