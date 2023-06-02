from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd  
driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()))



def amazon_scrape(item):
    # assign your website to scrape
    web = 'https://www.amazon.com'
    driver.get(web)
    driver.implicitly_wait(5)
    keyword = item
    search = driver.find_element(By.ID, 'twotabsearchtextbox')
    search.send_keys(keyword)
    # click search button
    search_button = driver.find_element(By.ID, 'nav-search-submit-button')
    search_button.click()

    driver.implicitly_wait(5)

    product_asin = []
    product_name = []
    product_price = []
    product_ratings = []
    product_ratings_num = []
    product_link = []
    product_image = [] 

    items = wait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "s-result-item s-asin")]')))
    for item in items:
        # find name
        # name = item.find_element(By.XPATH, './/span[@class="a-size-medium a-color-base a-text-normal"]')
        # name = item.find_element(By.XPATH, ".//span[contains(@class, 'a-size-medium') and contains(@class, 'a-color-base') and contains(@class, 'a-text-normal')]").text
        name_element = item.find_element(By.XPATH, ".//a[contains(@class, 'a-link-normal') and contains(@class, 's-underline-text') and contains(@class, 's-underline-link-text') and contains(@class, 's-link-style') and contains(@class, 'a-text-normal')]")
        name = name_element.text
        product_name.append(name)

        # find ASIN number 
        data_asin = item.get_attribute("data-asin")
        product_asin.append(data_asin)

        # find price
        whole_price = item.find_elements(By.XPATH, './/span[@class="a-price-whole"]')
        fraction_price = item.find_elements(By.XPATH, './/span[@class="a-price-fraction"]')
        
        if whole_price != [] and fraction_price != []:
            price = '.'.join([whole_price[0].text, fraction_price[0].text])
        else:
            price = 0
        product_price.append(price)

        # find ratings box
        ratings_box = item.find_elements(By.XPATH, './/div[@class="a-row a-size-small"]/span')

        # find ratings and ratings_num
        if ratings_box != []:
            ratings = ratings_box[0].get_attribute('aria-label')
            ratings_num = ratings_box[1].get_attribute('aria-label')
        else:
            ratings, ratings_num = 0, 0
        
        product_ratings.append(ratings)
        product_ratings_num.append(str(ratings_num))

        # find image link 
        image = item.find_element(By.XPATH, './/img[@class="s-image"]')
        image_link = image.get_attribute("src") 
        product_image.append(image_link)
        
        # # find link
        # a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal 
        # link = item.find_element(By.XPATH, '//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[17]/div/div/span/div/div/div/div/div[2]/div/div/div/div[3]/div/div[2]/a').get_attribute("href")
        link = item.find_element(By.XPATH, './/a[@class="a-link-normal s-no-outline"]').get_attribute("href")
 
        product_link.append(link)
        # look for the HERF link, then replace it with the xpath via find: a-link-normal a-text-normal"  
        # //*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[17]/div/div/span/div/div/div/div/div[2]/div/div/div/div[3]/div/div[2]/a 
    driver.quit()

    # to check data scraped
    print(product_name)
    print(product_asin)
    print(product_price)
    print(product_ratings)
    print(product_ratings_num)
    print(product_link)
    print(product_image)

    # check length of each list 
    print("product_name: ", len(product_name))
    print("product_asin: ", len(product_asin))
    print("product_price: ", len(product_price))
    print("product_ratings: ", len(product_ratings))
    print("product_ratings_num: ", len(product_ratings_num))
    print("product_link: ", len(product_link))
    print("product_image: ", len(product_image))

    # export to csv 
    # remove space in keyword 
    keyword = keyword.replace(' ', '_') 
    csv_name = keyword + '.csv'
    df = pd.DataFrame({'product_name': product_name, 'product_asin': product_asin, 'product_price': product_price, 'product_ratings': product_ratings, 'product_ratings_num': product_ratings_num, 'product_link': product_link, 'product_image': product_image})
    df.to_csv(csv_name, index=False, encoding='utf-8')

    ## twotabsearchtextbox 

    ## class="a-size-medium a-color-base a-text-normal"

    # s-result-item s-widget s-widget-spacing-large AdHolder s-flex-full-width

if __name__ == '__main__':
    amazon_scrape('make up tool') 

    # a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal