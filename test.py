# import re
# from jamdict import Jamdict
# jam = Jamdict()
# result = jam.lookup('じゅういち')

# # print all word entries
# for entry in result.entries:
#      print(entry)


import threading
from concurrent.futures import ThreadPoolExecutor

#账户类
class Account:
    def __init__(self, account_no, balance):
        #账户编号和账户余额
        self.account_no = account_no
        self.balance = balance

        self._flag = False
        self.cond = threading.Condition()
    
    def getBlance(self):
        return self.balance
    
    #提取现金方法
    def draw(self, draw_amount):
        with self.cond:
            if not self._flag:
                self.cond.wait()
            else:
                if self.balance >= draw_amount:
                    print(threading.current_thread().name+'	取钱成功!吐出钞票:'+str(draw_amount))
                    self.balance -= draw_amount
                    print(threading.current_thread().name+'操作之后	余额为:'+str(self.balance))
                else:
                    print(threading.current_thread().name+'	取钱失败!余额不足!	当前余额为:'+str(self.balance))
                self._flag = False
                self.cond.notify_all()

    #存钱方法
    def deposit(self, deposit_amount):
        with self.cond:
            if  self._flag:
                self.cond.wait()
            else:
                print(threading.current_thread().name+'	存钱成功!存入钞票:'+str(deposit_amount))
                self.balance += deposit_amount
                print(threading.current_thread().name+'操作之后	余额为:'+str(self.balance))
                self._flag = True
                self.cond.notify_all()

acct = Account('986623', 1000)

with ThreadPoolExecutor(100, thread_name_prefix='Account_Thread_Pool') as pools:
    for i in range(50):
        pools.submit(acct.deposit, 1000)
        pools.submit(acct.draw, 900)