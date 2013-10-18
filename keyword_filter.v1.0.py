#/*******************************************************************************
# * Author	 : jingbo.li | work at r
# * Email	 : ljb90@live.cn
# * Last modified : 2013-10-18 18:20
# * Filename	 : keyword_filter.v1.0.py
# * Description	 :  
#                   Capture information 
# * *****************************************************************************/
#!/usr/bin/python2
# -#- coding: UTF-8 -*-


import os
import sys

def main(*argv):
    if len(argv[0]) <= 1:
        print 'please input the argv!'
    else:
        try:
            fp = open(argv[0][1],'rb')
        except:
            print "read the file is error"
            return
        date_list = []
        date = fp.readline().strip('\n')
        org_info = runcommand(argv[0][2])#dmidecode -t processor'
        if not org_info:
            print 'the command is error'
            return
        while date:
            date_list.append(date)
            date = fp.readline().strip('\n')

        for kw in date_list:
            for orgs in org_info:
                if orgs.rfind(kw) != -1:
                    print orgs.strip()

def runcommand(cmd):
    try:
        temp = os.popen(cmd).readlines()
        return temp
    except:
        print 'cmd error'
        return None

if __name__ == "__main__":
    main(sys.argv)
