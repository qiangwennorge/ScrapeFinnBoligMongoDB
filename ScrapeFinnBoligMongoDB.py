# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 20:59:32 2017

@author: qiangwennorge
"""

from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
import re
import pymongo

# Get Bolig information in each page

def GetInfoOfEachRealestate(BoligDoc,soup):
    for ParentalTag in soup.find_all('div','unit flex align-items-stretch result-item'):
        BoligFinnCode = ParentalTag.contents[1].get('id')
        BoligTitle = ParentalTag.contents[1].find_all('h3')[0].string
        EachBoligDoc = {'boligfinncode': BoligFinnCode,
                        'boligtitle':BoligTitle}  
        BoligDoc.append(EachBoligDoc)
    return BoligDoc

# Start from first page

BoligDoc = []

BoligUrl = "https://www.finn.no/realestate/homes/search.html?filters="
BoligResponse = requests.get(BoligUrl)
BoligContent = BoligResponse.content

BoligSoup = BeautifulSoup(BoligContent,"html.parser")

BoligDoc = GetInfoOfEachRealestate(BoligDoc,BoligSoup) 

# Find the next page number

InitialTagsForNextPage = BoligSoup.find_all('div','t4 centerify r-margin')[0]
SecondPage = InitialTagsForNextPage.find_all('a',class_='pam')[0].get('href')
NextPageNum = int(re.findall(r'page=(\d+)', SecondPage)[0])

# Go to the rest pages

for PageNum in range(NextPageNum,3):
    NextPage = re.sub(r'page=(\d+)', 'page='+str(PageNum), SecondPage)
    NextUrl = 'https://m.finn.no' + NextPage
    NextResponse = requests.get(NextUrl)
    NextHtml = NextResponse.content
    print PageNum
    NextSoup = BeautifulSoup(NextHtml,"html.parser")
    TotalBoligDoc = GetInfoOfEachRealestate(BoligDoc,NextSoup)    

# Save collected bolig information to MongoDB
clientmongo = MongoClient(host = "localhost", port=27017)
databasehandler = clientmongo["FinnBoligDB"]
for EachBoligDoc in BoligDoc:
    databasehandler.boligcollection.insert(EachBoligDoc,safe=True)


