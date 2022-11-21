
import re
import xlrd
data = xlrd.open_workbook('dajiaxue/dajiaxue.xlsx')


for sheetname in data.sheet_names():
    table = data.sheet_by_name(sheetname)
    # 获取表格行数
    nrows = table.nrows
    print("表格",sheetname,"一共有",nrows,"行")

    for r in range(1, nrows):
        tone, *rowvalue = table.row_values(r)
        if type(tone) == float:
            tone = str(int(tone))
        print(tone, rowvalue)
