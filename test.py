
import os
import re
import sys
import sqlite3
import random

from collections import namedtuple

User = namedtuple("User", ["name", "age", "height"]) # 第一个参数为类名，后面为参数




user = None  # *user_tuple的作用就是将tuple解包
if 10:
    user_tuple2 = ("aaa", 10, 201)
    user =  User(*user_tuple2)


print(user.age, user.name, user.height)
