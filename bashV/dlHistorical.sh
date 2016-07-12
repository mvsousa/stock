#!/bin/bash
rm -rf data
mkdir data
cd data
mkdir nasdaq
cd nasdaq
mkdir stocks
cd ..
cd ..

awk '   BEGIN {FS = "\",\""} 
        {
                StockSymbol    = substr($1, 2, length($1)-0)
                StockName      = substr($2, 0, length($2)-0)
                StockLastSale  = substr($3, 0, length($3)-0)
                StockMarketCap = substr($4, 0, length($4)-0)
                StockIPOYear   = substr($5, 0, length($5)-0)
                StockSector    = substr($6, 0, length($6)-0) 
                StockIndustry   = substr($7, 0, length($7)-0)
                StockInfo      = substr($8, 0, length($8)-3)
                print StockName      > "data/nasdaq/name.txt"
                print StockSymbol    > "data/nasdaq/symbols.txt"
                print StockLastSale  > "data/nasdaq/lastsale.txt"
                print StockMarketCap > "data/nasdaq/marketcap.txt"
                print StockIPOYear   > "data/nasdaq/ipoyear.txt"
                print StockSector    > "data/nasdaq/sector.txt"
                print StockIndustry  > "data/nasdaq/industry.txt"
                print StockInfo      > "data/nasdaq/info.txt"
                
        }' < ../StockList/nasdaq.csv
FILE=data/nasdaq/symbols.txt
COUNT=1
total=$(cat data/nasdaq/name.txt | wc -l)
while read line; do
        echo "Downloading $line Historical Stocks..."
        rm -rf data/nasdaq/stocks/$line
        mkdir data/nasdaq/stocks/$line
        wget ichart.finance.yahoo.com/table.csv?s=$line -O data/nasdaq/stocks/$line/$line.csv
        a=`sed -n "${COUNT}p" data/nasdaq/name.txt`
        b=`sed -n "${COUNT}p" data/nasdaq/symbols.txt`
        c=`sed -n "${COUNT}p" data/nasdaq/lastsale.txt`
        d=`sed -n "${COUNT}p" data/nasdaq/marketcap.txt`
        e=`sed -n "${COUNT}p" data/nasdaq/ipoyear.txt`
        f=`sed -n "${COUNT}p" data/nasdaq/sector.txt`
        g=`sed -n "${COUNT}p" data/nasdaq/industry.txt`
        h=`sed -n "${COUNT}p" data/nasdaq/info.txt`
        echo "Progress $COUNT/$total"
        COUNT=$((COUNT+1))
        content=$(cat data/nasdaq/stocks/$line/$line.csv) # no cat abuse this time
        echo "Symbols, Last Sale, MarketCap, IPOYear, Sector, Industry, Info, Name,\n $b,$c,$d,$e,$f,$g,$h,$a\n\n$content" > data/nasdaq/stocks/$line/$line.csv

done < $FILE
