# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import urllib
from bs4 import BeautifulSoup
import requests 
import time
import pandas as pd
import numpy as np

headers = ({'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})

link='https://bj.lianjia.com/ershoufang/l2c1111027375333/?sug=%E5%8D%8E%E8%85%BE%E5%9B%AD'

response=requests.get(link,headers=headers)
html_soup = BeautifulSoup(response.text, 'html.parser')
house_containers = html_soup.find_all('div',class_='info clear')

name=[]
link=[]
total=[]
unit=[]
img=[]
detail=[]
#house_id=[]
d=dict()


for i in range(len(house_containers)):
    sub_link=house_containers[i].find('a',class_="").get('href')
    sub_response=requests.get(sub_link,headers=headers)
    sub_soup=BeautifulSoup(sub_response.text, 'html.parser')
    
    
    name.append(sub_soup.find('h1',class_="main").text)
    link.append(sub_link)
    #house_id.append(sub_link.split('/')[-1].replace('.html',''))
    
    total.append(sub_soup.find_all('span',class_='total')[0].text)
    unit.append(sub_soup.find_all('span',class_='unitPriceValue')[0].text)
    try:
        img.append(sub_soup.find_all('div',class_='imgdiv')[0].get('data-img')+'.720x540.jpg')
        #get area of each rooms
        area=sub_soup.find_all('div',class_='row') 
        s=str()      
        for j in range(len(area)-1):
            temp=area[j].find_all('div',class_='col')[0].text+":"+area[j].find_all('div',class_='col')[1].text+", "
            s=s+temp 
        detail.append(s[:-2])
    except:
        img.append('NA')
        detail.append('NA')
    
    

    #get basic and transaction info
    content=sub_soup.find_all('div',class_='introContent')[0].find_all('span',class_='label')
    for item in content:
        if item.next_sibling=='\n':
            if item.text in d.keys():
                d.get(item.text).append(item.find_next_sibling("span").string.replace("<span>","").strip())
            else:
                d[item.text]=[item.find_next_sibling("span").string.replace("<span>","").strip()]
        else:
            if item.text in d.keys():
                d.get(item.text).append(item.next_sibling)
            else:
                d[item.text]=[item.next_sibling]
                
    time.sleep(5)



d['name']=name
d['total']=total
d['unit']=unit
d['img']=img
d['detail']=detail
#d['house_id']=house_id
d['link']=link

df=pd.DataFrame(d,columns=d.keys())

df=df[['name', 'total', 'unit','房屋户型', '所在楼层', '建筑面积', '户型结构', '套内面积', '建筑类型', '房屋朝向', '建筑结构', '装修情况',
       '梯户比例', '供暖方式', '配备电梯', '产权年限','img', 'detail','挂牌时间', '交易权属', '上次交易', '房屋用途', '房屋年限',
       '产权所属', '抵押信息', '房本备件','link']]

df.to_csv('house_test.csv',index=False,encoding='utf-8-sig')



   







#sub_container=sub_soup.find_all('div',class_='introContent')
#basic=sub_container[0].find_all('div',class_='content')[0].find_all('span',class_='label')
#trans=sub_container[0].find_all('div',class_='content')[1].find_all('span',class_='label')























