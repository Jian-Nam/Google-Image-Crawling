
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.common import exceptions
import time
import urllib.request
import ssl
import os

class image_crawling:
    def __init__(self, keyword):
        self.searchbox_xpath =  '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/textarea'
        self.imgList_className = 'isv-r.PNCib.MSM1fd.BUooTd'
        self.imgUrl_xpath = '/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div[2]/div/div[2]/div[2]/div[2]/c-wiz/div/div[2]/div[1]/a/img[1]'
        self.keyword = keyword
        self.driver = self.set_chrome_driver()
        self.outpath = "./" + self.keyword + "/"

    def validate_SS_connection(self) :
        ssl._create_default_https_context = ssl._create_unverified_context

    def set_chrome_driver(self):
        chrome_options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        return driver

    def input_keyword(self):
        self.driver.get("https://www.google.co.kr/imghp?hl=ko&tab=wi&authuser=0&ogbl")

        searchbox = self.driver.find_element(By.XPATH, self.searchbox_xpath)
        searchbox.send_keys(self.keyword)
        searchbox.send_keys(Keys.RETURN)

    def make_output_dir(self):
        if not os.path.isdir(self.outpath): #폴더가 존재하지 않는다면 폴더 생성
            os.makedirs(self.outpath)
    

    def scroll_down_all(self):
        SCROLL_PAUSE_TIME = 1.5
        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)
            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                try:
                    self.driver.find_element(By.CLASS_NAME, "r0zKGf").click()
                    # driver.find_element(By.CLASS_NAME, "mye4qd").click()           
                except :
                    try:
                        self.driver.find_element(By.CLASS_NAME, "mye4qd").click() 
                    except:
                        self.driver.execute_script("window.scrollTo(0, 0);")
                        break
            last_height = new_height

    def crawl_img(self):
        image_elements = self.driver.find_elements(By.CLASS_NAME, self.imgList_className)

        count = 1
        for image_element in image_elements:
            try:
                image_element.click()
                time.sleep(2)

                opener = urllib.request.build_opener()
                opener.addheaders=[('User-Agent','Mozilla/5.0')]
                urllib.request.install_opener(opener)

                imgUrl = self.driver.find_element(By.XPATH, self.imgUrl_xpath).get_attribute("src")
                urllib.request.urlretrieve(imgUrl, self.outpath +  str(count) + ".jpg")
                count = count + 1
            except Exception as e:
                print(e)

    def crawl_img_test(self, img_index):
        try:
            image_elements = self.driver.find_elements(By.CLASS_NAME, self.imgList_className)
            image_elements[img_index].click()
            time.sleep(2)

            opener = urllib.request.build_opener()
            opener.addheaders=[('User-Agent','Mozilla/5.0')]
            urllib.request.install_opener(opener)

            imgUrl = self.driver.find_element(By.XPATH, self.imgUrl_xpath).get_attribute("src")
            urllib.request.urlretrieve(imgUrl, self.outpath +  "test" + str(img_index) + ".jpg")
        except Exception as e:
            print(e)

    def ready_crawling(self):
        self.validate_SS_connection()
        self.input_keyword()
        self.make_output_dir()


    def init_crawling(self):
        self.ready_crawling()
        self.scroll_down_all()
        self.crawl_img()
    
    def init_testing(self, img_index):
        self.ready_crawling()
        self.crawl_img_test(img_index)


    def __del__(self):
        self.driver.close()

keyword = input("KEYWORD: ")
i = image_crawling(keyword)
i.init_crawling()
# i.init_testing(0)