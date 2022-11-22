import pprint


lessonre = '%w-1-03%'
lessondata = "SELECT * FROM jpwords where lesson like '{}'".format(lessonre)
word = lessondata + " and tone != ''"
sentence = lessondata + " and tone == ''"


sqls = {'w': word, 's': sentence}

# print(pprint.pformat(sqls))
fileObj = open('myCats.py', 'w')
fileObj.write('sqls = ' + pprint.pformat(sqls) + '\n')
fileObj.close()

# import myCats
# print(myCats.cats)
# print(myCats.cats[0])
# print(myCats.cats[0]['name'])
