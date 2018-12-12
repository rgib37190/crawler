# coding: utf-8
import requests
from bs4 import BeautifulSoup
import json
from tqdm import tqdm_notebook
from lxml import etree
import pandas as pd

def get_link():
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'}
    session = requests.Session()
    url = 'https://www.dcard.tw/f/mood'
    request = requests.get(url,headers=headers)
    bsobj = BeautifulSoup(request.text,"html.parser")
    
    link_list = []
    links = bsobj.select("div.PostList_wrapper_2BLUM a.PostEntry_root_V6g0r")
    for link in links:
        link_list.append(link['href'])
        link = 'https://www.dcard.tw' + link['href']
        yield link
    for k in tqdm_notebook(range(0,100000)):
        post_data={
            "popular":"true",
            "limit":"30",
            "before":link_list[-1][10:19]
        }
        get_link = session.get("https://www.dcard.tw/_api/forums/mood/posts?",params=post_data,
                                headers = headers)
        data2 = json.loads(get_link.text)
        for i in range(len(data2)):
            temporary_url = "/f/mood/p/"+ str(data2[i]["id"])
            temporary_url= 'https://www.dcard.tw' + temporary_url
            yield temporary_url


headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'}
for link in get_link():
    request = requests.get(link,headers=headers)
    selector = etree.HTML(request.text)
    title = selector.xpath('//h2[@class="Post_title_2O-1e"]/text()')
    article = selector.xpath('//div[@class="Post_content_NKEl9"]/div/div/div/descendant::text()')
    article = "\n".join(article)
    article_tag = selector.xpath('//a[@class="TopicList_topic_1XGOj"]/text()')
    article_tag = article_tag[15:]
    article_tag = ",".join(article_tag)
    review = selector.xpath('//div[@class="CommentEntry_content_1ATrw"]/descendant::text()')
    review = "\n".join(review)
    output_data = pd.DataFrame({'title':title,'article':article,'article_tag':article_tag,
                               'review':review})
    with open('ds_project_data.csv','a+') as f:
        output_data.to_csv(f,header=None,encoding='utf8')
    






