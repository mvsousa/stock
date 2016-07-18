#!/usr/bin/env python
import sys
import urllib
import os
import shutil
import csv
import select
import socket 

from urllib.request import urlretrieve
nasdaq = 'http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nasdaq&render=download'
nyse = 'http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nyse&render=download'
amex = 'http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=amex&render=download'
southam = 'http://www.nasdaq.com/screening/companies-by-region.aspx?region=South+America&render=download'

def size(name):
    with open(name) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def download():
    i = 0
    total = size("../StockList/progress/download.csv")
    notDelete = True
    with open("../StockList/progress/download.csv", 'r') as csvopen:
        csvdownload = csv.reader(csvopen, delimiter = ',')
        for row in csvdownload:
            stockParam = row
            stockName = str(row[0])
            stockPath = "../data/" + stockName
            os.system('cls' if os.name == 'nt' else 'clear')
            print (stockName)
            print ("Progress: " + str(i) + "/" + str(total) + " files downloaded")
            print ("Downloading " + stockName + " stock historical data")
            print ("Press enter to stop...")
            if not os.path.exists(stockPath):
                os.makedirs(stockPath)
                link = 'http://' + 'ichart.finance.yahoo.com/table.csv?s=' + stockName
                path = stockPath + "/" + stockName + ".csv"
                try:
                    urllib.request.urlretrieve(link, path)
                except urllib.error.HTTPError as error:
                    print ("Erro ao baixar essa Stock")
                else:
                    print ("File downloaded")
            if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                line = input()
                notDelete = False
                break
            i += 1
        if notDelete:
            os.remove("../StockList/progress/download.csv")
#        This should remove lines            
#        lines = open("../StockList/progress/download.csv").readlines()
#        open("../StockList/progress/download.csv", 'w').writelines(lines[i:-1])

markets = [nasdaq, nyse, amex]
if not os.path.exists("../StockList"):
    os.makedirs("../StockList")
    os.makedirs("../StockList/progress")

    for i in range (0, 3):
        market =  (markets[i].split('=', -1)[2].split('&',-1)[0])
        path =  "../StockList/" + market + ".csv"
        urllib.request.urlretrieve(markets[i], path)
        subpath =  "../StockList/progress/" + market + ".csv"
        shutil.copy(path, subpath)
else:
    if not os.path.exists("../data"):
        os.makedirs("../data")
    files = os.listdir("../StockList/progress")
    while True:
        if not files:
            break
        if not os.path.exists("../StockList/progress/download.csv"):
            oFile = "../StockList/progress/" + files.pop()
            os.rename(oFile, "../StockList/progress/download.csv")
            download()
            files = os.listdir("../StockList/progress")
        else: 
            download()
            files = os.listdir("../StockList/progress")






























