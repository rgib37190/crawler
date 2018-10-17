import jieba
import jieba.posseg
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.common.keys import Keys
import requests
from selenium.webdriver.common.action_chains import ActionChains
import urllib
import re
from lxml import etree

with open('crawler_word3.txt',encoding='cp950') as f:
    crawler_txt = f.read()

crawler_txt = crawler_txt.replace('\n','')

word_list = []
for word, word_type in jieba.posseg.cut(crawler_txt):
    if word_type != 'x':
        word_list.append(word)

count = 0

for query in word_list:
    try:
        # 先將事先準備好的文本去輸入查詢app
        url = 'https://play.google.com/store/search?q&c=apps'
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # let google chrome not open
        chrome_options.add_argument("--no-sandbox")
        driver1 = webdriver.Chrome(r'C:/Users/champ/Desktop/blockchain/chromedriver.exe', chrome_options=chrome_options)
        driver1.get(url)
        elem = driver1.find_element_by_name("q")  # 查詢
        elem.send_keys(query)
        elem.send_keys(Keys.ENTER)
        # 找到付費app的網址
        url2 = driver1.current_url
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # let google chrome not open
        driver2 = webdriver.Chrome(r'C:/Users/champ/Desktop/blockchain/chromedriver.exe', chrome_options=chrome_options)
        driver2.get(url2)
        bsobj = BeautifulSoup(driver2.page_source, 'lxml')
        crawl_app_link = []
        for url in bsobj.findAll('a', {'title': '付費'}):
            target_url = url.attrs['href']
            final_url = 'https://play.google.com' + target_url
            # 得到app的網址
            chrome_options = Options()
            chrome_options.add_argument("--headless")  # let google chrome not open
            driver3 = webdriver.Chrome(r'C:/Users/champ/Desktop/blockchain/chromedriver.exe',
                                       chrome_options=chrome_options)
            driver3.get(final_url)
            bsobj2 = BeautifulSoup(driver3.page_source, 'lxml')
            for app_link in bsobj2.findAll('a', {'class': 'title'}):
                final_app_link = app_link.attrs['href']
                final_app_link = 'https://play.google.com' + final_app_link
                link_number = 0
                for exist_links in exist_link['link']:
                    if final_app_link == exist_links:
                        link_number += 1
                if link_number == 0:
                    crawl_app_link.append(final_app_link)
            driver3.quit()
        link_df = pd.DataFrame({'link': crawl_app_link})
        with open('link1.csv', 'a+') as f:
            link_df.to_csv(f, header=None, encoding='utf8')
        driver1.quit()
        driver2.quit()
        count = count + 1
        print('fininsh percentage:%f %%' % (count / len(word_list) * 100))
    except:
        count = count + 1
        print('error')


