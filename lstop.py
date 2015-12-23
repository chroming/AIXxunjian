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


def logopen(logfile, name):
    try:
        log = open('/Users/chroming/logtmp/log/%s/%s' % (logfile, name), 'r')
        logr = log.read()
        log.close()
        return logr
    except:
        return ''


def check_func(zz, logt):
    #get_data = re.findall(r'%s' % zz, logt)
    try:
        get_data = re.findall(r'%s' % zz, logt)
        get_data[0]
        return get_data
    except:
        return ['']


#读取文件
def maincheck(logfile):
    prtconf = logopen(logfile, 'hardware/prtconf.log')
    errpt = logopen(logfile, 'errpt/errpt.log')
    lsps = logopen(logfile, 'performance/lsps.txt')
    sar = logopen(logfile, 'performance/sar.txt')
    ip = logopen(logfile, 'hardware/ipaddr.txt')
    serialnumber = logopen(logfile, 'hardware/serialnumber.txt')
    rootvgmirror = logopen(logfile, 'software/rootvg_mirror.txt')
    df = logopen(logfile, 'softwareutil/df.log')
    iostat = logopen(logfile, 'performance/iostat.log')
    vmstat = logopen(logfile, 'performance/vmstat.log')
    mem = logopen(logfile, 'hardware/nummem.txt')
    ping = logopen(logfile, 'network/ping.log')
    sysdump = logopen(logfile, 'softwareutil/sysdumpdev.log')
    ps = logopen(logfile, 'softwareutil/ps.log')
    try:
        lvlist = os.listdir('/Users/chroming/logtmp/log/%s/lvm/lv/'%logfile)
    except:
        lvlist = []
    lenlv = len(lvlist)
    leni = 0
    for lvs in lvlist:
        if re.match(r'lslv\.\w*\.m', lvs):
            pass
        else:
            try:
                lvopen = logopen(logfile, 'lvm/lv/%s'%lvs)
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
    print('=============================================================')
    print('序列号: %s'%serialnumber)
    print('-------------------------------------------------------------')
    print('主机名为: %s'%get_hostname)
    print('IP地址为: %s'%ip)

    #errpt
    get_errpt = check_func('\w{8} *(\d{10}) (\w) (\w)(.*?)', errpt)
    i = j = 0

    try:
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
    except:
        print('报错信息获取失败!')

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
    try:
        freemem = float(check_func('\d+ +\d+ +\d+ +(\d+)', vmstat)[0])
        memory = 100*(1 - (freemem/(98304*256)))
        print('内存利用率: %.2f%%'%memory)
    except:
        print('内存利用率获取失败')
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
    print('=============================================================')


    #判断是否是手动输入模式,如果是
    if cnum == str(1):
        choicenum = raw_input('输入1继续选择其他目录,输入其他退出,请输入代码: ')
        if choicenum == str(1):
            logfile = inputdir()
            maincheck(logfile)


def onebyone():
    filelist = os.listdir('/Users/chroming/logtmp/log/')
    for fileone in filelist:
        if os.path.isdir('/Users/chroming/logtmp/log/%s'%fileone):
            raw_input('按Enter显示目录%s内容'%fileone)
            maincheck(fileone)


def Main():
    if cnum == str(1):
        logfile = inputdir()
        return logfile
    else:
        logfile = onebyone()
        return logfile


cnum = raw_input("请输入需要使用的模式,1为手动输入日志目录,其他为自动获取目录下所有日志目录: ")
logfile = Main()
maincheck(logfile)
