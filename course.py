#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import re
import sys
if sys.version_info < (3,2):
    import urllib
else:
    import urllib.request as urllib

if __name__ == "__main__":
    if len(sys.argv) == 1:
        try: input = raw_input
        except NameError: pass
        ans = input("系所代碼: ")
    else:
        ans = sys.argv[1]

    url = "http://course-query.acad.ncku.edu.tw/qry/qry001.php?dept_no=" + ans

    try:
        data = urllib.urlopen(url).read()   # Parse the raw data
    except IOError:
        print("連線錯誤!!!")
        exit()

    if "查無課程資訊" in data:    # maybe the DeptNo. is wrong
        print("查無課程資訊，請檢查課程代號是否正確！")
    else:
        print(type(data))
        content = re.findall("<TD(.+?)</TD>", data)
        """
        for i in range(0, len(content)):
            print i, content[i]
        """
        maxLength = 0
        nameList = []
        remainList = []
        for i in range(0, len(content)):
            if "<a href" in content[i]:     # encounter a mark to locate each course
                thisName = re.findall('.+">(.+?)</a>', content[i+4])[0]
                nameList.append(thisName)
                thisRemain = re.findall('.+>(.+)', content[i+9])[0]
                remainList.append(thisRemain)

                if len(thisName.decode("utf8")) > maxLength:
                    maxLength = len(thisName.decode("utf8"))
        print(maxLength)
        for j in range(0, len(nameList)):   #To print every course in the list
            space = []
            engCharSub = re.findall('[a-zA-Z]', nameList[j])

            for k in range(0, maxLength+2 - len(nameList[j].decode("utf8"))):
                space.append('  ')
            for l in range(0, len(engCharSub)):
                space.append(' ')
            space = "".join(space)

            print(nameList[j].decode("utf8"), space, remainList[j].decode("utf8"))
            print("-----------------------------------------------")
