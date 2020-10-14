# -*- coding: utf-8 -*-
"""
Created on Sun Aug 16 16:15:09 2020

@author: luya9001
"""
import requests
from bs4 import BeautifulSoup
# import re
import pandas as pd
from urllib import request,error
import time
import socket
import pathlib

url = 'https://list.tmall.com/search_product.htm?q=aptamil&type=p&spm=a220o.0.a2227oh.d100&from=.detail.pc_1_searchbutton'
web = requests.get(url)
# web.encoding = 'utf-8'

soup = BeautifulSoup(web.text, 'html.parser')
search = soup.find("div", attrs={'id': 'J_ItemList'})
nodes = search.find_all("div", attrs = {'class':'product'})
last = len(nodes)

df = pd.DataFrame()
fail_to_download = pd.DataFrame()
failure = {}

def cbk(a,b,c):
    '''回调函数
    @a:已经下载的数据块
    @b:数据块的大小
    @c:远程文件的大小
    '''
    per=100.0*a*b/c
    if per>100:
        per=100
    print('{:.1%}'.format(per/100))


def download(url, filename, callback):
    """
    封装了 urlretrieve()的自定义函数，递归调用urlretrieve(),当下载失败时，重新下载
    download file from internet
    :param url: path to download from
    :param savepath: path to save files
    :return: None
    """
    try:
        request.urlretrieve(url, filename, callback)
    except Exception as e:
        print(e)
        print('Network conditions is not good.\nReloading.....')
        download(url, filename, callback)

# =============================================================================
# 乱码问题  done
# 循环问题  done
# 翻页问题  
# 由于网络问题无法下载全图片  
# =============================================================================

for i in range(1, last + 1):
    info = {}
    img = '#J_ItemList > div:nth-child({}) > div > div > a > img'.format(str(i))
    try:
        info['IMG'] = soup.select(img)[0]['src']
    except:
        info['IMG'] = soup.select(img)[0]['data-ks-lazyload']
        
    prod_id = '#J_ItemList > div:nth-child({})'.format(str(i))
    info['PROD_ID'] = soup.select(prod_id)[0]['data-id']
    
    prod_desc = '#J_ItemList > div:nth-child({}) > div > p.productTitle > a'.format(str(i))
    info['PROD_DESC'] = soup.select(prod_desc)[0]['title']

    
    try:
        store_name = '#J_ItemList > div:nth-child({}) > div > div.productShop > a > span'.format(str(i))
        info['STORE_NAME'] = soup.select(store_name)[0].text
    except:
        info['STORE_NAME'] = 'NA'
    
    store_type = '#J_ItemList > div:nth-child({}) > div > div.productShop > a'.format(str(i))
    info['STORE_TYPE'] = soup.select(store_type)[0].text
    
    price = '#J_ItemList > div:nth-child({}) > div > p.productPrice > em'.format(str(i))
    info['PRICE'] = soup.select(price)[0].text
    
    url = '#J_ItemList > div:nth-child({}) > div > p.productTitle > a'.format(str(i))
    info['URL'] = soup.select(url)[0]['href']

    title = str(info['PROD_ID'])
    this_img_url="http:"+info['IMG']
    img_path="C:\\Users\\luya9001\\Desktop\\Tmall_image\\" + title +".jpg"
    
    socket.setdefaulttimeout(15)
    try:
       request.urlretrieve(this_img_url,img_path)
    except:
       fail_to_download.append(title)
      
    time.sleep(5)
    df = df.append(info, ignore_index = True)

# =============================================================================
#     
# =============================================================================

# =============================================================================
# 
# =============================================================================
for i in range(1, last + 1):
    info = {}
    img = '#J_ItemList > div:nth-child({}) > div > div > a > img'.format(str(i))
    try:
        info['IMG'] = soup.select(img)[0]['src']
    except:
        info['IMG'] = soup.select(img)[0]['data-ks-lazyload']
        
    prod_id = '#J_ItemList > div:nth-child({})'.format(str(i))
    info['PROD_ID'] = soup.select(prod_id)[0]['data-id']
    
# =============================================================================
#     prod_desc = '#J_ItemList > div:nth-child({}) > div > p.productTitle > a'.format(str(i))
#     info['PROD_DESC'] = soup.select(prod_desc)[0]['title']
# 
#     
#     try:
#         store_name = '#J_ItemList > div:nth-child({}) > div > div.productShop > a > span'.format(str(i))
#         info['STORE_NAME'] = soup.select(store_name)[0].text
#     except:
#         info['STORE_NAME'] = 'NA'
#     
#     store_type = '#J_ItemList > div:nth-child({}) > div > div.productShop > a'.format(str(i))
#     info['STORE_TYPE'] = soup.select(store_type)[0].text
#     
#     price = '#J_ItemList > div:nth-child({}) > div > p.productPrice > em'.format(str(i))
#     info['PRICE'] = soup.select(price)[0].text
#     
#     url = '#J_ItemList > div:nth-child({}) > div > p.productTitle > a'.format(str(i))
#     info['URL'] = soup.select(url)[0]['href']
# =============================================================================

    title = str(info['PROD_ID'])
    img_url="http:"+info['IMG']
    img_path="C:\\Users\\luya9001\\Desktop\\Tmall_image\\" + title +".jpg"
    
    j = pathlib.Path(img_path)
    if not j.exists():
        # 设置超时时间为30s
        socket.setdefaulttimeout(15)
        try:
           download(this_img_url,img_path,cbk)
           print(img_path, '\nDownload finished!')
        except:
           failure['URL'] = img_url
           failure['PROD_ID'] = title
           fail_to_download = fail_to_download.append(failure, ignore_index = True)
    else:
        print("\n")
        print(img_path, "'File already exsits!'")
    
    time.sleep(5)
    df = df.append(info, ignore_index = True)
    
df.to_csv('Aptamil_page1.csv', index = False, encoding = 'utf-8-sig')
fail_to_download.to_csv('Fail_to_download.csv',index = False, encoding = 'utf-8-sig')
