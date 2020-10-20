#!/usr/bin python3
# -*- coding: utf-8 -*-

'''

# Это файл парсинга цены товара с Citilink


'''



import requests
from bs4 import BeautifulSoup

from user_agent import generate_user_agent, generate_navigator

import json
from pprint import pprint

import configparser



class Citilink:


    # SITE_URL = "https://www.citilink.ru/catalog/mobile/cell_phones/1178761/"
    # SITE_URL = "https://www.citilink.ru/catalog/mobile/tablet_pc/1210847/"
    #
    # SITE_URL = "https://www.citilink.ru/catalog/mobile/tablet_pc/1092203/"



    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.headers = {
            'User-Agent': generate_user_agent(),  # ua.random,
            'From': self.config['CITILINK']['header_from']  # This is another valid field
        }
        self.cookies = {
            '_space': "uln_cl%3A", # self.config['CITILINK']['cookie_space']  #,
            '_csh': str(self.config['CITILINK']['cookie_csh'])  #,
        }


    # GET REQUESTS
    def get_html_page(self, url):
        try:
            r = requests.get(url, headers=self.headers, cookies=self.cookies)
            r.raise_for_status()
            # with open('citilink.txt', 'w') as f:
            #     f.write((r.content).decode("utf-8"))
            return r.content
        except requests.exceptions.HTTPError as errh:
            print("[send_post_req_on_server] CITILINK Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("[send_post_req_on_server] CITILINK Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("[send_post_req_on_server] CITILINK Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print("[send_post_req_on_server] CITILINK OOps: Something Else", err)



    # Parse Site Code
    def get_parser_result(self, url):
        soup = BeautifulSoup(self.get_html_page(url), 'html.parser')
        need_block = soup.find("script", type="application/ld+json")
        all_response_here = need_block.contents
        all_response_to_json = json.loads(all_response_here[0])

        return_array = {
            # "rating_value" : all_response_to_json['aggregateRating']['ratingValue'],
            # "rating_count" : all_response_to_json['aggregateRating']['reviewCount'],
            "brand" : all_response_to_json['brand'],
            "description" : all_response_to_json['description'],
            "image" : all_response_to_json['image'],
            "name" : all_response_to_json['name'],
            "offers_url" : all_response_to_json['offers']['url'],
            "offers_price" : all_response_to_json['offers']['price'],
            "availability": all_response_to_json['offers']['availability']
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



# citilink = Citilink()

# # Main
# def main():
#     get_parser_result(SITE_URL)

# if __name__ == '__main__':
#     main()