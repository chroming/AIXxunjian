# -*- coding:utf-8 -*-

import re
import os

#获取目录下文件夹列表
dirlist = os.listdir('/tmp/log')
#初始化i
i=0

#主运行函数
def main(i):
    #根据i依次获取文件

    logfile = dirlist[i]
    raw_input("获取目录%s信息，按Enter显示结果"%logfile)
    #print logfile
    prtconf = open('/tmp/log/%s/hardware/prtconf.log'%logfile,'r')
    prtconft = prtconf.read()
    prtconf.close()

    rootdisksize = open('/tmp/log/%s/hardware/rootdisksize.txt'%s,'r')
    rootdisksizet = rootdisksize.read()
    rootdisksize.close()

    lscfg = open('/tmp/log/%s/hardware/lscfg.vp.log'%logfile,'r')
    lscfgt = lscfg.read()
    lscfg.close()
    
    errpt = open('/tmp/log/%s/errpt/errpt/errpt.log'%s,'r')
    errptt = errpt.read()
    errpt.close()

    df = open('/tmp/log/%s/softwareutil/df.log'%s,'r')
    dft = df.read()
    df.close()

    lsps = open('/tmp/log/%s/performance/lsps.txt'%s,'r')
    lspst = df.read()
    lsps.close()

    rootvg = open('/tmp/log/%s/lvm/vg/lsvg.rootvg'%s,'r')
    rootvgt = rootvg.read()
    rootvg.close()

    rootvgl = open('/tmp/log/%s/lvm/vg/lsvg.rootvg.l'%s,'r'0)

    #获取proconf中信息
    get_machine_id = re.findall(r'Machine Serial Number\:\ (\w{5,10})',prtconft)[0]
    get_model = re.findall(r'Model\: *IBM\,(\d\S*)',prtconft)[0]
    get_type = re.findall(r'Processor Type\: (\S*)',prtconft)[0]
    get_memory = re.findall(r'Memory Size\: (\d* \w*)',prtconft)[0]
    get_fireware = re.findall(r'Firmware Version\: (\S*)',prtconft)[0]
    get_hostname = re.findall(r'Host Name\: (\S*)',prtconft)[0]
    get_ip = re.findall(r'IP Address\: ((?:\d{1,3}\.){3}\d{1,3})',prtconft)[0]
    print get_machine_id
    print get_model
    print get_type
    print get_memory
    print get_fireware
    print get_hostname
    print get_ip



    if i < 2:
        i=i+1   
        main(i)
    else:
        raw_input("程序运行结束！按Enter退出")
        exit()

main(i)
