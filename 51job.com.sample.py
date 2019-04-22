# _author:'DJS'
# date:2018-11-19
# 前程无忧爬虫实战（通过输入关键字爬取任意职位并自动保存为.csv文本）

import csv
import re
import time

import requests
from lxml import etree

headers = {
    "cache-control": "no-cache",
    "postman-token": "72a56deb-825e-3ac3-dd61-4f77c4cbb4d8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36",

}


def get_url(key1):
    try:
        i = 0
        url = "https://search.51job.com/list/030800%252C040000%252C030200,000000,0000,00,9,99,{},2,1.html"
        response = requests.get(url.format(key1), headers=headers)
        html = etree.HTML(response.content.decode('gbk'))
        max_page = int("".join(re.findall('(\d+)', "".join(html.xpath("//span[@class='td']/text()")))))
        while True:
            i += 1
            url = "https://search.51job.com/list/030800%252C040000%252C030200,000000,0000,00,9,99,{},2,{}.html"
            url = url.format(key1, i)
            print("*" * 100)
            print("on page正在爬取第%d页" % i)
            print("*" * 100)
            yield url
            # print("正在爬取%d页"%i)
            if max_page == i:
                break
    except:
        print("获取不到链接，已处理")


def pase_page(key1):
    try:
        for i in get_url(key1):
            url = i
            # print(url)
            response = requests.get(url, headers=headers)
            html = etree.HTML(response.content.decode('gbk'))  # 解码成gbk后输出，请求的是gbk，但是python默认的是
            # 输出的是utf-8，所以把utf-8解码成gbk就可以输出了，这样请求和输出就一样了,decode 相当于输出
            # 编码的输入和输出要一致。
            lists = html.xpath("//div[@id='resultList']//div[@class='el']")
            for list in lists:
                item = {}
                item["职位"] = "".join(list.xpath("./p/span/a/text()")).replace('\r\n', '').replace(' ', '')
                item["公司名称"] = "".join(list.xpath("./span[@class='t2']/a/text()")).replace('\r\n', '').replace(' ', '')
                item["工作地点"] = "".join(list.xpath("./span[@class='t3']/text()")).replace('\r\n', '').replace(' ', '')
                item["薪资"] = "".join(list.xpath("./span[@class='t4']/text()")).replace('\r\n', '').replace(' ', '')
                item["发布时间"] = "".join(list.xpath("./span[@class='t5']/text()")).replace('\r\n', '').replace(' ', '')
                item["爬网时间"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                yield item
    except:
        print("返回数据异常，已处理")


def save_excel(key1):
    try:
        header = ['职位', '公司名称', '工作地点', '薪资', '发布时间', '爬网时间']
        with open(key1 + 'jobinfo.csv', 'w', newline='') as f:  # w是写入
            # 标头在这里传入，作为第一行数据
            writer = csv.DictWriter(f, header)
            writer.writeheader()
        for i in pase_page(key1):
            item = i
            header = ['职位', '公司名称', '工作地点', '薪资', '发布时间', '爬网时间']
            with open(key1 + 'jobinfo.csv', 'a', newline='') as f:  # a是追加
                writer = csv.DictWriter(f, header)
                writer.writerow(item)
                # print(item)
    except:
        print("保存数据异常，已处理")


if __name__ == '__main__':
    key1 = input('请输入要爬取的职位Jobtitel：')
    save_excel(key1)
