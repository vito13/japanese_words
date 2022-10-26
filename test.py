import sqlite3
import os
def check(db_name,table_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    sql = '''SELECT tbl_name FROM sqlite_master WHERE type = 'table' '''
    cursor.execute(sql)
    values = cursor.fetchall()
    tables = []
    for v in values:
        tables.append(v[0])
    if table_name not in tables:
        return False # 可以建表
    else:
        return True # 不能建表
def find_tb():
    cur.execute("select * from scores")
    # 提取查询到的数据
    return cur.fetchall()
def zcd():
    os.system('cls')
    print("学生分数管理系统")
    print("1.增加学生分数信息")
    print("2.查看全部学生分数")
    print("3.查询分数段内学生分数")
    print("4.退出")
 
if __name__ == '__main__':
    # 创建与数据库的连接
    conn = sqlite3.connect('stuents_scores.db')
    #创建一个游标 cursor
    cur = conn.cursor()
    # 如果没有表则执行建表的sql语句
    if (check("stuents_scores.db","scores") == False):
        sql_text_1 = '''CREATE TABLE scores
                (姓名 TEXT,
                    班级 TEXT,
                    性别 TEXT,
                    语文 NUMBER,
                    数学 NUMBER,
                    英语 NUMBER,
                    总分 NUMBER);'''
        # 执行sql语句
        cur.execute(sql_text_1)
    zcd()
    while True:
        op = int(input("请输入:"))
        if op == 1:
            S_name = input("请输入要添加的学生的姓名(如:张三):")
            S_class = input("请输入要添加的学生的班级(如:一班):")
            S_xb = input("请输入该学生性别:")
            S_Chinese = int(input("请输入该学生语文成绩(只输入一个数字,如:82):"))
            S_Maths = int(input("请输入该学生数学成绩(只输入一个数字,如:95):"))
            S_English = int(input("请输入该学生英语成绩(只输入一个数字,如:98):"))
            S_gj = S_Maths+S_Chinese+S_English # 总分
            data = [(S_name, S_class, S_xb, S_Chinese, S_Maths, S_English,S_gj)]
            cur.executemany('INSERT INTO scores VALUES (?,?,?,?,?,?,?)', data)
            conn.commit()
            # cur.close()
            # conn.close()
            print("成功!")
            os.system('pause')
            os.system('cls')
            zcd()
        elif op == 2:
            info_list = find_tb()
            print("全部学生信息(排名不分前后):")
            for i in range(len(info_list)):
                print("第"+str(i+1)+"个:")
                print("学生姓名:"+str(info_list[i][0]))
                print("学生班级:"+str(info_list[i][1]))
                print("学生性别:"+str(info_list[i][2]))
                print("学生语文成绩:"+str(info_list[i][3]))
                print("学生数学成绩:"+str(info_list[i][4]))
                print("学生英语成绩:"+str(info_list[i][5]))
                print("学生总成绩:"+str(info_list[i][6]))
                os.system('pause')
                os.system('cls')
                zcd()
        elif op == 3:
            info_list = find_tb()
            fen = int(input("你要要查询总成绩高于n分的学生, 请输入n:"))
            for i in range(len(info_list)):
                if info_list[i][6] >= fen:
                    print("查询结果:")
                    print("第"+str(i+1)+"个:")
                    print("学生总成绩:"+str(info_list[i][6]))
            os.system('pause')
            os.system('cls')
            zcd()
        elif op == 4:
            os.system('cls')
            break
