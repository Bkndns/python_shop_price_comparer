#!/usr/bin python3
# -*- coding: utf-8 -*-

'''

# Это файл парсинга цен с разных источников с целью отслеживания

+ для начала объеденить все классы магазинов в один неймспейс и импорт сделать их классами
+ далее в файле маин забирать цены по товару сразу со всех магазинов
+ возможность передать в функции парсинга магазина ссылку не хардкодом
+ получив цену всех магазинов ее можно записать, массив этот перебрать и вывести где дешевле товар
+ далее сделать конфигуратор и отрефакторить хардкод

+ создать БД которая описывает товар и ссылки с ценами вот пример схемы:
+ [id, item_name, ozon_token, min_price, ozon_link, citilink_link, beru_link, dns_link, ozon_price_start, citilink_price_start, beru_price_start, dns_price_start, ozon_price_now, citilink_price_now, beru_price_now, dns_price_now, create_at, update_at]
- БД хранит цену первого парсинга и цену сейчас, на основе этого можно выводить повысилась или понизилась цена, сделать такую функцию

- теперь чат бот телеграм
    - первый вход что мы видим?
    - три кнопки - посмотреть отслеживаемые товары, добавить товар, удалить товар
    
    - в списке отслеживаемых товаров, по нажатию на товар, можно посмотреть информацию по товару, имя, ссылку, старую цену, новую цену, стрелку повыш/пониж, и на сколько пониз/повыс, а также дату синхронизации
    - также у одиночного товара есть кнопки - Синхронизировать сейчас и Удалить этот товар

    - добавление товара
    - запрашивает имя, запрашивает ссылки по очереди, можно запрашивать мин прайс для отслеживания

    - удаление товара
    - выводит список всех товаров, по нажатию на товар он удаляется с запросом


'''



import configparser

from markets import *
import database


# ССЫЛКИ НА ПЛАНШЕТ IPAD
# DNS_URL = "https://technopoint.ru/product/900e8d77d4411b80/102-planset-apple-ipad-2019-32-gb--zolotistyj-sale/"
# OZON_URL = "https://www.ozon.ru/context/detail/id/160020615/"
# BERU_URL = "https://beru.ru/product/planshet-apple-ipad-2019-32gb-wi-fi-silver/100774721748"
# CITILINK_URL = "https://www.citilink.ru/catalog/mobile/tablet_pc/1179782/"      

# ССЫЛКИ НА ПАРООЧИСТИТЕЛЬ
# DNS_URL = "https://technopoint.ru/product/8954c13119623332/paroocistitel-karcher-sc-2-de-luxe-zeltyj-sale/"
# OZON_URL = "https://www.ozon.ru/context/detail/id/150288308/"
# BERU_URL = "https://beru.ru/product/paroochistitel-karcher-sc-2-deluxe-easyfix/100565630777"
# CITILINK_URL = "https://www.citilink.ru/catalog/large_and_small_appliances/home_appliances/steam_cleaners/1182456/"

# ССЫЛКИ НА BLUETOOTH JBL КОЛОНКУ
DNS_URL = "https://technopoint.ru/product/549cb868ba3a3330/portativnaa-kolonka-jbl-charge-4-sinij-sale/"
OZON_URL = "https://www.ozon.ru/context/detail/id/149033570/"
BERU_URL = "https://beru.ru/product/portativnaia-akustika-jbl-charge-4-blue/100508525212"
CITILINK_URL = "https://www.citilink.ru/catalog/mobile/cell_phones_aks/portativnye_kolonki/1118131/"

#
ITEM_NAME = "Беспроводная колонка JBL"
ITEM_MIN_PRICE = 7000



