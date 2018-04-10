#!usr/bin/python
# _*_ coding:utf-8 _*_
# author: Robinn
# 功能: 从报表验证代理IP生成有效IP池


import os
import re
import sys
import xlwt
import xlrd
import requests
import telnetlib
import urllib2


#使用telnetlib包验证代理IP
def getip_telnet(sourceExl):
    proxyiplist = []
    data = xlrd.open_workbook(sourceExl)
    table = data.sheets()[0]
    nrows = table.nrows #行数
    ncols = table.ncols #列数
    for i in xrange(0,nrows):
        print(i)
        iplist = []
        if i>=1:
            rowValues= table.row_values(i) #某一行数据
            iplist.append(rowValues[1])
            iplist.append(rowValues[2])
            iplist.append(rowValues[3])
            iplist.append(rowValues[4])
            iplist.append(rowValues[5])
            # for item in rowValues:
            #     print item
            try:
                telnetlib.Telnet(host=rowValues[1], port=rowValues[2], timeout=20)
            except:
                continue
            else:
                proxyiplist.append(iplist)
    return proxyiplist


#使用requests包验证代理IP
def getip(sourceExl):
    proxyiplist = []
    data = xlrd.open_workbook(sourceExl)
    table = data.sheets()[0]
    nrows = table.nrows #行数
    ncols = table.ncols #列数
    for i in xrange(0,nrows):
        print(i)
        iplist = []
        if i>=1:
            rowValues= table.row_values(i) #某一行数据
            iplist.append(rowValues[1])
            iplist.append(rowValues[2])
            iplist.append(rowValues[3])
            iplist.append(rowValues[4])
            iplist.append(rowValues[5])
            # for item in rowValues:
            #     print item
            try:
                content = requests.get('http://ip.chinaz.com/getip.aspx', proxies={"http":"http://"+rowValues[1]+":"+rowValues[2]})
                ip = content.text.split("',")[0].split(":'")
                if ip[1] == rowValues[1]:
                    proxyiplist.append(iplist)
                    print rowValues[1]+":"+rowValues[2]+' requests success!'
                else:
                    continue
            except:
                continue

    return proxyiplist

#使用urllib2包验证代理IP
def getip_urllib(sourceExl):
    proxyiplist = []
    data = xlrd.open_workbook(sourceExl)
    table = data.sheets()[0]
    nrows = table.nrows #行数
    ncols = table.ncols #列数
    for i in xrange(0,nrows):
        print(i)
        iplist = []
        if i>=1:
            rowValues= table.row_values(i) #某一行数据
            iplist.append(rowValues[1])
            iplist.append(rowValues[2])
            iplist.append(rowValues[3])
            iplist.append(rowValues[4])
            iplist.append(rowValues[5])
            # for item in rowValues:
            #     print item
            regex = re.compile(r'baidu.com')
            server = 'http://'+ rowValues[1] + ':'+ rowValues[2]
            opener = urllib2.build_opener(urllib2.ProxyHandler({'http':server}))
            urllib2.install_opener(opener)
            try:
                response = urllib2.urlopen("http://www.baidu.com", timeout=5)
            except:
                continue
            else:
                try:
                    str = response.read()
                except:
                    continue
                if regex.search(str):
                    proxyiplist.append(iplist)
                    print rowValues[1] + ':' + rowValues[2]
    return proxyiplist


#保存有效代理ip
def saveip(iplist,targetExl):
    #获取代理IP池所有结果
    results = iplist

    #设置Excel表头
    fields = [u"代理IP地址",u"端口",u"服务器地址",u"是否匿名",u"类型"]

    #将表头字段写入到EXCEL新表的第一行
    wbk = xlwt.Workbook()
    sheet = wbk.add_sheet('ippool',cell_overwrite_ok=True)
    for ifs in range(0,len(fields)):
        field = fields[ifs]
        sheet.write(0,ifs,field)
        _col = sheet.col(ifs)
        _col.width = 306*(int(ifs)+10)
    ics=1
    jcs=0
    for ics in range(1,len(results)+1):
        for jcs in range(0,len(fields)):
            sheet.write(ics, jcs, results[ics-1][jcs])

    type = sys.getfilesystemencoding()
    print(u"有效代理IP池已经生成完毕,数据表正在打开,请稍等............")
    wbk.save(targetExl)
    print(u"有效代理IP池数据表已经打开.数据文件保存在当前程序目录中,请查看程序所在目录...")
    os.system(targetExl)


if __name__ == "__main__":
    sourceExl = "proxyip.xls"
    targetExl = "target_ip.xls"
    proxyiplist = getip(sourceExl)
    saveip(proxyiplist,targetExl)