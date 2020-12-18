import json
import re
import traceback

import requests
from bs4 import  BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options

options = Options()
# options.add_argument('--ignore-certificate-errors')
# options.add_argument('--disable-gpu')
# options.add_argument('--headless')
options.headless=True

# url = 'https://www.kmart.com.au/product/sodaking-windsor-soda-maker/3249331'
# driver.get(url)
# html = driver.find_element_by_class_name('title')

headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:83.0) Gecko/20100101 Firefox/83.0'}
# print(html)

def scrap1(url,driver):
    # driver = webdriver.Chrome()
    try:
        # url = 'https://www.kmart.com.au/product/incredible-but-true:-dinosaurs---book/2580336'
        # url = 'https://www.kmart.com.au/product/the-last-kids-on-earth-and-the-midnight-blade-by-max-brallier---book/3291323'
        driver.get(url)
        # details ={}




        rev = driver
        review = []
        while rev:

            review_id = rev.find_elements_by_class_name('yotpo-review')
            r_txt = rev.find_elements_by_class_name('content-review')
            for id,txts in zip(review_id,r_txt):
                id=id.get_attribute('data-review-id')
                text = txts.get_attribute('textContent')
                review.append({'submissionId': id
                          , 'text': text})
                # 'rating': rating,

            # rating = rev.find_element_by_class_name('sr-only')
            # rating = re.search(r'[\d]+.[\d]+', rating.get_attribute('textContent'))
            # print(id, rating.group(0))

            cont = rev.find_element_by_class_name('yotpo-reviews')
            cont = cont.find_element_by_class_name('yotpo-pager')
            lnk = cont.find_element_by_css_selector('.yotpo .yotpo-pager .yotpo-page-element.yotpo-icon-right-arrow')
            url = lnk.get_attribute('href')
            rev.get(str(url))

        # print(json.dumps(review, indent=4))



    except Exception as e:
        # print(review)
        if 'no such element' in str(e) :
            # traceback.print_tb(e.__traceback__)
            print(e)
        # check = not (bool(review))
        # print(check)
        # if check:
        #     rev = driver
        #     review = []
        #     while rev:
        #
        #         review_id = rev.find_elements_by_class_name('yotpo-review')
        #         r_txt = rev.find_elements_by_class_name('content-review')
        #         for id, txts in zip(review_id, r_txt):
        #             id = id.get_attribute('data-review-id')
        #             text = txts.get_attribute('textContent')
        #             review.append({'submissionId': id
        #                               , 'text': text})
        #             # 'rating': rating,
        #
        #         # rating = rev.find_element_by_class_name('sr-only')
        #         # rating = re.search(r'[\d]+.[\d]+', rating.get_attribute('textContent'))
        #         # print(id, rating.group(0))
        #
        #         cont = rev.find_element_by_class_name('yotpo-reviews')
        #         cont = cont.find_element_by_class_name('yotpo-pager')
        #         lnk = cont.find_element_by_css_selector('.yotpo .yotpo-pager .yotpo-page-element.yotpo-icon-right-arrow')
        #         url = lnk.get_attribute('href')
        #         rev.get(str(url))
        # else:
        #     rev =None
    finally:
        # pass
        print(review)
        return review
# scrap1('l','m')

# x = [1,2,3,4,5]
# y = [6,7,8,9,10]
#
# for i,j in zip(x,y):
#     print(i,j)
