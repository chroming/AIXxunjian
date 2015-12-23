# -*- coding: utf-8 -*-

import re
import os

#输入判断
def inputdir():
    logfile = raw_input("请输入同目录下的日志包文件夹名： ")
    if logfile and os.path.exists('/Users/chroming/logtmp/log/%s'%logfile):
        return logfile
    else:
        print('目录不存在!请检查后重新输入!')
        return inputdir()

logfile = inputdir()


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


#读取文件
prtconf = logopen('hardware/prtconf.log')
errpt = logopen('errpt/errpt.log')
lsps = logopen('performance/lsps.txt')
sar = logopen('performance/sar.txt')
ip = logopen('hardware/ipaddr.txt')
serialnumber = logopen('hardware/serialnumber.txt')
rootvgmirror = logopen('software/rootvg_mirror.txt')
df = logopen('softwareutil/df.log')
iostat = logopen('performance/iostat.log')
vmstat = logopen('performance/vmstat.log')
mem = logopen('hardware/nummem.txt')
ping = logopen('network/ping.log')
sysdump = logopen('softwareutil/sysdumpdev.log')
ps = logopen('softwareutil/ps.log')
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
print('系统mail给root的错误报告: 正常')
rootmirror = check_func('\w{2,3}', rootvgmirror)[0]
print('操作系统镜像: %s'%rootmirror)
print('有stale状态的逻辑卷存在: %s'%stalelv)

try:
    get_df = check_func('9\d\%', df)
    print('文件系统超过90%目录: %s' % get_df)
except:
    print('文件系统剩余空间: 正常')

pingtime = check_func('time=\d+', ping)
sysdumpdev = re.search(r'primary +\/dev\/sysdumpnull', sysdump)
if sysdumpdev:
    print('系统DUMP设置是否正确: 异常')
else:
    print('系统DUMP设置是否正确: 正常')

try:
    pingtime[0]
    print('IP、路由及网络连通: 正常')
except:
    print('IP、路由及网络连通: 异常')

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

clcomd = re.search(r'cluster\/clcomd', ps)
clstrmgr = re.search(r'cluster\/clstrmgr', ps)
clinfo = re.search(r'cluster\/clinfo', ps)
if clcomd and clstrmgr:
    print('检查HACMP的进程是否存在: 正常')
else:
    print('检查HACMP的进程是否存在: N/A')

if clinfo:
    print('检查监控资源是否有问题: 正常')
else:
    print('检查监控资源是否有问题: N/A')