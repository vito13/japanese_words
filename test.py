from threading import Thread,Event
import time

event=Event()

def light():
    print('红灯正亮着')
    time.sleep(3)
    event.set() #绿灯亮

def car(name):
    print('车%s正在等绿灯' %name)
    event.wait() #等灯绿 此时event为False,直到event.set()将其值设置为True,才会继续运行.
    print('车%s通行' %name)

if __name__ == '__main__':
    # 红绿灯
    t1=Thread(target=light)
    t1.start()
    # 车
    for i in range(10):
        t=Thread(target=car,args=(i,))
        t.start()
