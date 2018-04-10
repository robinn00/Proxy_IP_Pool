#!usr/bin/python
# _*_ coding:utf-8 _*_
# author: Robinn


str = "{ip:'222.210.102.162',address:'四川省成都市 电信'}"
ip = str.split("',")[0].split(":'")
print(ip[1])



#使用telnetlib包验证代理IP
import telnetlib
try:
    telnetlib.Telnet(host="58.19.15.44",port="18118",timeout=20)
except:
    print("telnetlib failed!")
else:
    print("telnetlib success!")


#使用requests包验证代理IP
import requests
try:
    cnt = requests.get('http://ip.chinaz.com/getip.aspx', proxies={"http":"http://58.19.15.44:18118"})
    print(cnt.text)
except:
    print 'requests failed!'
else:
    print 'requests success!'


#使用urllib2包验证代理IP
import urllib2
import re
class TestProxy(object):
    def __init__(self,ip,port):
        self.ip = ip
        self.port = port
        self.url = 'http://www.baidu.com'
        self.timeout = 3
        self.regex = re.compile(r'baidu.com')
        self.run()

    def run(self):
        self.linkWithProxy()

    def linkWithProxy(self):
        server = 'http://'+ self.ip + ':'+ self.port

        opener = urllib2.build_opener(urllib2.ProxyHandler({'http':server}))
        urllib2.install_opener(opener)
        try:
            response = urllib2.urlopen(self.url, timeout=self.timeout)
        except:
            print '%s connect failed' % server
            return
        else:
            try:
                str = response.read()

            except:
                print '%s connect failed' % server
                return
            if self.regex.search(str):
                print '%s connect success .......' % server
                print self.ip + ':' + self.port


if __name__ == '__main__':
    Tp = TestProxy(ip="58.19.15.44",port="18118")