# Main
def main():

    # DATABASE INIT
    config = configparser.ConfigParser()
    config.read('config.ini')

    sql = database.SQLer()
    conn = sql.create_connection(config['DATABASE']['DBNAME'])
    # DATABASE INIT



    # Первый запуск парсера - нужны цены.
    check_items = sql.select_data_by_ozon_link(conn, OZON_URL)

    if check_items != 0:
        # Если такая запись уже есть, то обновим цены
        ozon_price = check_items[8]
        item_id = check_items[0]
        # 1 - запись добавлена без цен, добавим цены
        if ozon_price == None:
            print("[DEBUG] - OZON PRICE NONE")
            parse_all_prices = start_parsing_all_markets(check_items) 
            data = (
                # эти поля не трогаем
                check_items[3],
                check_items[4],
                check_items[5],
                check_items[6],
                check_items[7],
                # Устанавливаем эти цены
                parse_all_prices['ozon'],
                parse_all_prices['citilink'], 
                parse_all_prices['beru'], 
                parse_all_prices['dns'], 
                # И эти цены
                parse_all_prices['ozon'],
                parse_all_prices['citilink'], 
                parse_all_prices['beru'], 
                parse_all_prices['dns'],

                item_id
            )
            sql.update_data(conn, data)

        else:
            print("[DEBUG] - OZON PRICE YES UPDATE PRICE NOW")
            # 2 - у записи есть старые цены парсим новые
            parse_all_prices = start_parsing_all_markets(check_items) 
            data = (
                # эти поля не трогаем
                check_items[3],
                check_items[4],
                check_items[5],
                check_items[6],
                check_items[7],
                # эти цены не трогаем
                check_items[8],
                check_items[9], 
                check_items[10], 
                check_items[11], 
                # эти цены устранавливаем
                parse_all_prices['ozon'],
                parse_all_prices['citilink'], 
                parse_all_prices['beru'], 
                parse_all_prices['dns'],

                item_id
            )
            sql.update_data(conn, data)
    else:
        print("[DEBUG] - THIS ITEM HAVE NO BEEN ADDED")
        # Такой записи нет совсем. Запускаем функцию добавления
        data = (ITEM_NAME, 
                ITEM_MIN_PRICE, 
                OZON_URL, CITILINK_URL, BERU_URL, DNS_URL)
        sql.create_item(conn, data)
        main()

    
    




    # print("Дешевле всего в - " + str(where_is_cheaper(price_array)))

    ######################

    # _ozon_market = ozon.Ozon()
    # ozon_short_array = start_parsing_ozon(OZON_URL)
    # print(ozon_short_array['name'] + " - " + str(ozon_short_array['offers_price']))

    ######################

    # _citilink_market = citilink.Citilink()
    # citilink_short_array = start_parsing_citilink(CITILINK_URL)
    # print(citilink_short_array['name'] + " - " + str(citilink_short_array['offers_price']))

    ######################

    # _beru_market = beru.Beru()
    # beru_short_array = start_parsing_beru(BERU_URL)
    # print(beru_short_array['name'] + " - " + str(beru_short_array['offers_price']))
    
    ######################

    # _technopoint_market = technopoint.Technopoint()
    # technopoint_short_array = start_parsing_technopoint(DNS_URL)
    # print(technopoint_short_array['name'] + " - " + str(technopoint_short_array['offers_price']))



# Функция запускает парсинг по всем источникам. Warning: функция выполняется долго.
# Функция вернет массив с источником и ценой.
def start_parsing_all_markets(check_items):
    url = {
        'ozon' : check_items[4],
        'citilink' : check_items[5],
        'beru' : check_items[6],
        'dns' : check_items[7]
    }

    # Запускаем все парсеры для парсинга цен
    all_parsing_info = start_parsing_all(url)

    price_array = {
        "ozon" : int(all_parsing_info['ozon']['offers_price']),
        "citilink" : int(all_parsing_info['citilink']['offers_price']),
        "beru" : int(all_parsing_info['beru']['offers_price']),
        "dns" : int(all_parsing_info['dns']['offers_price']),
    }
    #
    return price_array



# Вспомогательная функция для сортировки
def sort_by_value(item):
    return item[1]

def where_is_cheaper(array):
    new_arr = {}
    for k, v in sorted(array.items(), key=sort_by_value):
        new_arr[k] = v
    # new_arr - отсортировано по порядку возрастания цены
    # return new_arr
    return next(iter(new_arr))



if __name__ == '__main__':
    main()