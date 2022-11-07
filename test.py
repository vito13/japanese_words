# coding=utf8
# 上述标签定义了本文档的编码，与Python 2.x兼容。

import re

regex = r"((.*?)@(\d))+?"

test_str = "じかんに@4おわれる@0"

h = re.compile(r"((.*?)@(\d))+?")
m = h.findall(test_str)

print(m)