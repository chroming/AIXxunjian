# -*- coding:gbk -*-

import re
import os
import xlwt

print('----------------------------------------------------------------------------')
print('本程序用于备件整理，版本V1.0，作者sikx@dcits.com')
print('请将程序与日志文件放在同一文件夹下')
print('----------------------------------------------------------------------------')
raw_input('按Enter开始 ')
fi = 0
file = xlwt.Workbook(encoding = 'gbk')
table = file.add_sheet('sheet1')

#get hdisk infomation and write to xls
def get_hdisk(x,y,lscfgt,get_model):
    get_hdisk_name = re.findall(r'hdisk\d *(\w{5}\.\d{3}\.\w*\-(?:\w{2,3}\-){1,4}\w{1,3}\s) *(\S[ \S]*\S).*?Part Number[ \.]*(\w*)',lscfgt,re.S)

    for hdisk in get_hdisk_name:

        hdisk_location = hdisk[0]
        hdisk_describe = hdisk[1].decode('utf-8')
        hdisk_pn = hdisk[2]

        table.write(x,y,get_model)
        y += 1
        table.write(x,y,'硬盘')
        y += 1
        table.write(x,y,hdisk_pn)
        y += 1
        table.write(x,y,hdisk_describe)
        #y += 1
        #table.write(x,y,hdisk_location)
        x += 1
        y=0
        file.save('beijian.xls')
    return x,y

#get other infomation
def get_detail(spe):
    get_name = re.findall(r'(\w[ \S]*\w) *\:\s*Record Name',spe)[0]
    #if its memory then get size
    try:
        get_size = re.findall(r'Size[ \.]*(\d*)',spe)[0]
        get_describe = get_name+"-"+get_size+"MB"
    except:
        get_describe = get_name
    try:
        get_pn = re.findall(r'Part Number\.*(\w*)',spe)[0]
    #check if there is PN and FRU
    except:
        try:

            get_fru = re.findall(r'FRU[ \w]*\.* *(\w*)',spe)[0]
            get_pn = get_fru
        except:
            get_pn = 000000000000
    get_Location = re.findall(r'Physical Location\: (\S*)',spe)[0]
    return(get_describe,get_pn,get_Location)

#get classic by describe
def get_class(describe):
    if re.search(r'Memory', describe):
        return '内存'
    elif re.search(r'Air Mover', describe):
        return '风扇'
    elif re.search(r'AC PS', describe):
        return '电源'
    elif re.search(r'\d\-WAY', describe):
        return 'CPU'

#write to excel
def get_info(x,y,lscfgt):
    get_model = re.findall(r'Model\: *IBM\,(\d\S*)',lscfgt)[0]
    get_spe_list = re.findall(r'([ \S]*\:\s*Record Name.*?Physical Location\:[ \S]*)',lscfgt,re.S)

    for spe in get_spe_list:
        detail = get_detail(spe)
        describe = detail[0]
        pn = detail[1]
        location = detail[2]
        theclass = get_class(describe)

        if pn != 0 and theclass:
            table.write(x,y,get_model)
            y += 1
            table.write(x, y, theclass)
            y += 1
            table.write(x,y,pn)
            y += 1
            table.write(x,y,describe)
            #y += 1
            #table.write(x,y,location)
            x += 1
            y=0
            file.save('beijian.xls')
    return x,y,get_model

#get all file
def onebyone():
    global fi
    x=y=0
    filelist = os.listdir(os.getcwd())
    for fileone in filelist:
        if fileone[0] != '.':
            filelog = open('%s'%fileone)
            file = filelog.read()
            filelog.close()
            if re.findall(r'Model\: *IBM\,(\d\S*)',file) != []:
                print('开始获取%s信息'%fileone)            
                x,y,get_model = get_info(x,y,file)
                x,y = get_hdisk(x,y,file,get_model)
                fi += 1


onebyone()
raw_input('共获取日志%s ，备件信息保存在同文件夹下的beijia.xls中。按Enter退出'%fi)


