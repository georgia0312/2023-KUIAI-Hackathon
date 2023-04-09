# 무신사 스탠다드 상품 태그 크롤링

import requests
from bs4 import BeautifulSoup
import pandas as pd

start = 1
title_list = []
url_list = []

while start < 2:  # 1페이지만 가져오기 
    try:
        url = 'https://www.musinsa.com/brands/musinsastandard?category3DepthCodes\
                =&category2DepthCodes=&category1DepthCode=&colorCodes=&startPrice=\
                &endPrice=&exclusiveYn=&includeSoldOut=&saleGoods=&timeSale=&includeKeywords\
                =&sortCode=emt_high&tags=&page=1&size=90&listViewType=small&campaignCode=\
                &groupSale=&outletGoods=false&boutiqueGoods='.format(start)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')

        for soup in soup.find_all('a', attrs={'class': 'img-block'}):
            title_list.append(soup['title'])
            url_list.append('https:' + soup['href'])
        start += 1
    except:
        print(start)
        break

df = pd.DataFrame({'상품명': title_list,
                  'url': url_list})

if __name__ == '__main__':
    tag1 = []
    df['tags']=''
    for j in range(len(df)): #행마다 태그 가져오기
        url = df.iloc[j]['url'] #j행 url 가져오기
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)\
                    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        soup.find_all('a', attrs={'class': 'listItem'})
        length = len(soup.find_all('a', attrs={'class': 'listItem'}))
        tag=[]
        for i in range(length): #모든 태그 하나의 리스트(tag)로 저장
           tag.append(soup.find_all('a', attrs={'class': 'listItem'})[i].get_text())
        df.iat[j, 2] = tag
        #print(tag)
        tag1.append(tag)

df.to_csv('무신사tags.csv', encoding = 'utf-8-sig')

