# japanese_words

此项目仅用于本人背单词与练习键盘输入使用


## 操作指南

### 初始化数据

```
$ python3 createdb.py
```

此方法仅运行一次即可，作用是初始化数据库

### 启动程序

```
$ python3 play.py -k19

参数"19"的作用可以参考run.json中的配置
```

启动后如果想去除杂乱的字符可以运行下面的替换后再次启动即可

```
$ perl -i.bak -pe 's/contents0, kana, contents1, newchn, contents2, newroma, kanji, contents3/"", "", "", newchn, "", "", "", ""/g' play.py
```

### 其余操作

启动后可有下列操作

|按键|说明|
|-|-|
|q|exit|
|1|prev|
|`|next|
|9|手动标记+1|
|0|手动标记-1|
|6|查词典|


## 功能列表

- 【ok】1 运行中可以手动调整next与prev进行重复练习
- 2 加入计时器
- 【ok】3 统计数据，展示正确失败次数
- 【ok】4 加入生词本，生词本去重
- 【ok】5 可以在配置里有多个sql，根据参数选择运行的sql
- 【ok】6 添加加、减生词与失败次数的记录功能
- 【ok】7 添加记录正确的次数
- 【ok】8 加入“大家的日本语”，“新标准日本语”
- 【ok】9 每次练习后可以再选择是否again一次错误的单词
- 【ok】10 查词典
- 【ok】11 添加手动录入的词库
- 12 数据库属性值去重
- 【ok】13 自动保存最末次练习的错误单词列表
- 【ok】14 启动时候可通过参数-klast练习上一次的错误单词列表
- 【ok】15 添加字段记录单词最后一次测试时间，并提供基于此时间进行计算的取词方式。如key：“1day”就是取一天前练习过的单词，并还可以配合其他字段进行再次过滤
- 【ok】 16 拆分单词表与统计表
- 【ok】 17 可以通过参数选择重置数据库所有表（-i），以及仅更新单词表，保留统计表（-r），默认无参数则是合并文件词库到db中
- 【ok】 18 添加“大家学标准日本语初级”单词表
