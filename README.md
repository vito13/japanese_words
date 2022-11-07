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


## 功能列表

- 【ok】1 运行中可以手动调整next与prev进行重复练习
- 2 加入计时器
- 【ok】3 统计数据，展示正确失败次数
- 【ok】4 加入生词本，生词本去重
- 【ok】5 可以在配置里有多个sql，根据参数选择运行的sql
- 【ok】6 添加加、减生词与失败次数的记录功能
- 【ok】7 添加记录正确的次数
- 【ok】8 加入“大家的日本语”，“新标准日本语”


