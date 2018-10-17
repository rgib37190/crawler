

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt
import requests
import time
import csv

for i in range(1,64104):
    try:
        #control button by selenium
        url = 'https://etherscan.io/blocks?p='+str(i)
        chrome_options = Options()
        chrome_options.add_argument("--headless")  #let google chrome not open
        driver = webdriver.Chrome(r'C:/Users/champ/Desktop/blockchain/chromedriver.exe',chrome_options=chrome_options)
        driver.get(url)
        select = Select(driver.find_element_by_name("ctl00$ContentPlaceHolder1$ddlRecordsPerPage"))
        select.select_by_index(3)  #select page = '100'
        
        #crawl time
        datetime = []
        bsobj = BeautifulSoup(driver.page_source,'lxml')
        for title in bsobj.findAll('span',attrs={'rel':'tooltip'}):
            time = title.get('data-original-title')
            datetime.append(time)
        #crawl data    
        data = pd.read_html(driver.page_source)
        eth_data = pd.DataFrame(data[0])
        eth_data['Age'] = datetime
        with open('eth_data.csv','a+') as f:
            eth_data.to_csv(f,header=None)
        print('Page finish%s:' %str(i))
        driver.quit()

        
    except:#try again
        try:
            url = 'https://etherscan.io/blocks?p='+str(i)
            chrome_options = Options()
            chrome_options.add_argument("--headless")   #不把瀏覽器打開
            driver = webdriver.Chrome(r'C:/Users/champ/Desktop/blockchain/chromedriver.exe',chrome_options=chrome_options)
            driver.get(url)
            select = Select(driver.find_element_by_name("ctl00$ContentPlaceHolder1$ddlRecordsPerPage"))
            select.select_by_index(3)
        
            datetime = []
    
            bsobj = BeautifulSoup(driver.page_source,'lxml')
            for title in bsobj.findAll('span',attrs={'rel':'tooltip'}):
                time = title.get('title')
                datetime.append(time)
            
            data = pd.read_html(driver.page_source)
            eth_data = pd.DataFrame(data[0])
            eth_data['Age'] = datetime
            with open('eth_data.csv','a+') as f:
                eth_data.to_csv(f,header=None)
            driver.quit()
            print('try again page finish:%s' %str(i))
        except:
            print('page cannot finish%s' %str(i))
        

