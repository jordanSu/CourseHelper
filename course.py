#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import re
import sys
if sys.version_info < (3,2):
    import urllib
    isPython3 = False
else:
    import urllib.request as urllib
    isPython3 = True

if __name__ == "__main__":
    if len(sys.argv) == 1:
        if isPython3 is not True:
            input = raw_input
        ans = input("系所代碼: ")
    else:
        ans = sys.argv[1]   # get the argument from command line

    url = "http://course-query.acad.ncku.edu.tw/qry/qry001.php?dept_no=" + ans

    try:
        data = urllib.urlopen(url).read()   # Parse the raw data
        if isPython3 is True:
            data = data.decode()    # 'bytes' -> u'str'
    except IOError:
        print("連線錯誤!!!")
        exit()

    if "查無課程資訊" in data:    # maybe the DeptNo. is wrong
        print("查無課程資訊，請檢查課程代號是否正確！")
    else:
        content = re.findall("<TD(.+?)</TD>", data)

        #for info in content:
        #    print(info)
        maxLength = 0
        nameList = []
        deptList = []
        noList = []
        remainList = []
        for i in range(0, len(content)):
            if "<a href" in content[i]:     # encounter a mark to locate each course
                # parse the course name and put it into list
                thisName = re.findall('.+">(.+?)</a>', content[i+4])[0]
                nameList.append(thisName)

                # parse the course No and put it into list
                if i-5 > 0:
                    try:
                        thisDept = re.findall('.+>(.+)', content[i-5])[0]
                        thisNo = re.findall('.+>(\d+)', content[i-4])[0]
                    except IndexError:
                        thisDept = "  "
                        thisNo = "   "
                    deptList.append(thisDept)
                    noList.append(thisNo)

                # parse the course remain and put it into list
                thisRemain = re.findall('.+>(.+)', content[i+9])[0]
                remainList.append(thisRemain)

                # To find the maxLength
                if isPython3 is True:
                    if len(thisName) > maxLength:
                        maxLength = len(thisName)
                else:
                    if len(thisName.decode("utf8")) > maxLength:
                        maxLength = len(thisName.decode("utf8"))

        for j in range(0, len(nameList)):   #To print every course in the list
            space = []  # add space to make pretty column print

            # searching for english character since it's width is 1
            engCharSub = re.findall('[a-zA-Z]', nameList[j])

            for l in range(0, len(engCharSub)):
                space.append(' ')

            if isPython3 is True:
                for k in range(0, maxLength+2 - len(nameList[j])):
                    space.append('  ')
                space = "".join(space)
                print(deptList[j], noList[j], nameList[j], space, remainList[j])
            else:
                for k in range(0, maxLength+2 - len(nameList[j].decode("utf8"))):
                    space.append('  ')
                space = "".join(space)
                print(deptList[j], noList[j], nameList[j].decode("utf8"), space, remainList[j].decode("utf8"))

            print("-----------------------------------------------")
