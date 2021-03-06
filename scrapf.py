import json
import re
import time
import traceback
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.request import urlopen


option = Options()
option.headless = True
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:83.0) Gecko/20100101 Firefox/83.0'}

def scrap_data(url):
    driver = webdriver.Chrome(options=option)
    details = {}
    try:
        print("scraping data",url)
        driver.get(url)
        page = driver.page_source
        # page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page,'html.parser')
        # print(soup.contents)

        pattern = re.compile("'ecommerce': .*?\}\);", re.DOTALL | re.MULTILINE)
        product_details = re.search(pattern, str(soup.contents))

        try:
            title = soup.find('h1', attrs={'class': 'pdp__productName'}).text.strip('\n')
            details["Product Name"] = title
        except:
            details["Product Name"] = "Not Available"


        try:
            code = re.search("'id': '(.+?)'", str(product_details.group())).group(1)
            details["code"] = [code]
            # print('code: ' + code)
            details["prodcode"] = [code]
            # print('prodcode: ' + code)
            details["varcode"] = [code]
        except:
            details["code"] = "Not Available"
            # print('code: ' + code)
            details["prodcode"] = "Not Available"
            # print('prodcode: ' + code)
            details["varcode"] ="Not Available"
        try:
            price = re.search("'price': '(.+?)'", str(product_details.group())).group(1)
            price = [float(price)]
            details["Price"] = price
        except:
            details['Price'] = "Not Available"
        cat = url.split('/')
        # print(url)
        details['category'] = cat[3]
        # print("category :",cat[3])
        details['subCategory'] = cat[-4]
        # print("subCategory :",cat[-4])
        try:
            in_stock = re.search("'stock level': '(.*?)'", str(product_details.group())).group(1)
            details["stock"] = int(in_stock)
        except:
            details["stock"] = "Not Available"

        details["URL"] = url
        details['deliveryMtd'] = " "
        details['shipFrom'] ="UK"
        details['shipTo'] = ["TW","HK", "JP","UAE","AU", "PH", "IN","MY","CN","UK","ID"]

        try:
            image_box = soup.find('div',class_='carousel-inner pdp-gallery__carousel')
            link = soup.find('div', attrs={'class': 'carousel-inner'})
            link = link.find_all('img')
            print(link)
            imagLink = ['https://www.superdrug.com' + src.get('src') for src in link]
            details['imgsURL'] = imagLink
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            details["Image URL"] = "Not Available"
            print(e)
        try:
            # Variant = re.search("'variant': '(.*?)'", str(product_details.group())).group(1)
            Variant = url.split('/')
            Variant = Variant[-3].split('-')
            Variants = "".join(Variant[-2:])
            # print(Variants)
            details["Variants"] = Variants
        except:
            details["Variants"] = "Null"
        try:
            Variant = url.split('/')
            Variant = Variant[-3].split('-')
            Variants = "".join(Variant[-2:])
            breadcrumb = soup.find('div', attrs={'id': 'breadcrumb'})
            breadcrumb =breadcrumb.findAll('a')
            breadCrumb =[]
            for i in breadcrumb:
                breadCrumb.append(i.text)
            details["breadcrumb"] = breadCrumb
        except Exception as e:
            traceback.print_tb(e.__traceback__)


        try:
            reviews_url = f'https://api.bazaarvoice.com/data/batch.json?passkey=i5l22ijc8h1i27z39g9iltwo3&apiversion=5.5&displaycode=10798-en_gb&resource.q0=products&filter.q0=id%3Aeq%3A{code}&stats.q0=questions%2Creviews&filteredstats.q0=questions%2Creviews&filter_questions.q0=contentlocale%3Aeq%3Aen_GB%2Cen_US&filter_answers.q0=contentlocale%3Aeq%3Aen_GB%2Cen_US&filter_reviews.q0=contentlocale%3Aeq%3Aen_GB%2Cen_US&filter_reviewcomments.q0=contentlocale%3Aeq%3Aen_GB%2Cen_US&resource.q1=reviews&filter.q1=isratingsonly%3Aeq%3Afalse&filter.q1=productid%3Aeq%3A{code}&filter.q1=contentlocale%3Aeq%3Aen_GB%2Cen_US&sort.q1=relevancy%3Aa1&stats.q1=reviews&filteredstats.q1=reviews&include.q1=authors%2Cproducts%2Ccomments&filter_reviews.q1=contentlocale%3Aeq%3Aen_GB%2Cen_US&filter_reviewcomments.q1=contentlocale%3Aeq%3Aen_GB%2Cen_US&filter_comments.q1=contentlocale%3Aeq%3Aen_GB%2Cen_US&limit.q1=2&offset.q1=0&limit_comments.q1=3&callback=bv_351_10687'
            reviews_text = requests.get(reviews_url, headers=headers).text
            reviews = re.search(r'\((.*?)\)$', reviews_text).group(1)
            reviews = json.loads(str(reviews))
        except:
            reviews = None
            pass
        if bool(reviews):
            try:
                Avgrating = reviews['BatchedResults']['q0']['Results'][0] \
                    ['FilteredReviewStatistics']['AverageOverallRating']
                details['rating'] = Avgrating
            except:
                details['rating'] = "Not Available"
            try:
                # print(reviews['BatchedResults']['q0']['Results'][0]['CategoryId'])
                details['catid'] = reviews['BatchedResults']['q0']['Results'][0]['CategoryId']
            except Exception as e:
                traceback.print_tb(e.__traceback__)
                details['catid'] = "Not Available"
                print('no catid', e)
        else:
            details['rating'] = "Not available"
            details['catid'] = "Nota available"
        try:
            description = soup.find('div', attrs={'id': 'pdp__details'})

            details['description'] = {}
            try:
                shortDes = description.find('p', attrs={'itemprop': 'description'}).text
                details['description']["shortDes"] = shortDes
            except:
                details['description']['shortDes'] = "Not Available"
            try:
                details['description']['imgsURL'] = imagLink
            except:
                details['description']['imgsURL'] = "Not Available"
            try:
                details['description']["detailDes"] = str(description)
            except:
                details['description']["detailDes"] = "Not Available"
                traceback.print_tb(e.__traceback__)
                print(e)

        except:
            details['description'] = "Not Available"
            print('Description Error')

        details['seller']={}
        details['seller']['name'] = ""
        details['seller']['URL'] = ""
        details['seller']['code'] = ""

        try:
            details['rootProductcode'] = [code]
            details["rootprice"] = price
        except:
            details['rootProductcode'] = "Not Available"
            details["rootprice"] = "Not Available"
        # details['rootoriginprice'] = org_price
        try:
            Currency = re.search("'currencyCode': '(.*?)'", str(product_details.group())).group(1)
            details["Currency"] = Currency
        except:
            details["Currency"] = "Not Available"
        # # print(json.dumps(details,indent=4))
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else", err)
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        print(e)
    print(json.dumps(details,indent=4))
    # print("Returning details")
    # with open('sduk.json','a') as f:
    #     f.write(',')
    #     f.write(json.dumps(details,indent=4))
    return details

