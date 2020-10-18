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


def download(try_time, url, filename, callback):
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
        time.sleep(1)
        try_time +=1
        while try_time < 5:
            download(try_time,url, filename, callback)

# =============================================================================
# 乱码问题  done
# 循环问题  done
# 翻页问题  
# 由于网络问题无法下载全图片  
# =============================================================================
def one_page(url,output_path):
    #headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36'}
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'}
    web = requests.get(url, headers=headers)
    print('Current url is %s' % url)
    #web = requests.get(url)
    #web_req = request.Request(url)
    if ('扫码登录' in web.text) or ('请拖动滑块完成验证' in web.text):
        print('登录/滑动要求，停止')
        exit()
    else:
        # web.encoding = 'utf-8'
        url_prefix = url.split('?')[0]
        soup = BeautifulSoup(web.text, 'html.parser')
        search = soup.find("div", attrs={'id': 'J_ItemList'})
        nodes = search.find_all("div", attrs={'class': 'product'})
        last = len(nodes)
        df = pd.DataFrame()
        fail_to_download = pd.DataFrame()
        failure = {}
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
                store_name = '#J_ItemList > div:nth-child({}) > div > p.productStatus > span.ww-light.ww-small'.format(str(i))
                info['STORE_NAME'] = soup.select(store_name)[0]['data-nick']
            except:
                info['STORE_NAME'] = 'NA'


            price = '#J_ItemList > div:nth-child({}) > div > p.productPrice > em'.format(str(i))
            info['PRICE'] = soup.select(price)[0].text

            url = '#J_ItemList > div:nth-child({}) > div > p.productTitle > a'.format(str(i))
            info['URL'] = soup.select(url)[0]['href']

            title = str(info['PROD_ID'])
            this_img_url="http:"+info['IMG']
            img_path= output_path + title +".jpg"

            socket.setdefaulttimeout(15)
            try:
               request.urlretrieve(this_img_url,img_path)
            except:
               fail_to_download.append(title)

            time.sleep(1)
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
            img_path= output_path + title +".jpg"

            j = pathlib.Path(img_path)
            if not j.exists():
                # 设置超时时间为30s
                socket.setdefaulttimeout(15)
                try:
                   try_time = 0
                   download(try_time,this_img_url,img_path,cbk)
                   print(img_path, '\nDownload finished!')
                except:
                   failure['URL'] = img_url
                   failure['PROD_ID'] = title
                   fail_to_download = fail_to_download.append(failure, ignore_index = True)
                time.sleep(1)
            else:
                print("\n")
                print(img_path, "'File already exsits!'")
        next_page_loc = soup.select('a.ui-page-next')[0]['href']
        next_page_url = url_prefix + next_page_loc
        # content > div > div.ui-page > div > b.ui-page-num >
        return df, fail_to_download,next_page_url

def several_page(url,end_page,output_path):
    current_count = 1
    print('current page: %s' % current_count)
    base_df, base_fail_to_download,next_page_url = one_page(url,output_path)
    while current_count <= end_page:
        time.sleep(3)
        df, fail_to_download, next_page_url = one_page(next_page_url,output_path)
        base_df = base_df.append(df,ignore_index=True)
        base_fail_to_download = base_fail_to_download.append(fail_to_download,ignore_index=True)
        current_count +=1
        print('next page')
    else:
        print('Done')
        return base_df, base_fail_to_download



if __name__ == '__main__':
    url = 'https://list.tmall.com/search_product.htm?q=aptamil&type=p&spm=a220o.0.a2227oh.d100&from=.detail.pc_1_searchbutton'
    #url = 'https://list.tmall.com/search_product.htm??brand=101286946&s=60&q=aptamil&sort=s&style=g&from=.detail.pc_1_searchbutton&spm=a220o.0.a2227oh.d100&type=pc#J_Filter'
    process_date = '20201018'
    output_path = '../../Tmall_image_%s/' % process_date
    summary_path = '../../summary_files/'
    #df, fail_to_download,_ = one_page(url,output_path)

    ## several pages
    end_page = 3
    df, fail_to_download = several_page(url,end_page,output_path)

    df.to_csv('%s/Aptamil_page1_%s.csv' % (summary_path,process_date), index = False, encoding = 'utf-8-sig')
    fail_to_download.to_csv('%s/Fail_to_download_%s.csv'  % (summary_path,process_date),index = False, encoding = 'utf-8-sig')
