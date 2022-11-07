# coding=utf8
# 上述标签定义了本文档的编码，与Python 2.x兼容。

import re
 
a = '--忽段落段:  ![ [douzo]yor~oshiku[onegaishimasu],   [どうぞ]よろしく[お願いします],    ](/home/abcde/work/PostgreSQL/primary/应用应用/./././im数据sql'
b = re.sub('\[|\]|~','',a)
print(b)   ## 于枫立马立正，全身绷直！