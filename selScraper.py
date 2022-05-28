from lib2to3.pgen2.token import OP
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import json
import os

'''Takes the name of the 24 Hour Fitness Location, either AutoMall or Milpitas, and returns True if the 
price for that location dropped, False if it didn't, and none if the scraping method needs to be adjusted.'''
def check_price(name):
    #path on eel linux machine, change path if running on windows computer
    PATH = r"/root/24hr/chromedriverlinux"
    #necessary to run on linux server, if not then errors with might not have permission for PATH
    os.chmod(PATH, 755)
    #for linux machine where there's no gui for google
    options = Options()
    options.headless = True
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")

    service = Service(executable_path = PATH)
    driver = webdriver.Chrome(service=service, options=options )

    base_link = "https://www.24hourfitness.com/sales-redirect/salesredirect.html?type=sales&clubId="
    id_dict = {"AutoMall": "00493", "Milpitas": "00602"}
    id = id_dict[name]

    with open("price.txt", "r") as f:
        price_dict = json.loads(f.readline())
    
    driver.get(base_link + id)
    x_path = "/html/body/app-root/div/app-home/main/section/app-membership/div/app-membership-new-product-options/div/div/div[2]/div[2]/div/div/div[2]/app-membership-product/div/app-brand24-radio/div/div/span/label"
    
    try:
        target = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, x_path))
        )
        price = target.text.split()[0]
        print(price)
    except:
        return None
    finally:
        driver.quit()

    if float(price) < float(price_dict[name]):
        price_dict[name] = price
        with open("price.txt", "w") as f:
            f.write(json.dumps(price_dict))
        return True
    
    return False