# scrap_data('https://www.superdrug.com/Health/Allergy-%26-Hayfever/Cetirizine-Hayfever-Tablets/Superdrug-Allergy-%26-Hayfever-1-a-Day-Loratadine-Tablets-X-30/p/637200')
# url = "https://www.superdrug.com/Skin/Face-Skin-Care/Cleansers/Cleansing-Milks/Anne-French-Cleansing-Milk-200ml/p/26989"
# Variant = url.split('/')
# Variant = Variant[-3].split('-')
# Variants = "".join(Variant[-2:])
# print(Variants)

scrap_data('https://www.superdrug.com/Make-Up/Eye-Makeup/Eye-Shadow/Eye-Shadow-Palettes/Revolution-X-Friends-Open-The-Door-Shadow-Palette/p/800601')

#https://www.superdrug.com/Make-Up/Eye-Makeup/Eye-Shadow/Eye-Shadow-Palettes/Revolution-X-Friends-Open-The-Door-Shadow-Palette/p/800601
#https://www.superdrug.com/medias/sys_master/front-zoom/front-zoom/hea/h10/11354414678046/Revolution-X-Friends-Open-The-Door-Shadow-Palette-800601.jpg
#https://www.superdrug.com/medias/sys_master/ls1-zoom/ls1-zoom/h38/h38/11354515865630/Revolution-X-Friends-Open-The-Door-Shadow-Palette-800601.jpg
