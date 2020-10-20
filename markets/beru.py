#!/usr/bin python3
# -*- coding: utf-8 -*-

'''

# Это файл парсинга цены товара с BERU


'''



import requests
from bs4 import BeautifulSoup

from user_agent import generate_user_agent, generate_navigator

import time
import random
import json

from subprocess import Popen, PIPE
from pprint import pprint

import configparser



class Beru:


    # SITE_URL = "https://beru.ru/product/planshet-apple-ipad-2019-32gb-wi-fi-silver/100774721748"
    # SITE_URL = "https://beru.ru/product/smartfon-apple-iphone-11-64gb-belyi-mwlu2ru-a/100773347843"
    #
    # SITE_URL = "https://beru.ru/product/besprovodnye-naushniki-jbl-reflect-flow-chernyi/100764493807"
        


    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')



    def sleeper(self):
        # Beru блокирует частые попытки подключения, поэтому делаем таймауты
        sleep_time = random.randint(int(self.config['BERU']['sleep_time_to']), int(self.config['BERU']['sleep_time_from']))
        print("Beru response sleep " + str(sleep_time) + " seconds")
        time.sleep(sleep_time)



    # GET REQUESTS
    def get_html_page(self, url):
        try:
            self.sleeper()

            # По какой - то причине не работает запрос request, сделал через curl
            p = Popen('curl '+ url, shell=True, stdout=PIPE, stderr=PIPE)
            output, _error = p.communicate()

            # r = requests.get(url, headers=headers, cookies=cookies)
            # r.raise_for_status()

            # with open('beru.txt', 'w') as f:
            #     f.write(output.decode("utf-8"))

            return output

        except requests.exceptions.HTTPError as errh:
            print("[send_get_req_on_server] BERU Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("[send_get_req_on_server] BERU Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("[send_get_req_on_server] BERU Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print("[send_get_req_on_server] BERU OOps: Something Else", err)



    # Parse Site Code
    def get_parser_result(self, url):
        try:
            soup = BeautifulSoup(self.get_html_page(url), 'html.parser')
            need_block = soup.find("div", attrs={'data-zone-name' : "SkuWishlist"})["data-zone-data"]
            # json_d = '{"productId":558171067,"name":"Смартфон Apple iPhone 11 64GB белый (MWLU2RU/A)","isExpired":false,"rate":4.5,"skuId":"100773347843","hid":91491,"slug":"smartfon-apple-iphone-11-64gb-belyi-mwlu2ru-a","marketSkuCreator":"market","responses":206,"price":58890}'
            all_response_to_json = json.loads(need_block)
            # print(all_response_to_json)

            if all_response_to_json['isExpired'] == True:
                availability = 'OutOfStock'
                price = 0
            else:
                availability = 'InStock'
                price = all_response_to_json['price']

            return_array = {
                "rating_value" : all_response_to_json['rate'],
                "rating_count" : all_response_to_json['responses'],
                "brand" : "",
                "description" : "",
                "image" : "",
                "name" : all_response_to_json['name'],
                "offers_url" : self.config['BERU']['beru_url'] + "product/" + all_response_to_json['slug'] + "/" + all_response_to_json['skuId'],
                "offers_price" : price,
                "availability": availability
            }

            # pprint(return_array)

            return_short = {
                "name" : return_array['name'],
                "offers_url" : return_array['offers_url'],
                "offers_price" : return_array['offers_price'],
                "availability" : return_array['availability']
            }

            return return_short

        except :
            print("Ошибка. Пустой результат. Вероятно Беру определило скрипт как бота...")



    # Main
    # def __init__(self):
    #     self.get_parser_result(self.SITE_URL)



# beru = Beru()

# Main
# def main():
#     get_parser_result(SITE_URL)

# if __name__ == '__main__':
#     main()