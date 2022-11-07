from Jpword import Jpword

class Jpdict:
    def __init__(self):
        self.dict = {}
        self.totalmerge = 0
        self.totaladd = 0
        pass

    def merge(self, newword):
        if newword.kana in self.dict.keys():
            self.dict[newword.kana].merge(newword)
            self.totalmerge += 1
        else:
            self.dict[newword.kana] = newword
            self.totaladd += 1
        pass
    
    def show(self):
        for key, value in self.dict.items():
            value.show()
        print(len(self.dict))

    def getitems(self):
        return self.dict.items()

