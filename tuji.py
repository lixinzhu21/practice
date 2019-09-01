# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import urllib
from bs4 import BeautifulSoup
from requests import get 
import time
import pandas as pd
import numpy as np




headers = ({'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})

sapo = "https://casa.sapo.pt/Venda/Apartamentos/?sa=11&or=10"
response = get(sapo, headers=headers)
html_soup = BeautifulSoup(response.text, 'html.parser')
house_containers = html_soup.find_all('div', class_="searchResultProperty")
first = house_containers[0]

price=first.find_all('span')[2].text
price=int(price.replace('\xa0','').replace('€',''))

location=first.find_all('p',class_='searchPropertyLocation')[0].text.strip()

size=int(first.find_all('p')[7].text.replace('m²',''))

for url in first.find_all('a'):
    print(url.get('href'))

link='https://casa.sapo.pt'+first.find_all('a')[0].get('href')







names=[]
regions=[]
prices=[]
scores=[]
distances=[]
describes=[]
links=[]

for pg in range(1,3):
    tujia='https://www.tujia.com/unitlist?startDate=2019-07-25&endDate=2019-07-26&cds=42_48_%25E5%258C%2597%25E4%25BA%25AC&cityId=48&page='+str(pg)
    response=get(tujia,headers=headers)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    house_containers = html_soup.find_all('div', class_="houseInfo-cont")
    for i in range(len(house_containers)):
        temp=house_containers[i]
        name=temp.find_all('a',class_='house-detail-link')[0].text
        link=temp.find_all('a',class_='house-detail-link')[0].get('href')
        region=temp.find_all('div',class_='region')[0].get('data-label')
        if len(temp.find_all('div',class_='distance-container')[0])==0:
            distance=''
            describe=temp.find_all('p')[0].text
        else:
            distance=temp.find_all('p')[0].text
            describe=temp.find_all('p')[1].text
            
        price=int(temp.find_all('span',class_='yuan')[0].text)
        try:
            score=float(temp.find_all('div',class_='score')[0].text.split('/')[0].replace('分',''))
        except:
            score=np.nan
        names.append(name)
        regions.append(region)
        prices.append(price)
        scores.append(score)
        distances.append(distance)
        describes.append(describe)
        links.append(link)
    time.sleep(3)
        
        
df=pd.DataFrame({'name':names,'region':regions,'price':prices,'score':scores,'distance':distances,'desc':describes,'link':links})   
