import re
import traceback

import requests
from bs4 import  BeautifulSoup
from selenium import webdriver
import time

options = webdriver.ChromeOptions()
# options.add_argument('--ignore-certificate-errors')
# options.add_argument('--incognito')
# options.add_argument('--headless')
driver = webdriver.Chrome()
# url = 'https://www.kmart.com.au/product/sodaking-windsor-soda-maker/3249331'
# driver.get(url)
# html = driver.find_element_by_class_name('title')
# print(html)

def scrap1():
    try:
        url = 'https://www.kmart.com.au/product/incredible-but-true:-dinosaurs---book/2580336'
        driver.get(url)
        details ={}
        # point = driver.find_element_by_id("panel-reviews")
        review_container = driver.find_element_by_class_name('yotpo-nav-content')
        # review_container = review_container.find_element("div['yotpo-reviews yotpo-active']")
        # review_container = review_container.find_element
        review_container = review_container.find_element_by_css_selector(".yotpo div")
        # review_container = review_container.find_element_by_css_selector('.yotpo .yotpo-regular-box')
        # for i,j in enumerate(review_container):
        #     print(i,j)
            # print(i.get_attribute('textContent'))
        r_txt = driver.find_elements_by_class_name('content-review')
        for i in r_txt:
            print(i.get_attribute('textContent'))
        review_id = driver.find_element_by_xpath('/html/body/div[11]/section[2]/div[1]/div/div[2]/div[2]/div/div[5]/div[3]/div[3]')
        id = review_id.get_attribute("data-review-id")

        rating = driver.find_element_by_class_name('sr-only')
        rating = re.search(r'[\d]+.[\d]+',rating.get_attribute('textContent'))
        print(id,rating.group(0))
        # review_txt = driver.find_element_by_xpath(
        #     '/html/body/div[11]/section[2]/div[1]/div/div[2]/div[2]/div/div[5]/div[3]/div[3]').get_attribute(
        #     "textContent")
        page_no = driver.find_element_by_class_name('yotpo-pager')
        next = page_no.find_element_by_xpath('/html/body/div[11]/section[2]/div[1]/div/div[2]/div[2]/div/div[5]/div[3]/div[5]/a[2]').click()
        r_txt = driver.find_elements_by_class_name('content-review')
        for i in r_txt:
            print(i.get_attribute('textContent'))
        # p_no = 0
        # for i in page_no:
        #     p_no = i.get_attribute('textContent')
        #     print(i)
        #     print(type(i.get_attribute('textContent')))
        # print(p_no)
        details['Reviews'] ={}
        details['Reviews']['id'] = id

        # print("befor script\n",point)
        # driver.execute_script("document.getElementsById ('panel-reviews') [0] .style.display = 'none';")
        # point = driver.find_element_by_id("panel-reviews").get_attribute(
        #     "textContent")
        # print("after script\n",point)
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        print(e)
    finally:
        driver.close()
scrap1()