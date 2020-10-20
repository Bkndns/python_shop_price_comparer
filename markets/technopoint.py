#!/usr/bin python3
# -*- coding: utf-8 -*-

'''

# Это файл парсинга цены товара с DNS Technopoint, парсит через Selenium


'''



from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

import time
from pprint import pprint

import configparser



class Technopoint:


    # SITE_URL = "https://technopoint.ru/product/900e8d77d4411b80/102-planset-apple-ipad-2019-32-gb--zolotistyj-sale/"
    # SITE_URL = "https://technopoint.ru/product/1582885194dc1b80/133-noutbuk-apple-macbook-pro-retina-tb-mxk62rua-serebristyj-sale/"
    #
    # SITE_URL = "https://technopoint.ru/product/7734c2fe94df1b80/133-noutbuk-apple-macbook-pro-retina-tb-mxk72rua-serebristyj-sale/"



    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

    

    def get_parser_result(self, url):

        op = webdriver.FirefoxOptions()
        op.add_argument('--headless')

        driver = webdriver.Firefox(options=op, executable_path='/home/bkndns/Selenium/geckodriver')
        driver.get(url)

        time.sleep(int(self.config['DNS']['sleep_time']))
        driver.implicitly_wait(int(self.config['DNS']['wait_time']))

        #
        try:
            price = driver.find_element_by_xpath("//div[@id='product-page']/div[3]/div[2]/div/div[3]/div/div/div/div/div[2]/span").text
        except NoSuchElementException:
            try:
                price = driver.find_element_by_xpath("//div[@id='product-page']/div[4]/div[2]/div/div[3]/div/div/div/div/div[2]/span").text
            except:
                price = ""

        name = driver.find_element_by_xpath("//div[@id='product-page']/h1").text

        try:
            # NOT IN STOCK
            availability = driver.find_element_by_css_selector("html body.stay-at-home div.container div#product-page div.price-item.ec-price-item div.node-block div.item-header div.col-header.col-order div.clearfix div.rating-block-wrap div.hidden-xs.hidden-sm div.order-avail-wrap span.avail-text.no-avails").text
        except NoSuchElementException:
            # IN STOCK
            availability = "InStock"


        # try:
        #     rating_count = driver.find_element_by_xpath("//div[@id='product-page']/div[3]/div[2]/div/div[3]/div/div[2]/div[2]/div/span").text
        # except NoSuchElementException:
        #     rating_count = ""

        # try:
        #     review_value = driver.find_element_by_xpath("//div[@id='product-page']/div[3]/div[2]/div/div[3]/div/div[2]/div[2]/div/span[3]").text
        # except NoSuchElementException:
        #     review_value = ""
        
        try:
            _image = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[3]/div[2]/div/div[2]/div/div[1]/div/div[1]/div/div[1]/div/a/img")
        except NoSuchElementException:
            _image = ""
        #


        #
        price = price.replace(" ", "")[:-1]

        all_response_to_json = {}
        all_response_to_json['price'] = price
        all_response_to_json['name'] = name
        all_response_to_json['availability'] = availability
        
        # all_response_to_json['image'] = image.get_attribute("src")
        all_response_to_json['rating_count'] = "" #rating_count
        all_response_to_json['review_value'] = "" #review_value

        #
        driver.close()

        return_array = {
            "rating_value" : all_response_to_json['rating_count'],
            "rating_count" : all_response_to_json['review_value'],
            "brand" : "",
            "description" : "",
            "image" : "", #all_response_to_json['image'],
            "name" : all_response_to_json['name'],
            "offers_url" : url,
            "offers_price" : all_response_to_json['price'],
            "availability" : availability
        }

        # pprint(return_array)

        return_short = {
            "name" : return_array['name'],
            "offers_url" : return_array['offers_url'],
            "offers_price" : return_array['offers_price'],
            "availability" : return_array['availability']
        }

        return return_short


    # Main
    # def __init__(self):
    #     self.get_parser_result(self.SITE_URL)



# technopoint = Technopoint()

# Main
# def main():
#     get_parser_result(SITE_URL)

# if __name__ == '__main__':
#     main()