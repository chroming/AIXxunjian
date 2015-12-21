# -*- coding:utf-8 -*-

import re
import os

logfile = raw_input("请输入同目录下的日志包文件夹名： ")

#读取文件夹下需要的文件
def logopen(name):
    log = open('/logtmp/log/%s'%name,'r')
    logr = log.read()
    log.close
    return logr

prtconf = logopen('%s/hardware/prtconf.log')
errpt = logopen('%s/errpt/errpt.log')
lsps = logopen('%s/performance/lsps.txt')
#cluster = logopen('%s/software/')
sar = logopen('%s/performance/sar.log')
ip = logopen('%s/hardware/ipaddr.txt')
serialnumber = logopen('%s/hardware/serialnumber.txt')
rootvgmirror = logopen('%s/software/rootvg_mirror.txt')
df = logopen('%s/softwareutil/df.log')
def check_func(zz,logt):
    get_data = re.findall(r'%s'%zz,logt,re.S)
    try:
        get_data[0]
        return get_data
    except:
        return ('获取失败！')

#获取所需信息

#get_machine_id = check_func('Machine Serial Number\:\ (\w{5,10})',prtconf)[0]
get_hostname = check_func('Host Name: (\S*)',prtconf)[0]

get_df = check_func('9\d\%')
print(for df9 in get_df)
