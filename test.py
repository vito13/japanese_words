import getopt
import sys

opts,args = getopt.getopt(sys.argv[1:],'-h-f:-v',['help','filename=','version'])
print(opts)
for opt_name,opt_value in opts:
    if opt_name in ('-h','--help'):
        print("[*] Help info")
        sys.exit()
    if opt_name in ('-v','--version'):
        print("[*] Version is 0.01 ")
        sys.exit()
    if opt_name in ('-f','--filename'):#当外部输入'-f1'或者'--flilename=1'时，输出为：[('--filename', '3')] \n [*] Filename is  3
        fileName = opt_value
        print("[*] Filename is ",fileName)
        # do something
        sys.exit()