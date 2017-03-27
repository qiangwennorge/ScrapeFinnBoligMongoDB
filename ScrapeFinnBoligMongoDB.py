# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 20:59:32 2017

@author: qiangwennorge
"""

from pymongo import MongoClient



clientmongo = MongoClient(host = "localhost", port=27017)
databasehandler = clientmongo["FinnBoligDB"]

BoligUrl = "https://www.finn.no/realestate/homes/search.html?filters="
