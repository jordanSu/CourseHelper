#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import re
import sys

if __name__ == "__main__":
    if len(sys.argv) == 1:
        ans = raw_input("系所代碼: ")
    else:
        ans = sys.argv[1]
    url = "http://course-query.acad.ncku.edu.tw/qry/qry001.php?dept_no=" + ans
    data = urllib.urlopen(url).read()
    if "查無課程資訊" in data:
        print "查無課程資訊"
    else:
        courseName = re.findall("<TD><a target='_blank'.+>(.+?)</a></TD>", data)
        
        content = re.findall("<TD(.+?)</TD>", data)
        """
        for i in range(0, len(content)):
            print i, content[i]
        """
        for i in range(0, len(content)):
            if "<a href" in content[i]:
                name = re.findall('.+">(.+?)</a>', content[i+4])[0]
                remain = re.findall('.+>(\w+)', content[i+9].decode('utf8'), re.UNICODE)[0]
                print i, name, "\t\t" ,remain
