# Importing libraries
import time
import random
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
pd.options.mode.chained_assignment = None
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


# Function to delay some process
def delay():
    time.sleep(random.randint(3, 10))


# Scrolling down the page in order to overcome Lazy Loading
def lazy_loading():
    element = driver.find_element(By.XPATH,'/html/body')
    count = 0
    while count < 20:
        element.send_keys(Keys.PAGE_DOWN)
        delay()
        count += 1


# Clicking the button to go to next page
def pagination():
    try:
        driver.find_element(By.XPATH, "//li[@class='a-last']/a").click()
        delay()

    except:
        pass


# Function to fetch the product links of products
def fetch_product_links_and_ranks():
    content = driver.page_source
    homepage_soup = BeautifulSoup(content, 'html.parser')

    all_products = homepage_soup.find('div', attrs={"class": "p13n-desktop-grid"})
    for product_section in all_products.find_all('div', {'id': 'gridItemRoot'}):
        for product_link in product_section.find_all('a',{'tabindex':'-1'}):
            if product_link['href'].startswith('https:'):
                product_links.append(product_link['href'])
            else:
                product_links.append('https://www.amazon.com' + product_link['href'])
        ranking.append(product_section.find('span',{'class': 'zg-bdg-text'}).text)


# Function to extract content of the page
def extract_content(url):
    driver.get(url)
    page_content = driver.page_source
    product_soup = BeautifulSoup(page_content, 'html.parser')
    return product_soup


# Function to extract product name
def extract_product_name(soup):
    try:
        name_of_product = soup.find('div', attrs={"id": "titleSection"}).text.strip()
        data['product name'].iloc[product] = name_of_product

    except:
        name_of_product = 'Product name not available '
        data['product name'].iloc[product] = name_of_product


# Function to extract brand name
def extract_brand(soup):
    try:
        brand = soup.find('a', attrs={"id": "bylineInfo"}).text.split(':')[1].strip()  #one location where brand data could be found
        data['brand'].iloc[product] = brand

    except:
        if soup.find_all('tr', attrs={'class': 'a-spacing-small po-brand'}):  #other location where brand data could be found
            brand = soup.find_all('tr', attrs={'class': 'a-spacing-small po-brand'})[0].text.strip().split(' ')[-1]
            data['brand'].iloc[product] = brand
        else:
            brand = 'Brand data not available'
            data['brand'].iloc[product] = brand


# Function to extract price
def extract_price(soup):
    try:
        price = soup.find('span', attrs={"class": "a-price a-text-price a-size-medium apexPriceToPay"}).text.split('$')[
            -1]
        data['price(in dollar)'].iloc[product] = price

    except:
        price = 'Price data not available'
        data['price(in dollar)'].iloc[product] = price


# Function to extract size
def extract_size(soup):
    try:
        size = soup.find('span', attrs={"id": "inline-twister-expanded-dimension-text-size_name"}).text.strip()
        data['size'].iloc[product] = size

    except:
        size = 'Size data not available'
        data['size'].iloc[product] = size


# Function to extract star rating
def extract_star_rating(soup):
    try:
        star = None
        for star_rating_locations in ['a-icon a-icon-star a-star-4-5', 'a-icon a-icon-star a-star-5']:
            stars = soup.find_all('i', attrs={"class": star_rating_locations})
            for i in range(len(stars)):
                star = stars[i].text.split(' ')[0]
                if star:
                    break
            if star:
                break
        
    except:
        star = 'Star rating data not available'
        
    data['star rating'].iloc[product] = star   


# Function to extract number of ratings
def extract_num_of_ratings(soup):
    try:
        star = soup.find('span', attrs={"id": "acrCustomerReviewText"}).text.split(' ')[0]
        data['number of ratings'].iloc[product] = star

    except:
        star = 'Number of rating not available'
        data['number of ratings'].iloc[product] = star


# Function to extract color
def extract_color(soup):
    try:
        color = soup.find('tr', attrs={'class': 'a-spacing-small po-color'}).text.strip().split('  ')[1].strip()
        data['color'].iloc[product] = color

    except:
        color = 'Color not available'
        data['color'].iloc[product] = color


# Function to extract hardware interface
def extract_hardware_interface(soup):
    try:
        hardware_interface = \
        soup.find('tr', attrs={"class": "a-spacing-small po-hardware_interface"}).text.strip().split('  ')[1].strip()
        data['hardware interface'].iloc[product] = hardware_interface

    except:
        hardware_interface = 'Hardware interface data not available'
        data['hardware interface'].iloc[product] = hardware_interface


# Function to extract compatible devices
def extract_compatible_devices(soup):
    try:
        compatible_devices = \
        soup.find('tr', attrs={"class": "a-spacing-small po-compatible_devices"}).text.strip().split('  ')[1].strip()
        data['compatible devices'].iloc[product] = compatible_devices

    except:
        compatible_devices = 'Compatible devices data not available'
        data['compatible devices'].iloc[product] = compatible_devices


