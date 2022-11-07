from Jpword import Jpword

class Jpdict:
    def __init__(self):
        self.dict = {}
        pass

    def merge(self, newword):
        if newword.kana in self.dict.keys():
            self.dict[newword.kana].merge(newword)
        else:
            self.dict[newword.kana] = newword
        pass
    
    def show(self):
        for key, value in self.dict.items():
            value.show()
        print(len(self.dict))

    def getitems(self):
        return self.dict.items()


# if __name__ == '__main__':
#     jpdict = Jpdict()
#     w = Jpword('1')
#     w.kanji = '1'
#     w.roma = '1'
#     w.chinese = '1'
#     w.english = '1'
#     w.wordtype = '1'
#     w.tone = '1'
#     w.lesson.append('1')
#     w.description = '1'
#     w.nlevel = '1'
 
#     jpdict.merge(w)
    
#     w = Jpword('1')
#     w.kanji = '2'
#     w.roma = '2'
#     w.chinese = '2'
#     w.english = '2'
#     w.wordtype = '2'
#     w.tone = '2'
#     w.lesson.append('1')
#     w.description = '2'
#     w.nlevel = ['2']
#     jpdict.merge(w)
#     jpdict.show()

    
