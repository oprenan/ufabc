import sys
import pandas as pd # type: ignore
import requests # type: ignore
from requests_html import HTMLSession # type: ignore
from bs4 import BeautifulSoup as bs # type: ignore
from selenium import webdriver
from selenium.webdriver.chrome.options import Options  
from time import sleep

class FlightScrapper:
    def _make_url(self):
            #https://www.decolar.com/passagens-aereas/SAO/YVR?from=SB&di=1&searchType=ONEWAY&outboundMonthRanges=202411
            #https://www.decolar.com/passagens-aereas/SAO/{dest}?from=SB&di=1&searchType=ONEWAY&outboundMonthRanges=202411
            #https://www.maxmilhas.com.br/busca-passagens-aereas/OW/SAO/YVR/2025-03-01/1/0/0/EC
            #'https://www.maxmilhas.com.br/busca-passagens-aereas/OW/{org}/{dest}/2025-03-01/1/0/0/EC'
            return 'https://www.maxmilhas.com.br/busca-passagens-aereas/OW/{org}/{dest}/2025-03-01/1/0/0/EC'.format(
                dest = self._dest,
                org = self._origin
            )

    def __init__(self, origin, destination, date_leave, date_return):
        self._origin = origin
        self._dest = destination
        self._date_leave = date_leave
        self._date_return = date_return
        self._url = self._make_url()
    
    def __str__(self) -> str:
        print ('FlightScrapper from {org} to {dest} on {dl} through {dr}'.format(self._origin,self._dest,self._date_leave,self._date_return))    

    def write_to_file(self, filename, content):
        with open(filename, "wb") as file:
            if content != None:
                file.write(content)
            else:
                soup = bs(self.response.text,features="lxml")
                file.write(soup.prettify("utf-8"))

    def make_request(self):
        url = self._url
        print(url)
        headers ={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
            "method": "GET"
        }
        session = HTMLSession()
        self.response = session.get(url, headers=headers) 
        self.write_to_file('output1.html')
        self.response.html.render(timeout=30)
        self.write_to_file('output2.html')
        soup = bs(self.response.text, features="lxml")
        return soup.prettify("utf-8")
        
    def make_request_selenium(self):
        chrome_options = Options()
        #chrome_options.add_argument("--headless")
        driver = webdriver.Chrome()
        driver.get(self._url)
        print("sleeping")
        sleep(20)
        content = driver.page_source
        soup = bs(content, features="html.parser")
        self.write_to_file('output.html', soup.prettify("utf-8"))
    
    
if __name__ == "__main__":
    flight = FlightScrapper('SAO', 'YVR', '2025-04-01', '2025-14-12')
    src = flight.make_request_selenium()
    #flight.write_to_file('output.html')
    