# Function to extract data transfer rate
def extract_data_transfer_rate(soup):
    try:
        data_transfer_rate = \
        soup.find('tr', attrs={"class": "a-spacing-small po-data_transfer_rate"}).text.strip().split('  ')[1].strip()
        data['data transfer rate'].iloc[product] = data_transfer_rate

    except:
        data_transfer_rate = 'Data transfer rate data not available'
        data['data transfer rate'].iloc[product] = data_transfer_rate


# Function to extract mounting type
def extract_mounting_type(soup):
    try:
        mounting_type = soup.find('tr', attrs={"class": "a-spacing-small po-mounting_type"}).text.strip().split('  ')[
            1].strip()
        data['mounting type'].iloc[product] = mounting_type

    except:
        mounting_type = 'Mounting type data not available'
        data['mounting type'].iloc[product] = mounting_type


# Function to extract special features
def extract_special_features(soup):
    try:
        special_feature = \
        soup.find('tr', attrs={"class": "a-spacing-small po-special_feature"}).text.strip().split('  ')[1].strip()
        data['special features'].iloc[product] = special_feature

    except:
        special_feature = 'Special features data not available'
        data['special features'].iloc[product] = special_feature


# Function to extract connectivity technology
def extract_connectivity_technology(soup):
    try:
        connectivity_technology = \
        soup.find('tr', attrs={"class": "a-spacing-small po-connectivity_technology"}).text.strip().split('  ')[
            1].strip()
        data['connectivity technology'].iloc[product] = connectivity_technology

    except:
        connectivity_technology = 'Connectivity technology data not available'
        data['connectivity technology'].iloc[product] = connectivity_technology


# Function to extract connector type
def extract_connector_type(soup):
    try:
        connector_type = soup.find('tr', attrs={"class": "a-spacing-small po-connector_type"}).text.strip().split('  ')[
            1].strip()
        data['connector type'].iloc[product] = connector_type

    except:
        connector_type = 'Connector type data not available'
        data['connector type'].iloc[product] = connector_type


# Function to extract date first available
def extract_date_first_available(soup):
    try:
        product_details_keys = soup.find_all('th', attrs={"class": "a-color-secondary a-size-base prodDetSectionEntry"})
        product_details_values = soup.find_all('td', attrs={"class": "a-size-base prodDetAttrValue"})
        for detail_key in range(len(product_details_keys)):
            if 'Date First Available' in product_details_keys[detail_key].text:
                date_first_available = product_details_values[detail_key - 2].text
                if '20' not in date_first_available:
                    date_first_available = product_details_values[detail_key].text
        data['date first available'].iloc[product] = date_first_available

    except:
        date_first_available = 'Date first available data not available'
        data['date first available'].iloc[product] = date_first_available


# Amazon Best Sellers website link
start_url ='https://www.amazon.com/Best-Sellers-Computers-Accessories/zgbs/pc/ref=zg_bs_pg_1?_encoding=UTF8&pg=1'
driver.get(start_url)


# Fetching the product links of all items
product_links = []
ranking=[]
lazy_loading()
fetch_product_links_and_ranks()        # fetching links from first page
pagination()                           # going to second page
lazy_loading()
fetch_product_links_and_ranks()        # fetching links from second page


# Creating a dictionary of the required columns
data_dic = {'product url': [],'ranking': [], 'brand': [], 'product name': [],
            'number of ratings': [], 'size': [], 'star rating': [], 'price(in dollar)': [], 'color': [],
            'hardware interface': [], 'compatible devices': [], 'connectivity technology': [], 'connector type': [], 'data transfer rate':[], 'mounting type': [], 'special features':[], 'date first available':[]}


# Creating a dataframe with those columns
data = pd.DataFrame(data_dic)


# Assigning the scraped links and rankings to the columns 'product url' and 'ranking'
data['product url'] = product_links
data['ranking'] = ranking

for product in range(len(data)):
    product_url = data['product url'].iloc[product]
    product_content = extract_content(product_url)

    # brands
    extract_brand(product_content)

    # product_name
    extract_product_name(product_content)

    # price
    extract_price(product_content)

    # size
    extract_size(product_content)

    # star rating
    extract_star_rating(product_content)

    # number of ratings
    extract_num_of_ratings(product_content)

    # color
    extract_color(product_content)

    # hardware interface
    extract_hardware_interface(product_content)

    # compatible devices
    extract_compatible_devices(product_content)

    # data transfer rate
    extract_data_transfer_rate(product_content)

    # mounting type
    extract_mounting_type(product_content)

    # special features
    extract_special_features(product_content)

    # connectivity technology
    extract_connectivity_technology(product_content)

    # connector type
    extract_connector_type(product_content)

    # date first available
    extract_date_first_available(product_content)


# saving the resultant dataframe as a csv file
data.to_csv('amazon_best_sellers.csv')
