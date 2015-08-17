# -*- coding:utf-8 -*-

#本程序用于自动获取/tmp/log目录下的所有log包中的各项数据并写入同目录下的xunjian.xls做备件储备。
#获取数据为机器SN号，机器型号，各部件PN号、位置、描述。
#作者sikx@dcits.com
#p5 p6测试正常使用

import re
import os
import xlwt

#EXCEL新建
file = xlwt.Workbook()
table = file.add_sheet('sikx')
x = 0
y = 0

#获取目录下文件夹列表
dirlist = os.listdir('/tmp/log')
#初始化i
i=1

#读取两个日志文件
#logfile = raw_input("请输入同目录下的日志包文件夹名： ")

#主运行函数
def main(i,x,y):
    #根据i依次获取文件

    logfile = dirlist[i]
    print logfile
    prtconf = open('/tmp/log/%s/hardware/prtconf.log'%logfile,'r')
    prtconft = prtconf.read()
    prtconf.close()

    lscfg = open('/tmp/log/%s/hardware/lscfg.vp.log'%logfile,'r')
    lscfgt = lscfg.read()
    lscfg.close()


    #获取机器序列号和型号
    get_machine_id = re.findall(r'Machine Serial Number\:\ (\w{5,10})',prtconft,re.S)[0]
    get_model = re.findall(r'Model\: *IBM\,(\d\S*)',lscfgt)[0]
    print get_machine_id
    print get_model



    #获取硬盘信息并写入EXCEl
    def get_hdisk(lscfgt):
        get_hdisk_name = re.findall(r'hdisk\d *(\w{5}\.\d{3}\.\w*\-(?:\w{2,3}\-){1,4}\w{1,3}\s) *(\S[ \S]*\S).*?Part Number[ \.]*(\w*)',lscfgt,re.S)

        return get_hdisk_name

    hdisk_detail = get_hdisk(lscfgt)
    #print hdisk_detail
    for hdisk in hdisk_detail:

        hdisk_location = hdisk[0]
        hdisk_describe = hdisk[1]
        hdisk_pn = hdisk[2]

        table.write(x,y,get_model)
        y=y+1
        table.write(x,y,hdisk_pn)
        y=y+1
        table.write(x,y,hdisk_describe)
        y=y+1
        table.write(x,y,hdisk_location)
        x=x+1
        y=0
        file.save('/tmp/log/xunjian.xls')


    #获取所有PLATFORM SPECIFIC设备名称，序列号，位置函数
    def get_detail(spe):
        
        get_name = re.findall(r'(\w[ \S]*\w) *\:\s*Record Name',spe)[0]
        #如果是内存有Size值先尝试获取Size
        try:
            get_size = re.findall(r'Size[ \.]*(\d*)',spe)[0]
            get_describe = get_name+"-"+get_size+"MB"
        except:
            get_describe = get_name
        try:
            get_pn = re.findall(r'Part Number\.*(\w*)',spe)[0]
        #确认是否有PN和FRU
        except:
            try:

                get_fru = re.findall(r'FRU[ \w]*\.* *(\w*)',spe)[0]
                get_pn = get_fru
            except:
                get_pn = 000000000000
        get_Location = re.findall(r'Physical Location\: (\S*)',spe)[0]
        return(get_describe,get_pn,get_Location)

    get_spe_list = re.findall(r'([ \S]*\:\s*Record Name.*?Physical Location\:[ \S]*)',lscfgt,re.S)


    #调用函数并写入EXCEL
    for spe in get_spe_list:
        detail = get_detail(spe)
        describe = detail[0]
        pn = detail[1]
        location = detail[2]

        table.write(x,y,get_model)
        y=y+1
        table.write(x,y,pn)
        y=y+1
        table.write(x,y,describe)
        y=y+1
        table.write(x,y,location)
        x=x+1
        y=0
        file.save('/tmp/log/xunjian.xls')

    
    if i < 6:
        i=i+1   
        main(i,x,y)
    else:
        exit()

main(i,x,y)

