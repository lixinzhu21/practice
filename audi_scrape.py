# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 23:07:49 2019

@author: lixinzhu21
"""

import urllib
from bs4 import BeautifulSoup
from requests import get 
import time
import pandas as pd
import numpy as np
import time

headers = ({'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})

link = "http://www.12365auto.com/zlts/index.shtml?page=1&cb=1&cs=0&cm=0&ba=0&qt=0&z=0&zs=0&f=0&nt=0&wd=%e5%af%bc%e8%88%aa"
response = get(link, headers=headers)
html_soup = BeautifulSoup(response.text, 'html.parser')
#house_containers = html_soup.find_all('div', class_="searchResultProperty")

container=html_soup.find_all('div',class_="tslb_b")[0].find_all('tr')

columns=[i.text for i in container[0].find_all('th')]

m=[]
for i in range(1,len(container)):
    m.append([j.text for j in container[i].find_all('td')])
    

for x in range(2,5):
    link="http://www.12365auto.com/zlts/index.shtml?page="+str(x)+"&cb=1&cs=0&cm=0&ba=0&qt=0&z=0&zs=0&f=0&nt=0&wd=%e5%af%bc%e8%88%aa"
    response = get(link, headers=headers)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    container=html_soup.find_all('div',class_="tslb_b")[0].find_all('tr')
    for i in range(1,len(container)):
        m.append([j.text for j in container[i].find_all('td')])
    time.sleep(3)
    
    
df=pd.DataFrame(m,columns=columns)

df.to_csv('navigation.csv',index=False,encoding='utf-8-sig')



link = "http://www.12365auto.com/zlts/index.shtml?cb=1&cs=0&cm=0&ba=0&qt=0&z=0&zs=0&f=0&nt=0&wd=%25E5%259C%25B0%25E5%259B%25BE"
response = get(link, headers=headers)
html_soup = BeautifulSoup(response.text, 'html.parser')
#house_containers = html_soup.find_all('div', class_="searchResultProperty")

container=html_soup.find_all('div',class_="tslb_b")[0].find_all('tr')

columns=[i.text for i in container[0].find_all('th')]

m=[]
for i in range(1,len(container)):
    m.append([j.text for j in container[i].find_all('td')])
    
df=pd.DataFrame(m,columns=columns)

df.to_csv('navigation2.csv',index=False,encoding='utf-8-sig')
