from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd  
driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()))

def costco_scrape(item): 
    # element: id="search-field"  
    # image: id="productTileLink_0" 
    # href: <a href="https://www.costco.com/macbook-air-(13.3-inch)---apple-m1-chip-8-core-cpu%2c-7-core-gpu---8gb-memory---256gb-ssd-space-gray-(2020).product.100688258.html" automation-id="productDescriptionLink_0">
			# 	MacBook Air (13.3-inch) - Apple M1 Chip 8-core CPU, 7-core GPU - 8GB Memory - 256GB SSD Space Gray (2020)
			# </a> 
    # price: <div class="price" </div>
    # assign your website to scrape
    # <div class="product-tile-set" </div> 
    web = 'https://www.costco.com'
    driver.get(web)
    driver.implicitly_wait(5)
    keyword = item
    search = driver.find_element(By.ID, 'search-field')
    search.send_keys(keyword)
    # click search button
    # $(this).closest('.CatalogSearchForm').submit() 
    # search_button = driver.find_element(By.ID, 'co-search-thin')
    search_button = driver.find_element(By.CSS_SELECTOR, '.search-ico-button [automation-id="searchWidgetButton"]')
    search_button.click()

    driver.implicitly_wait(5)

    product_asin = []
    product_name = []
    product_price = []
    product_ratings = []
    product_ratings_num = []
    product_link = []
    product_image = [] 

    items = wait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "product-tile-set")]')))
    count = 0 
    print(items[0].text)
    # convert items to list 
    # for item in items:
    #     name_element = item.find_element(By.CSS_SELECTOR, '.search-ico-button [automation-id="searchWidgetButton"]')
    #     name = name_element.text
    #     # automation-id="productDescriptionLink_0" 
    #     product_name.append(name)
    # print(product_name) 
    driver.quit() 


if __name__ == '__main__':
    costco_scrape('macbook air') 

