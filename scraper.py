import re
import time
import traceback

from bs4 import BeautifulSoup
import  requests
from selenium.webdriver import Chrome
import json


headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:83.0) Gecko/20100101 Firefox/83.0'}


# driver.get('https://www.kmart.com.au/')
# data=driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div/div[3]/div[2]/div')
# data = driver.find_element_by_tag_name('a')
# data = data.find_elements_by_tag_name('a')
def scrap():
        driver = Chrome()
        time.sleep(3)
        try:
                data = ['https://www.kmart.com.au/category/home-&-living/home-by-category/home-&-living-latest-arrivals/427501',
                        'https://www.kmart.com.au/category/women/features/womens-latest-arrivals/459002',
                        'https://www.kmart.com.au/category/kids-&-baby/kids-clothing/kidswear-latest-arrivals/513027',
                        'https://www.kmart.com.au/category/men/features/menswear-latest-arrivals/513029#.plp-wrapper',
                        'https://www.kmart.com.au/category/electronics/electronics-by-category/electronics-latest-arrivals/462007',
                        'https://www.kmart.com.au/category/toys/features/toys-latest-arrivals/467503',
                        'https://www.kmart.com.au/category/latest-arrivals/latest-arrivals-by-category/sports-&-outdoor-latest-arrivals/464538#.plp-wrapper',
                        'https://www.kmart.com.au/category/latest-arrivals/latest-arrivals-by-category/books-latest-arrivals/505531#.plp-wrapper'
                        ]
                # for i in data:
                    # print(i.get_attribute('href'))
                    # driver.get(i)
                details = {}

                # url = 'https://www.kmart.com.au/product/cocoon-chair/3273813'
                # url = 'https://www.kmart.com.au/product/sodaking-windsor-soda-maker/3249331'
                # url = 'https://www.kmart.com.au/product/sharks-(inside-out):-look-inside-a-great-white-in-three-dimensions!-by-david-george-gordon---book/3073313'
                url = 'https://www.kmart.com.au/product/incredible-but-true:-dinosaurs---book/2580336'
                driver.get(url)


                title = driver.find_element_by_class_name('title')
                # print(title.text)
                details['Product Name'] = title.text
                # sku = driver.find_element_by_class_name('right-side-description')
                # sku = sku.find_elements_by_tag_name('h7')
                # for i in sku:
                #         sku = i.text
                #         # print(sku)
                # details['sku'] = sku
                code = url.split('/')[-1]
                details['code'] = code
                price = driver.find_element_by_class_name('price')
                price = re.search(r'[\d]*\.[\d]*',price.text).group(0)
                # orgprice = driver.find_element_by_class_name('price')
                # orgprice = orgprice.find_elements_by_tag_name('h4')
                # for i in orgprice:
                #         print(i)
                # orgprice = re.search(r'[a-z]*[\d]+\.[\d]*',orgprice.text)
                # print(orgprice)
                # details['Price'] = price

                # breadcrumb =[]
                breadcrumb = driver.find_element_by_class_name('breadcrumbs')
                breadcrumb = breadcrumb.text.split('\n')
                # print(breadcrumb)
                details['breadcrumb'] = breadcrumb
                img = driver.find_element_by_class_name('owl-stage-outer')
                # img = driver.find_element_by_class_name('owl-stage-outer')
                img = img.find_elements_by_tag_name('img')
                img_link = []
                for i in img:
                        img_link.append(i.get_attribute('src'))
                        # print(i.get_attribute('src'))
                details['Img_URL'] = img_link
                prodDetail = driver.find_element_by_class_name('tab-panel') #product-details-desc
                prodDetail = prodDetail.get_attribute('innerHTML')
                details['prodDescription'] = {}
                details['prodDescription']['imgurl'] = img_link
                details['prodDescription']['detailDes'] = prodDetail
                details['rootPrice'] = price
                details['rootProdcode'] = code
                code = 'P_42938194'

                # review = requests.get(rev_url,headers=headers).text
                review = driver.find_element_by_xpath('/html/body/div[11]/section[2]/div[1]/div/div[2]/div[2]')
                print('review:-',review.text)
                # details['review'] = review
                # Variant = url.split('/')
                # Variant = Variant[-3].split('-')
                # Variants = "".join(Variant[-2:])
                # details['variants'] = Variants


                # print(json.dumps(details,indent=4))

                # print(details)
        except Exception as e :
                traceback.print_tb(e.__traceback__)
                print(e)
        finally:
                driver.close()
                # pass
scrap()

# orgprice = '$27.00 RRP $69.95'
# orgprice = re.search(r'[RRP][$][\d]+\.[\d]*',orgprice)
# print(orgprice)

# html = BeautifulSoup(page.text,'html.parser')
# print(html)
# page = BeautifulSoup