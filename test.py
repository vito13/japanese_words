import sys
from termcolor import colored, cprint
from colorama import Fore, Back, Style
 
 
def primal_print():
    # 通用格式：033[1;31m + mes + 033[0m
    mes1 = "我是红色"
    print("\033[1;31m" + mes1 + "\033[0m")
 
    mes2 = "我是绿色"
    print("\033[1;32m" + mes2 + "\033[0m")
 
    # 组合的方式:如 下划线 - 红色字体 - 背景黑色
    mes3 = "我是组合的方式"
    print("\033[4;31;40m" + mes3 + "\033[0m")
 
 
def termcolor_demo():
    text = colored('Hello, World!', 'red', attrs=['reverse', 'blink'])
    print(text)
    cprint('Hello, World!', 'green', 'on_red')
 
    print_red_on_cyan = lambda x: cprint(x, 'red', 'on_cyan')
    print_red_on_cyan('Hello, World!')
    print_red_on_cyan('Hello, Universe!')
 
    for i in range(3):
        cprint(str(i), 'magenta', end=' ')
    print()
 
 
def color_demo():
    # 字体颜色
    print(Fore.RED + "甲是红色")
    print(Fore.GREEN + "乙是绿色")
    print(Fore.BLUE + "丙是蓝色")
 
    # 重置设置，还原默认设置
    print(Style.RESET_ALL)
 
    # 字体背景色
    print(Back.RED + "A的背景色为红色")
    print(Back.GREEN + "B的背景色为绿色")
    print(Back.BLUE + "C的背景色为蓝色")
 
    # 重置设置，还原默认设置
    print(Style.RESET_ALL)
 
    # 字体加粗
    print(Style.BRIGHT + "字体加粗")
 
    # 组合
    print(Fore.RED + Back.GREEN + Style.BRIGHT + "绿底红字加粗")
 
    # 重置设置，还原默认设置
    print(Style.RESET_ALL + "普通字体")

if __name__ == '__main__':
    primal_print()
    print("*" * 80)
    termcolor_demo()
    print("*" * 80)
    color_demo()