count = 0
link_data = pd.read_csv('exist_link.csv')
for link in link_data['link'][:5000]:
    try:
        #開始抓取app資料
        chrome_options = Options()
        chrome_options.add_argument("--headless")#let google chrome not open
        chrome_options.add_argument("--lang=zh-tw")
        chrome_options.add_argument("--no-sandbox")
        data_driver = webdriver.Chrome(r'C:/Users/champ/Desktop/blockchain/chromedriver.exe',chrome_options=chrome_options)
        data_driver.get(link)

        app_name_list = []
        genre_list = []
        rating_list = []
        review_list = []
        size_list = []
        install_number_list = []
        price_list = []
        content_rating_list = []
        update_date_list = []
        rating_5_list = []
        rating_4_list = []
        rating_3_list = []
        rating_2_list = []
        rating_1_list = []

        bsobj = BeautifulSoup(data_driver.page_source,'lxml')
        #app_name
        for app_name in bsobj.findAll('h1',{'class':'AHFaub'}):
            app_name_list.append(app_name.get_text())
        #genre
        for genre in bsobj.findAll('a',{'itemprop':'genre'}):
            genre_list.append(genre.get_text())
        if len(genre_list) > 1:
            genre_list.pop()
        if len(genre_list) == 0:
            genre_list.append(None)
        #rating
        for rating in bsobj.findChild('div',{'class':'pf5lIe'}):
            text = rating.attrs['aria-label']
            text1 = text.split(' ')[1]
            rating_list.append(text1)
        if len(rating_list) > 1:
            rating_list.pop()
        if len(rating_list) == 0:
            rating_list.append(None)
        #review
        for review in bsobj.findAll('span',{'class':'O3QoBc hzfjkd'}):
            review_list.append(review.next_sibling.get_text())
        if len(review_list) > 1:
            review_list.pop()
        if len(review_list) == 0:
            review_list.append(0)
        #rating5
        for rating_5 in bsobj.findAll('span',{'class':'L2o20d P41RMc'}):
            rating_5_list.append(rating_5.attrs['title'])
        if len(rating_5_list) == 0:
            rating_5_list.append(0)
        #rating4
        for rating_4 in bsobj.findAll('span',{'class':'L2o20d tpbQF'}):
            rating_4_list.append(rating_4.attrs['title'])
        if len(rating_4_list) == 0:
            rating_4_list.append(0)
        #rating3
        for rating_3 in bsobj.findAll('span',{'class':'L2o20d Sthl9e'}):
            rating_3_list.append(rating_3.attrs['title'])
        if len(rating_3_list) == 0:
            rating_3_list.append(0)
        #rating2
        for rating_2 in bsobj.findAll('span',{'class':'L2o20d rhCabb'}):
            rating_2_list.append(rating_2.attrs['title'])
        if len(rating_2_list) == 0:
            rating_2_list.append(0)
        #rating1
        for rating_1 in bsobj.findAll('span',{'class':'L2o20d A3ihhc'}):
            rating_1_list.append(rating_1.attrs['title'])
        if len(rating_1_list) == 0:
            rating_1_list.append(0)
        #size
        result_number = 0
        for size in bsobj.findAll('span',{'class':'htlgb'}):
            text = size.get_text()
            pattern = re.compile(r'\d*\.{0,1}\d*M')
            result = re.match(pattern,text)
            if result:
                if result_number == 0:
                    size_list.append(result.group())
                result_number = result_number + 1
        if len(size_list) == 0:
            size_list.append(None)
        #install_number
        result_number = 0
        for install_number in bsobj.findAll('span',{'class':'htlgb'}):
            text = install_number.get_text()
            pattern = re.compile(r'.*\+')
            result = re.match(pattern,text)
            if result:
                if result_number == 0:
                    install_number_list.append(result.group())
                result_number = result_number + 1
        if len(install_number_list) == 0:
            install_number_list.append(None)
        #content_rating
        result_number = 0
        for content_rating in bsobj.findAll('span',{'class':'htlgb'}):
            text = content_rating.get_text()
            pattern = re.compile(r'\d* 歲以上')
            result = re.match(pattern,text)
            if result:
                if result_number == 0:
                    content_rating_list.append(result.group())
                result_number = result_number + 1
        if len(content_rating_list) == 0:
            content_rating_list.append(None)
        #update_date
        result_number = 0
        for update_date in bsobj.findAll('span',{'class':'htlgb'}):
            text = update_date.get_text()
            pattern = re.compile(r'\d+年\d+月\d+日')
            result = re.match(pattern,text)
            if result:
                if result_number == 0:
                    update_date_list.append(result.group())
                result_number = result_number + 1
        if len(update_date_list) == 0:
            update_date_list.append(None)
        #price
        en_html = etree.HTML(data_driver.page_source)
        price_xpath = en_html.xpath('//*[@id="fcxH9b"]/div[4]/c-wiz/div/div[2]/div/div[1]/div/c-wiz[1]/c-wiz[1]/div/div[2]/div/div[2]/div/div[2]/div[2]/c-wiz/div/span/button/text()')
        for button_text in price_xpath:
            if button_text == '安裝':
                price_list.append(0)
            else:
                button_text = str(button_text).replace('購買','')
                button_text = button_text.replace('(','')
                button_text = button_text.replace(')','')
                button_text = button_text.replace('$','')
                price_list.append(button_text)
        #結果製成dataframe
        result = pd.DataFrame({'app_name':app_name_list,'genre':genre_list,'rating':rating_list,'review':review_list,
                            'size':size_list,'install_number':install_number_list,'price':price_list,
                             'content_rating':content_rating_list,'update_date':update_date_list,
                             'rating_5':rating_5_list,'rating_4':rating_4_list,'rating_3':rating_3_list,
                            'rating_2':rating_2_list,'rating_1':rating_1_list})
        with open('renew_data1.csv','a+') as f:
            result.to_csv(f,header=None,encoding='utf8')
        data_driver.quit()
        count = count + 1
        print('fininsh percentage:%f %%' %(count/len(link_data['link'][:5000])*100))
    except:
        print('error')
        count = count + 1

