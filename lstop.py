# -*- coding: utf-8 -*-

import re
import os

logfile = raw_input("请输入同目录下的日志包文件夹名： ")


def logopen(name):
    log = open('/Users/chroming/logtmp/log/%s/%s' % (logfile, name), 'r')
    logr = log.read()
    log.close()
    return logr


prtconf = logopen('hardware/prtconf.log')
errpt = logopen('errpt/errpt.log')
lsps = logopen('performance/lsps.txt')
# cluster = logopen('%s/software/')
sar = logopen('performance/sar.log')
ip = logopen('hardware/ipaddr.txt')
serialnumber = logopen('hardware/serialnumber.txt')
rootvgmirror = logopen('software/rootvg_mirror.txt')
df = logopen('softwareutil/df.log')


def check_func(zz, logt):
    get_data = re.findall(r'%s' % zz, logt, re.S)
    try:
        get_data[0]
        return get_data
    except:
        return '获取失败！'


# 获取所需信息

# get_machine_id = check_func('Machine Serial Number\:\ (\w{5,10})',prtconf)[0]
get_hostname = check_func('Host Name: (\S*)', prtconf)[0]

try:
    get_df = check_func('9\d\%', df)
    print('文件系统超过90%目录: %s' % get_df)
except:
    print('文件系统剩余空间正常')