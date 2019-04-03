#!/user/bin/env python3
# -*- coding: utf-8 -*-

import requests
from lxml import etree
import chardet
import csv
import sys
# 设置递归深度，python的递归深度为999
sys.setrecursionlimit(100000)
# 获取源码
def get_html(url):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}
    response = requests.get(url=url,headers=headers)
    response.encoding = chardet.detect(response.content)["encoding"]
    html = etree.HTML(response.text)
    get_data(html)

# 对源码进行解析
def get_data(html):
    positions = html.xpath('//*[@id="resultList"]/div/p/span/a/text()') # 获得职位名
    position = []
    for i in positions:
        position.append(i.replace("\n",'').replace(" ","").replace("\r",""))
    company = html.xpath('//div[@class="el"]/span[@class="t2"]/a/text()')  # 获得公司名
    workPlace = html.xpath('//div[@class="el"]/span[@class="t3"]/text()') # 获得工作地点
    workSalary = html.xpath('//div[@class="el"]/span[@class="t4"]/text()') # 获得薪水
    workPublic = html.xpath('//div[@class="el"]/span[@class="t5"]/text()') # 获得工作地点
    zip_list = zip(position,company,workPlace,workSalary,workPublic)
    # print(list(zip_list))
    saveData(list(zip_list))
    next_url = html.xpath('//div[@class="p_in"]//li[last()]/a/@href')     # 得到下一页url
    if len(next_url) != 0:
        get_html(next_url[0])

def saveData(lists):
    with open('data1.csv', 'a', encoding='utf-8-sig', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for lis in lists:
            print("…………存入数据…………")
            writer.writerow(list(lis))

if __name__ == '__main__':
    with open('data1.csv', 'a', encoding='utf-8-sig', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['职位', '公司名', '工作地点', '工资', '发布日期'])
    url = "https://search.51job.com/list/000000,000000,0000,00,9,99,python,2,1.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare="
    get_html(url)
