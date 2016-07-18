#!/usr/bin/env python
import sys
import urllib
import os
import shutil
import csv
import select
import socket 
from urllib.request import urlretrieve

def line_prepender(filename, line):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)

def setup():
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
            name = ''
            summary = '"Symbol","Name","LastSale","MarketCap","IPOyear","Sector","industry","SummaryQuote",'
            stockParam = row
            stockName = str(row[0])
            stockPath = "../data/" + stockName
            os.system('cls' if os.name == 'nt' else 'clear')
           # print (stockName)
            for a in range (15, 0, -2):
                name = "\""+(str(row).split('\'',-1)[a]) + "\"" + ", " + name
            print ("Progress: " + str(i) + "/" + str(total) + " files downloaded")
            print ("Downloading " + stockName + " stock historical data")
            print ("Press enter to stop...")
            path = ''
            if not os.path.exists(stockPath):
                os.makedirs(stockPath)
                link = 'http://' + 'ichart.finance.yahoo.com/table.csv?s=' + stockName
                path = stockPath + "/" + stockName + ".csv"
                try:
                    urllib.request.urlretrieve(link, path)
                except socket.gaierror as error:
                    print ("Error")
                except urllib.error.HTTPError as error:
                    print ("Error")
                else:
                    print (" ")
            if os.path.exists(path):
                line_prepender(path, '\n')
                line_prepender(path, name)
                line_prepender(path, summary)

            if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                line = input()
                notDelete = False
                sys.exit(0)
                break
            i += 1
        if notDelete:
            os.remove("../StockList/progress/download.csv")

nasdaq = 'http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nasdaq&render=download'
nyse = 'http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nyse&render=download'
amex = 'http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=amex&render=download'
            
markets = [nasdaq, nyse, amex]
if not os.path.exists("../StockList"):
    os.makedirs("../StockList")
    os.makedirs("../StockList/progress")

    for i in range (0, 1):
        market =  (markets[i].split('=', -1)[2].split('&',-1)[0])
        path =  "../StockList/" + market + ".csv"
        urllib.request.urlretrieve(markets[i], path)
        subpath =  "../StockList/progress/" + market + ".csv"
        shutil.copy(path, subpath)
    setup()
else:
    setup()





























