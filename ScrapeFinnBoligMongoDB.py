# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 20:59:32 2017

@author: qiangwennorge
"""

from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
import re

def GetLinkOfEachRealestate(LinkList, soup):
    for ParentalTag in soup.find_all('div','unit flex align-items-stretch result-item'):
        OneLinkOfEachRealestate = ParentalTag.contents[1].get('href')
        #print OneLinkOfEachRealestate
        LinkList.append(OneLinkOfEachRealestate)
    return LinkList


clientmongo = MongoClient(host = "localhost", port=27017)
databasehandler = clientmongo["FinnBoligDB"]

BoligUrl = "https://www.finn.no/realestate/homes/search.html?filters="
BoligResponse = requests.get(BoligUrl)
BoligContent = BoligResponse.content

BoligSoup = BeautifulSoup(BoligContent,"html.parser")

InitialTagsForNextPage = BoligSoup.find_all('div','t4 centerify r-margin')[0]
SecondPage = InitialTagsForNextPage.find_all('a',class_='pam')[0].get('href')

NextPageNum = int(re.findall(r'page=(\d+)', SecondPage)[0])

LinkList = []
FirstLinkList = GetLinkOfEachRealestate(LinkList, BoligSoup)

for PageNum in range(NextPageNum,3):
    NextPage = re.sub(r'page=(\d+)', 'page='+str(PageNum), SecondPage)
    NextUrl = 'https://m.finn.no' + NextPage
    NextResponse = requests.get(NextUrl)
    NextHtml = NextResponse.content
    print PageNum
    NextSoup = BeautifulSoup(NextHtml,"html.parser")    
    NextLinkList = GetLinkOfEachRealestate(FirstLinkList, NextSoup)






#SecondLinkList = GetLinkOfEachRealestate(LinkList, InitialSoup)

