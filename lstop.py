# -*- coding: utf-8 -*-

import re
import os

logfile = raw_input("请输入同目录下的日志包文件夹名： ")


def logopen(name):
    log = open('/Users/chroming/logtmp/log/%s/%s' % (logfile, name), 'r')
    logr = log.read()
    log.close()
    return logr

def check_func(zz, logt):
    get_data = re.findall(r'%s' % zz, logt)
    try:
        get_data[0]
        return get_data
    except:
        return '获取失败！'

prtconf = logopen('hardware/prtconf.log')
errpt = logopen('errpt/errpt.log')
lsps = logopen('performance/lsps.txt')
# cluster = logopen('%s/software/')
sar = logopen('performance/sar.txt')
ip = logopen('hardware/ipaddr.txt')
serialnumber = logopen('hardware/serialnumber.txt')
rootvgmirror = logopen('software/rootvg_mirror.txt')
df = logopen('softwareutil/df.log')
iostat = logopen('performance/iostat.log')
vmstat = logopen('performance/vmstat.log')
mem = logopen('hardware/nummem.txt')

lvlist = os.listdir('/Users/chroming/logtmp/log/%s/lvm/lv/'%logfile)
lenlv = len(lvlist)
leni = 0
for lvs in lvlist:
    if re.match(r'lslv\.\w*\.m', lvs):
        pass
    else:
        try:
            lvopen = logopen('lvm/lv/%s'%lvs)
            stale = re.findall(r'LV STATE: +\w+\/stale', lvopen)
            stale[0]
            if stale != []:
                leni += 1
        except:
            pass

if int(leni) == 0:
    stalelv = '正常'
else:
    stalelv = '异常'


# 获取所需信息
get_hostname = check_func('Host Name: (\S*)', prtconf)[0]
print('序列号: %s'%serialnumber)
print('-------------------------------------------------------------')
print('主机名为: %s'%get_hostname)
print('IP地址为: %s'%ip)

#errpt
get_errpt = re.findall(r'\w{8} *(\d{10}) (\w) (\w)(.*?)', errpt)
i = j = 0
if get_errpt == []:
    print('系统无报错!')
else:
    for errptsingle in get_errpt:
        i += 1
        if (errptsingle[2] == 'P') & (errptsingle[3] == 'H'):
            j += 1
if i > 0:
    if j > 0:
        print('系统有%s条报错,其中有%s条硬件报错.最近一条报错时间为%s月%s日'%(i, j, get_errpt[0][0][0:1], get_errpt[0][0][2:3]))
    else:
        print('系统有%s条报错,无硬件报错.最近一条报错时间为%s月%s日'%(i, get_errpt[0][0][0:2], get_errpt[0][0][2:4]))
else:
    print('系统无报错!')

rootmirror = check_func('\w{2,3}', rootvgmirror)[0]
print('操作系统是否做镜像: %s'%rootmirror)
print('有stale状态的逻辑卷存在: %s'%stalelv)

try:
    get_df = check_func('9\d\%', df)
    print('文件系统超过90%目录: %s' % get_df)
except:
    print('文件系统剩余空间正常')
print(' ')
CPU = check_func('\d{1,2}', sar)[0]
print('CPU利用率: %s%%'%CPU)

try:
    ios = check_func('tty: *tin *tout *avg-cpu: *\% *user *\% *sys *\% *idle *\% *iowait\s*(?:\d{1,2}\.\d{1,2} *){4}(\d{1,2}\.\d{1,2})',iostat)
    get_io = 100 - float(ios[0])
    print ('I/O分布: %s%%'%get_io)
except:
    print('I/O分布获取失败!')
freemem = float(check_func('\d+ +\d+ +\d+ +(\d+)', vmstat)[0])
memory = 100*(1 - (freemem/(98304*256)))
print('内存利用率: %.2f%%'%memory)
print('交换区使用率: %s'%lsps)

