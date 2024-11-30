import time
import logging
#from google_flight_analysis.scrape import *
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from datetime import date, datetime, timedelta
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup as bs
import simplejson as json
import argparse
from collections import defaultdict
from src.objects.Processors.GoogleFlight import GoogleFlight
import src.objects.DatabaseHandler 
import sys

def parse_opts():
    parser = argparse.ArgumentParser(prog='main')
    parser.add_argument('-s','--scraprun', help="run the scrap portion", action='store_true')
    parser.add_argument('-l','--listrun', help="run the list processing portion", action='store_true')
    parser.add_argument('-i','--insertdb', help="run the list processing portion", action='store_true')

    args = parser.parse_args()
    opts = vars(args)
    return(opts)


def makeUrl(org, dest, date,lan,ret):
    #https://www.decolar.com/passagens-aereas/SAO/YVR?from=SB&di=1&searchType=ONEWAY&outboundMonthRanges=202411
    #https://www.decolar.com/passagens-aereas/SAO/{dest}?from=SB&di=1&searchType=ONEWAY&outboundMonthRanges=202411
    #https://www.maxmilhas.com.br/busca-passagens-aereas/OW/SAO/YVR/2025-03-01/1/0/0/EC
    #'https://www.maxmilhas.com.br/busca-passagens-aereas/OW/{org}/{dest}/2025-03-01/1/0/0/EC'
    #https://www.google.com/travel/flights/search?tfs=CBwQAhopEgoyMDI1LTA1LTAxag0IAhIJL20vMDIycGZtcgwIAhIIL20vMGZuMmcaKRIKMjAyNS0wNS0xMmoMCAISCC9tLzBmbjJncg0IAhIJL20vMDIycGZtQAFAAUgBcAGCAQsI____________AZgBAQ&hl=pt-BR&gl=br&client=safari&curr=BRL
    #https://www.google.com/travel/flights?hl=en&q=Flights%20to%20GRU%20from%20BCN%20on%202025-05-14%20roundtrip%20duration%2020
    return 'https://www.google.com/travel/flights?hl={lan}&q=Flights%20to%20{dest}%20from%20{org}%20on%20{date}%20oneway'.format(
        dest = dest,
        org = org,
        date = date,
        lan=lan
    )


def getHTML(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    print(url)
    driver.get(url)
    elementSource = driver.page_source
    driver.close()
    writeToFile('src/tmp/output.html', elementSource)
    return elementSource

def handleResponse(response, source):
    data = defaultdict(list)
    soup = bs(response, features="html.parser")
    t = soup.find_all("div", {"class": "JMc5Xc"}) #GRU,YVR,2024-12-01,en
    #t = soup.find_all("div", {"class": "cKvRXe"}) #GRU,FOR,2024-12-01,pt
    data[source].append(str(t))
    writeToFile('src/tmp/TextToProcess.txt', json.dumps(data,encoding='utf-8', ensure_ascii=False))

def writeToFile(filename, content):
    with open(filename, "w", encoding="utf-8") as file:
        if content != None:
            file.write(str(content))

def readFromFile(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()

def processRawData(sourceDict, org, dest, dateStr,lan):
    google = GoogleFlight(sourceDict['GoogleFlight'], org, dest, dateStr,lan)
    for flight in google.flights:
        logging.debug(flight.export())
    return google

def sumDays(dateStr, days):
    date = datetime.strptime(dateStr, '%Y-%m-%d')
    return (date + timedelta(days=days)).strftime('%Y-%m-%d')

def insertQuery(flight):
    relatedDict = flight.export()   
    layovers = ",".join(str(item) for item in relatedDict['layovers']).replace("'", '"')
    return '''INSERT into flightsearcher.flight VALUES (
        '{0}'
        ,'{1}'
        ,'{2}'::date
        ,{3}
        ,'{4}'
        ,'{5}'
        ,'{6}'
        ,{7}
        ,'{8}'
        ,'{9}'
        ,now()
    )'''.format(
        relatedDict['org'] if relatedDict['org'] is not None else 'NULL',
        relatedDict['dest'] if relatedDict['dest'] is not None else 'NULL',
        relatedDict['date'] if relatedDict['date'] is not None else 'NULL',
        relatedDict['price'] if relatedDict['price'] is not None else 'NULL',
        relatedDict['companies'] if relatedDict['companies'] is not None else 'NULL',
        relatedDict['departure'] if relatedDict['departure'] is not None else 'NULL',
        relatedDict['arrival'] if relatedDict['arrival'] is not None else 'NULL',
        relatedDict['stops'] if relatedDict['stops'] is not None else 'NULL',
        layovers if relatedDict['layovers'] is not None else 'NULL',
        relatedDict['duration'] if relatedDict['duration'] is not None else 'NULL'
    )

if __name__ == "__main__":
    sys.path.append('/Users/renan/Library/Python/3.9/lib/python/site-packages')
    optsHash = parse_opts()
    config = json.loads(readFromFile('src/config.json'))
    scenarios = pd.read_csv(config['run_file'])
    
    for indx, row in scenarios.iterrows():
        if indx % 10 == 0:
            time.sleep(10)
        org = row['org']
        dest = row['dest']
        dateStr = row['date']
        lan = row['lan']
        ret = sumDays(row['date'],row['days'])
        print('-'*50)
        print('Running scenario for {} to {} on {} returning at {}'.format(org,dest,dateStr,lan,ret))

        if optsHash['scraprun']:
            url = makeUrl(dest = dest,org = org,date = dateStr,lan=lan,ret=ret)
            html = getHTML(url)
            handleResponse(html, 'GoogleFlight')

        if optsHash['listrun']:
            sourceText = json.loads(readFromFile('src/tmp/TextToProcess.txt'))
            google = processRawData(sourceText, org, dest, dateStr, lan)

            if optsHash['insertdb']:
                db = src.objects.DatabaseHandler.init_db(config)
                for flight in google.flights:
                    insertStatement = insertQuery(flight)
                    db_hash = src.objects.DatabaseHandler.execute_qry_and_fetch_all_records(db, 'insertFlight', insertStatement)
                db['connection'].commit()

    #        with open('src/tmp/TextToProcess.txt', "r") as file:
    #            content = file.read()